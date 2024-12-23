#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que contiene la interfaz gráfica wxPython.
Se mezcla y guarda el audio en tiempo real.
Al detener la grabación, si se requiere conversión a otro formato, se muestra un diálogo modal "espere por favor",
pero la conversión se realiza en un hilo separado para no bloquear la GUI. Al finalizar, se cierra el diálogo
y se informa el resultado.

La escritura en disco durante la grabación se hace con flush() en recorder.py para asegurar
que los archivos crezcan continuamente.

Los atajos globales se registran con wx.RegisterHotKey() para que funcionen incluso si la
aplicación no está en primer plano.

Se implementa la opción de minimizar a la bandeja, con ícono y menú contextual,
usando métodos show_icon() y hide_icon() para manejar su visibilidad.

Se modificó la lógica de cierre (on_close):
- Si hay grabación en curso al momento de cerrar, se pregunta al usuario si desea detener y salir.
  - Si dice “No”, se cancela el cierre.
  - Si dice “Sí”, se detiene la grabación, se muestra el diálogo "Por favor espere..." mientras se guarda/convierte,
    y luego se muestra el mensaje final con la ruta. Al aceptar, se cierra la app.
- Si no hay grabación pero hay conversión en curso, se muestra el diálogo de espera hasta que termine la conversión,
  y luego se cierra.
"""

import os
import sys
import wx
import wx.adv
import soundcard as sc
import winsound
import datetime
import numpy as np
import soundfile as sf
import time
from threading import Thread, Event
import base64
import io

from core.utils import get_base_path
from core.config import save_config, load_config
from core.devices import (
	update_selected_mic, update_selected_system, refresh_devices,
	update_quality, update_output_format, update_bitrate,
	update_mic_volume, update_system_volume
)
from core.recorder import record_audio, to_mono
from ui.widgets import mensaje
from ui.manual import ManualDialog
from core.hotkeys import load_hotkeys_from_config
from core.info import _version, _nombre, _manual, _icono


# IDs para las hotkeys globales
HOTKEY_ID_START = wx.NewIdRef()
HOTKEY_ID_STOP = wx.NewIdRef()


class MyTaskBarIcon(wx.adv.TaskBarIcon):
	"""
	Icono de la aplicación en la bandeja del sistema.
	Muestra un menú contextual para mostrar la ventana o cerrar la app.
	"""
	def __init__(self, parent_frame):
		super().__init__()
		self.parent_frame = parent_frame
		self._visible = False

		# Icono en base64 embebido (por ejemplo, en otro módulo)
		self.icon = self._create_icon_from_base64(_icono)

		# Quita cualquier ícono anterior
		self.RemoveIcon()

		# Vinculamos el evento de doble clic con botón izquierdo
		self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.on_left_double_click)

	def _create_icon_from_base64(self, icon_b64):
		icon_bytes = base64.b64decode(icon_b64)
		stream = io.BytesIO(icon_bytes)

		# IMPORTANTE: El tipo debe coincidir con la imagen. Si es PNG:
		icon_image = wx.Image(stream, wx.BITMAP_TYPE_PNG)

		bitmap = wx.Bitmap(icon_image)
		icon = wx.Icon()
		icon.CopyFromBitmap(bitmap)
		return icon

	def show_icon(self):
		"""
		Muestra el ícono en la bandeja.
		"""
		if self.icon.IsOk():
			self.SetIcon(self.icon, "WASAPIRecording")
		else:
			self.SetIcon(wx.Icon(), "WASAPIRecording")  # en caso de no cargar bien
		self._visible = True

	def hide_icon(self):
		"""
		Oculta y elimina el ícono de la bandeja.
		"""
		self.RemoveIcon()
		self._visible = False

	def CreatePopupMenu(self):
		menu = wx.Menu()
		item_show = menu.Append(-1, _("Mostrar aplicación"))
		item_close = menu.Append(-1, _("Cerrar"))
		self.Bind(wx.EVT_MENU, self.on_show_app, item_show)
		self.Bind(wx.EVT_MENU, self.on_close_app, item_close)
		return menu

	def on_left_double_click(self, event):
		self.on_show_app(event)

	def on_show_app(self, event):
		self.parent_frame.Show()
		self.parent_frame.Iconize(False)
		self.parent_frame.Raise()

	def on_close_app(self, event):
		self.parent_frame.on_close(None)

class PleaseWaitDialog(wx.Dialog):
	"""
	Diálogo modal que muestra un mensaje de "espere por favor" y
	reproduce un beep mientras se realiza un proceso en hilo separado.
	"""
	def __init__(self, parent, message=_("Espere por favor... Procesando")):
		super().__init__(parent, title=_("Procesando"), style=wx.STAY_ON_TOP | wx.BORDER_NONE)
		self.SetWindowStyleFlag(
			self.GetWindowStyleFlag()
			& ~wx.CLOSE_BOX
			& ~wx.MAXIMIZE_BOX
			& ~wx.MINIMIZE_BOX
			& ~wx.SYSTEM_MENU
		)

		# Evitamos cerrar con Alt+F4
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)

		panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(panel, label=message)
		label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
		sizer.Add(label, 0, wx.ALL | wx.CENTER, 20)
		panel.SetSizer(sizer)
		self.Fit()
		self.Centre()

		self.keep_playing = True
		self.sound_thread = Thread(target=self.play_tone, daemon=True)
		self.sound_thread.start()

	def on_key_down(self, event):
		key_code = event.GetKeyCode()
		if key_code == wx.WXK_F4 and event.AltDown():
			return
		event.Skip()

	def play_tone(self):
		import winsound
		while self.keep_playing:
			winsound.Beep(800, 200)
			time.sleep(0.3)

	def stop_tone(self):
		self.keep_playing = False
		self.sound_thread.join()


class ConversionThread(Thread):
	"""
	Hilo para realizar la conversión del formato sin bloquear la GUI.
	"""
	def __init__(self, parent, wav_path, target_format, separate_files, mic_path, system_path):
		super().__init__()
		self.parent = parent
		self.wav_path = wav_path
		self.target_format = target_format
		self.separate_files = separate_files
		self.mic_path = mic_path
		self.system_path = system_path
		self.exception = None
		self.final_path = None

	def run(self):
		try:
			self.final_path = self.parent.convert_to_final_format(
				self.wav_path,
				self.target_format,
				self.separate_files,
				self.mic_path,
				self.system_path
			)
		except Exception as e:
			self.exception = e


class AudioRecorderApp(wx.App):
	"""
	Aplicación principal para grabar audio desde micrófono y sistema.
	"""
	def __init__(self, lang):
		self.lang = lang
		wx.App.__init__(self)

	def OnInit(self):
		self.name = f"WASAPIRecording{wx.GetUserId()}"
		self.instance = wx.SingleInstanceChecker(self.name)
		if self.instance.IsAnotherRunning():
			from ui.widgets import mensaje
			msg = _("""WASAPIRecording ya se encuentra en ejecución.

No se pueden tener dos instancias a la vez.""")
			mensaje(None, msg, "Error", style=wx.OK | wx.ICON_ERROR)
			return False

		self.frame = AudioRecorderFrame()
		self.frame.Show()
		return True


class AudioRecorderFrame(wx.Frame):
	"""
	Ventana principal con la interfaz para grabar audio.
	"""
	def __init__(self):
		super(AudioRecorderFrame, self).__init__(
			None, style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN
		)

		self.get = wx.GetApp()
		# Creamos el icono desde base64 y lo asignamos al frame.
		self.icon = self._create_icon_from_base64(_icono)
		if self.icon.IsOk():
			self.SetIcon(self.icon)
		self.SetTitle(f"WASAPIRecording v{_version}")
		self.output_dir = os.path.join(get_base_path(), "recording")
		self.CONFIG_FILE = os.path.join(get_base_path(), "WASAPIRecording.dat")

		self.recording_event = Event()
		self.recording_thread = None
		self.sample_rate = 48000
		self.channels = 2
		self.mic_volume = 0.5
		self.system_volume = 0.5
		self.selected_mic = sc.default_microphone()
		self.selected_system = sc.get_microphone(sc.default_speaker().name, include_loopback=True)
		self.quality_options = [22050, 44100, 48000]
		self.selected_quality = 48000
		self.output_formats = ["MP3", "WAV", "FLAC", "OGG", "AIFF"]
		self.selected_format = "MP3"
		self.bitrate_options = [128, 192, 256, 320]
		self.selected_bitrate = 192
		self.separate_files = False
		self.mono_mix_enabled = False
		self.combined_output_path = None
		self.mic_output_path = None
		self.system_output_path = None

		# Para saber si el usuario confirmó detener y salir
		self.want_to_close = False

		panel = wx.Panel(self)
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		# ---------------------------
		# Sección Dispositivos
		# ---------------------------
		device_box = wx.StaticBoxSizer(wx.StaticBox(panel, label=_("Dispositivos")), wx.VERTICAL)
		device_box.Add(wx.StaticText(panel, label=_("Micrófon&o:")), 0, wx.ALL, 5)
		self.mic_choice = wx.Choice(panel, choices=[mic.name for mic in sc.all_microphones()])
		self.mic_choice.SetSelection(0)
		self.mic_choice.Bind(wx.EVT_CHOICE, self.on_update_selected_mic)
		device_box.Add(self.mic_choice, 0, wx.ALL | wx.EXPAND, 5)

		device_box.Add(wx.StaticText(panel, label=_("&Sistema (loopback):")), 0, wx.ALL, 5)
		self.system_choice = wx.Choice(
			panel, choices=[sys.name for sys in sc.all_microphones(include_loopback=True)]
		)
		self.system_choice.SetSelection(0)
		self.system_choice.Bind(wx.EVT_CHOICE, self.on_update_selected_system)
		device_box.Add(self.system_choice, 0, wx.ALL | wx.EXPAND, 5)

		self.refresh_button = wx.Button(panel, label=_("&Refrescar Dispositivos"))
		self.refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh_devices)
		device_box.Add(self.refresh_button, 0, wx.ALL | wx.CENTER, 5)

		main_sizer.Add(device_box, 0, wx.ALL | wx.EXPAND, 10)

		# Línea divisoria
		main_sizer.Add(wx.StaticLine(panel), 0, wx.ALL | wx.EXPAND, 10)

		# ---------------------------
		# Sección Configuración
		# ---------------------------
		config_box = wx.StaticBoxSizer(wx.StaticBox(panel, label=_("Configuración de Grabación")), wx.VERTICAL)

		config_box.Add(wx.StaticText(panel, label=_("&Calidad (Hz):")), 0, wx.ALL, 5)
		self.quality_choice = wx.Choice(panel, choices=[str(q) for q in self.quality_options])
		self.quality_choice.SetSelection(2)
		self.quality_choice.Bind(wx.EVT_CHOICE, self.on_update_quality)
		config_box.Add(self.quality_choice, 0, wx.ALL | wx.EXPAND, 5)

		config_box.Add(wx.StaticText(panel, label=_("&Formato de salida:")), 0, wx.ALL, 5)
		self.format_choice = wx.Choice(panel, choices=self.output_formats)
		self.format_choice.SetSelection(0)
		self.format_choice.Bind(wx.EVT_CHOICE, self.on_update_output_format)
		config_box.Add(self.format_choice, 0, wx.ALL | wx.EXPAND, 5)

		config_box.Add(wx.StaticText(panel, label=_("&Bitrate MP3 (kbps):")), 0, wx.ALL, 5)
		self.bitrate_choice = wx.Choice(panel, choices=[str(b) for b in self.bitrate_options])
		self.bitrate_choice.SetSelection(1)
		self.bitrate_choice.Bind(wx.EVT_CHOICE, self.on_update_bitrate)
		config_box.Add(self.bitrate_choice, 0, wx.ALL | wx.EXPAND, 5)

		config_box.Add(wx.StaticText(panel, label=_("Modo de &grabación:")), 0, wx.ALL, 5)
		self.mode_choice = wx.Choice(panel, choices=[_("Mono"), _("Estéreo")])
		self.mode_choice.SetSelection(1)
		config_box.Add(self.mode_choice, 0, wx.ALL | wx.EXPAND, 5)

		self.mono_mix_checkbox = wx.CheckBox(panel, label=_("&Habilitar Mezcla Monoaural"))
		config_box.Add(self.mono_mix_checkbox, 0, wx.ALL, 5)

		self.separate_files_checkbox = wx.CheckBox(panel, label=_("Guardar archivos separados de micrófono &y sistema"))
		config_box.Add(self.separate_files_checkbox, 0, wx.ALL, 5)

		config_box.Add(wx.StaticText(panel, label=_("&Volumen del Micrófono:")), 0, wx.ALL, 5)
		self.mic_volume_slider = wx.Slider(panel, value=100, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL)
		self.mic_volume_slider.Bind(wx.EVT_SLIDER, self.on_update_mic_volume)
		config_box.Add(self.mic_volume_slider, 0, wx.ALL | wx.EXPAND, 5)

		config_box.Add(wx.StaticText(panel, label=_("&Volumen del Sistema:")), 0, wx.ALL, 5)
		self.system_volume_slider = wx.Slider(panel, value=50, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL)
		self.system_volume_slider.Bind(wx.EVT_SLIDER, self.on_update_system_volume)
		config_box.Add(self.system_volume_slider, 0, wx.ALL | wx.EXPAND, 5)

		main_sizer.Add(config_box, 0, wx.ALL | wx.EXPAND, 10)

		# Línea divisoria
		main_sizer.Add(wx.StaticLine(panel), 0, wx.ALL | wx.EXPAND, 10)

		# ---------------------------
		# Botones de control
		# ---------------------------
		control_box = wx.BoxSizer(wx.HORIZONTAL)
		self.start_button = wx.Button(panel, label=_("&Iniciar Grabación"))
		self.start_button.Bind(wx.EVT_BUTTON, self.start_recording)
		control_box.Add(self.start_button, 0, wx.ALL | wx.EXPAND, 5)

		self.stop_button = wx.Button(panel, label=_("&Detener Grabación"))
		self.stop_button.Disable()
		self.stop_button.Bind(wx.EVT_BUTTON, self.stop_recording)
		control_box.Add(self.stop_button, 0, wx.ALL | wx.EXPAND, 5)

		self.test_audio_button = wx.Button(panel, label=_("&Prueba de Audio"))
		self.test_audio_button.Bind(wx.EVT_BUTTON, self.show_test_audio)
		control_box.Add(self.test_audio_button, 0, wx.ALL | wx.EXPAND, 5)

		self.menu_button = wx.Button(panel, label=_("&Menú"))
		self.menu_button.Bind(wx.EVT_BUTTON, self.on_menu_button)
		control_box.Add(self.menu_button, 0, wx.ALL | wx.EXPAND, 5)

		main_sizer.Add(control_box, 0, wx.ALL | wx.CENTER, 10)

		# Línea divisoria
		main_sizer.Add(wx.StaticLine(panel), 0, wx.ALL | wx.EXPAND, 10)

		# ---------------------------
		# Estado / Mensajes
		# ---------------------------
		hk_cfg = load_hotkeys_from_config()
		hotkey_start = hk_cfg["hotkey_start"]
		initial_text = _("En espera (Usa {hk} para iniciar)").format(hk=hotkey_start)

		status_box = wx.StaticBoxSizer(wx.StaticBox(panel, label=_("Estado")), wx.VERTICAL)
		self.status_box = wx.TextCtrl(
			panel, value=initial_text,
			style=wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY
		)
		status_box.Add(self.status_box, 1, wx.ALL | wx.EXPAND, 5)
		main_sizer.Add(status_box, 1, wx.ALL | wx.EXPAND, 10)

		panel.SetSizer(main_sizer)
		main_sizer.Fit(self)
		self.SetMinSize(self.GetSize())
		self.Centre()

		# ---------------------------
		# TaskBarIcon y eventos
		# ---------------------------
		self.tray_icon = MyTaskBarIcon(self)
		self.tray_icon.hide_icon()

		self.Bind(wx.EVT_CLOSE, self.on_close)
		self.Bind(wx.EVT_ICONIZE, self.on_iconify)
		self.Bind(wx.EVT_HOTKEY, self.on_hotkey)

		self.load_config()
		self.validate_and_register_hotkeys()
		self.update_status_message(recording=False)

	def on_iconify(self, event):
		config = load_config(self.CONFIG_FILE)
		minimize_to_tray = config.get("minimize_to_tray", False)

		if event.IsIconized() and minimize_to_tray:
			self.Hide()
			self.tray_icon.show_icon()
		else:
			event.Skip()

	def _create_icon_from_base64(self, icon_b64):
		icon_bytes = base64.b64decode(icon_b64)
		stream = io.BytesIO(icon_bytes)

		# IMPORTANTE: El tipo debe coincidir con la imagen. Si es PNG:
		icon_image = wx.Image(stream, wx.BITMAP_TYPE_PNG)

		bitmap = wx.Bitmap(icon_image)
		icon = wx.Icon()
		icon.CopyFromBitmap(bitmap)
		return icon

	def on_hotkey(self, event):
		hotkey_id = event.GetId()
		if hotkey_id == HOTKEY_ID_START:
			self.start_recording()
		elif hotkey_id == HOTKEY_ID_STOP:
			self.stop_recording()

	def on_close(self, event):
		"""
		Si hay grabación en curso, pedimos confirmación al usuario:
			- "¿Desea detener la grabación y salir?"
			Si NO, cancelamos el cierre. Si SÍ, detenemos y esperamos a la conversión.
			Cuando finalice, mostramos el mensaje final y cerramos.
		Si no hay grabación, revisamos si hay conversión. Si la hay, mostramos "espere por favor" hasta que acabe.
		Luego cerramos.
		"""
		if self.recording_event.is_set():
			resp = mensaje(
				None,
				_("Hay una grabación en curso. ¿Desea detenerla y salir?"),
				_("Confirmar cierre"),
				wx.YES_NO | wx.ICON_WARNING
			)
			if resp == wx.NO:
				if event:
					event.Veto()
				return
			else:
				# El usuario eligió sí => detener grabación y luego al final se cierra
				self.want_to_close = True
				self.stop_recording(None)
		else:
			# No hay grabación => ver si hay conversión
			if hasattr(self, "conversion_thread") and self.conversion_thread.is_alive():
				wait_dlg = PleaseWaitDialog(self, _("Por favor espere, finalizando conversión..."))
				wait_dlg.Show()
				while self.conversion_thread.is_alive():
					wx.Yield()
					time.sleep(0.1)
				wait_dlg.stop_tone()
				wait_dlg.Destroy()

			# Cerrar definitivamente
			self.final_close()

	def final_close(self):
		try:
			self.UnregisterHotKey(HOTKEY_ID_START)
			self.UnregisterHotKey(HOTKEY_ID_STOP)
		except:
			pass

		if hasattr(self, "tray_icon"):
			self.tray_icon.hide_icon()
			self.tray_icon.Destroy()

		self.save_config_wrapper()
		self.Destroy()

	def on_refresh_devices(self, event):
		refresh_devices(self.mic_choice, self.system_choice, self.status_box)

	def on_update_selected_mic(self, event):
		selected_name = self.mic_choice.GetStringSelection()
		self.selected_mic = update_selected_mic(selected_name)

	def on_update_selected_system(self, event):
		selected_name = self.system_choice.GetStringSelection()
		self.selected_system = update_selected_system(selected_name)

	def on_update_quality(self, event):
		self.selected_quality = update_quality(self.quality_choice)
		self.sample_rate = self.selected_quality

	def on_update_output_format(self, event):
		self.selected_format = update_output_format(self.format_choice)

	def on_update_bitrate(self, event):
		self.selected_bitrate = update_bitrate(self.bitrate_choice)

	def on_update_mic_volume(self, event):
		self.mic_volume = update_mic_volume(self.mic_volume_slider)

	def on_update_system_volume(self, event):
		self.system_volume = update_system_volume(self.system_volume_slider)

	def toggle_controls(self, enable):
		self.mic_choice.Enable(enable)
		self.system_choice.Enable(enable)
		self.quality_choice.Enable(enable)
		self.format_choice.Enable(enable)
		self.bitrate_choice.Enable(enable)
		self.mode_choice.Enable(enable)
		self.mono_mix_checkbox.Enable(enable)
		self.separate_files_checkbox.Enable(enable)
		self.start_button.Enable(enable)
		self.refresh_button.Enable(enable)
		self.test_audio_button.Enable(enable)

	def start_recording(self, event=None):
		if not self.recording_event.is_set():
			self.recording_event.set()
			self.toggle_controls(False)
			self.stop_button.Enable()
			self.stop_button.SetFocus()

			self.update_status_message(recording=True)
			winsound.Beep(1000, 200)

			self.channels = 1 if self.mode_choice.GetStringSelection() == _("Mono") else 2
			self.separate_files = self.separate_files_checkbox.GetValue()
			self.mono_mix_enabled = self.mono_mix_checkbox.IsChecked()

			timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

			self.combined_output_path = os.path.join(self.output_dir, f"recording_{timestamp}.wav")
			self.mic_output_path = (
				os.path.join(self.output_dir, f"recording_mic_{timestamp}.wav")
				if self.separate_files
				else None
			)
			self.system_output_path = (
				os.path.join(self.output_dir, f"recording_system_{timestamp}.wav")
				if self.separate_files
				else None
			)

			self.recording_thread = Thread(
				target=record_audio,
				args=(
					self.recording_event,
					self.selected_mic,
					self.selected_system,
					self.sample_rate,
					self.channels,
					self.output_dir,
					self.combined_output_path,
					self.mic_output_path,
					self.system_output_path,
					self.mono_mix_enabled,
					self.mic_volume,
					self.system_volume
				)
			)
			self.recording_thread.start()

	def stop_recording(self, event=None):
		if self.recording_event.is_set():
			self.recording_event.clear()
			self.toggle_controls(True)
			self.stop_button.Disable()
			self.start_button.SetFocus()
			self.update_status_message(recording=False)
			winsound.Beep(500, 200)

			if self.recording_thread:
				self.recording_thread.join()

			if self.selected_format != "WAV":
				self.dialog = PleaseWaitDialog(self, _("Por favor espere, convirtiendo a formato final..."))
				self.dialog.Show()

				self.conversion_thread = ConversionThread(
					self,
					self.combined_output_path,
					self.selected_format,
					self.separate_files,
					self.mic_output_path,
					self.system_output_path
				)
				self.conversion_thread.start()

				self.timer = wx.Timer(self)
				self.Bind(wx.EVT_TIMER, self.on_conversion_check, self.timer)
				self.timer.Start(500)
			else:
				# Sin conversión
				message = _("Grabación completada. Archivo guardado como:\n{file_path}").format(
					file_path=self.combined_output_path
				)
				if self.separate_files and self.mic_output_path and self.system_output_path:
					message += _(
						"\nArchivo separado de micrófono: {mic_path}\nArchivo separado de sistema: {system_path}"
					).format(
						mic_path=self.mic_output_path,
						system_path=self.system_output_path
					)

				# Si queremos cerrar => mostramos mensaje y cerramos
				if self.want_to_close:
					res = mensaje(None, message, _("Grabación"), style=wx.OK | wx.ICON_INFORMATION)
					self.final_close()
				else:
					self.show_info_message(message, _("Grabación"))

	def on_conversion_check(self, event):
		if not hasattr(self, "conversion_thread"):
			return

		if self.conversion_thread.is_alive():
			return

		self.timer.Stop()
		self.dialog.stop_tone()
		self.dialog.Destroy()

		if self.conversion_thread.exception:
			self.show_error_message(
				f"Error al convertir el archivo: {self.conversion_thread.exception}"
			)
			self.show_error_message(
				_("Error al convertir el archivo: {error}").format(
					error=self.conversion_thread.exception
				)
			)
			# Si queríamos cerrar, cerramos
			if self.want_to_close:
				self.final_close()
		else:
			final_path = self.conversion_thread.final_path
			message = _("Grabación completada. Archivo guardado como:\n{file_path}").format(
				file_path=final_path
			)
			if self.separate_files and self.mic_output_path and self.system_output_path:
				ext = self.selected_format.lower()
				mic_final = (
					self.mic_output_path.replace(".wav", f".{ext}")
					if self.mic_output_path
					else None
				)
				sys_final = (
					self.system_output_path.replace(".wav", f".{ext}")
					if self.system_output_path
					else None
				)
				if mic_final and sys_final:
					message += _(
						"\nArchivo separado de micrófono: {mic_path}\nArchivo separado de sistema: {sys_path}"
					).format(
						mic_path=mic_final,
						sys_path=sys_final
					)

			if self.want_to_close:
				res = mensaje(None, message, _("Grabación"), style=wx.OK | wx.ICON_INFORMATION)
				self.final_close()
			else:
				self.show_info_message(message, _("Grabación"))

	def convert_to_final_format(self, wav_path, target_format, separate_files, mic_path, system_path):
		if target_format == "MP3":
			final_path = self.save_as_mp3(wav_path)
			if separate_files:
				if mic_path:
					self.save_as_mp3(mic_path)
				if system_path:
					self.save_as_mp3(system_path)
		else:
			final_path = self.save_as_format(wav_path, target_format)
			if separate_files:
				if mic_path:
					self.save_as_format(mic_path, target_format)
				if system_path:
					self.save_as_format(system_path, target_format)
		return final_path

	def save_as_mp3(self, wav_file_path):
		import lameenc
		data, samplerate = sf.read(wav_file_path)

		encoder = lameenc.Encoder()
		encoder.set_bit_rate(self.selected_bitrate)
		encoder.set_in_sample_rate(samplerate)
		channels = 2 if len(data.shape) > 1 else 1
		encoder.set_channels(channels)
		encoder.set_quality(2)

		data_int16 = (data * 32767).astype(np.int16).tobytes()
		mp3_data = encoder.encode(data_int16) + encoder.flush()

		mp3_path = wav_file_path.replace(".wav", ".mp3")
		with open(mp3_path, "wb") as mp3_file:
			mp3_file.write(mp3_data)

		os.remove(wav_file_path)
		return mp3_path

	def save_as_format(self, wav_file_path, target_format):
		data, samplerate = sf.read(wav_file_path)
		out_path = wav_file_path.replace(".wav", f".{target_format.lower()}")
		sf.write(out_path, data, samplerate, format=target_format)
		os.remove(wav_file_path)
		return out_path

	def show_about(self, event):
		msg = \
_("""WASAPIRecording
Versión {}
Creado por {}""").format(_version, _nombre)
		self.show_info_message(
			msg,
			_("Acerca de...")
		)

	def open_recordings_directory(self, event):
		try:
			if not os.path.exists(self.output_dir):
				os.makedirs(self.output_dir)
			os.startfile(self.output_dir)
		except Exception as e:
			self.show_error_message(
				_("No se pudo abrir el directorio de grabaciones: {error}").format(error=e)
			)

	def show_error_message(self, message, title=_("Error")):
		mensaje(None, message, title, style=wx.OK | wx.ICON_ERROR)

	def show_info_message(self, message, title=_("Información")):
		mensaje(None, message, title, style=wx.OK | wx.ICON_INFORMATION)

	def save_config_wrapper(self):
		config_file = os.path.join(get_base_path(), "WASAPIRecording.dat")
		config = load_config(config_file)

		config["mic_name"] = self.selected_mic.name if self.selected_mic else ""
		config["system_name"] = self.selected_system.name if self.selected_system else ""
		config["quality"] = self.sample_rate
		config["format"] = self.selected_format
		config["bitrate"] = self.selected_bitrate
		config["mic_volume"] = self.mic_volume_slider.GetValue()
		config["system_volume"] = self.system_volume_slider.GetValue()
		config["mode"] = self.mode_choice.GetStringSelection()
		config["mono_mix"] = self.mono_mix_checkbox.GetValue()
		config["separate_files"] = self.separate_files_checkbox.GetValue()

		save_config(self.CONFIG_FILE, config)
		self.get.lang.set_language(self.get.lang.current_lang)

	def load_config(self):
		config = load_config(self.CONFIG_FILE)
		mics = [mic.name for mic in sc.all_microphones()]
		mic_name = config.get("mic_name", "")
		if mic_name in mics:
			self.selected_mic = next(m for m in sc.all_microphones() if m.name == mic_name)
			self.mic_choice.SetItems(mics)
			self.mic_choice.SetSelection(mics.index(mic_name))
		else:
			self.selected_mic = sc.default_microphone()
			self.mic_choice.SetItems(mics)
			if self.selected_mic.name in mics:
				self.mic_choice.SetSelection(mics.index(self.selected_mic.name))

		systems = [s.name for s in sc.all_microphones(include_loopback=True)]
		system_name = config.get("system_name", "")
		if system_name in systems:
			self.selected_system = next(
				s for s in sc.all_microphones(include_loopback=True) if s.name == system_name
			)
			self.system_choice.SetItems(systems)
			self.system_choice.SetSelection(systems.index(system_name))
		else:
			self.selected_system = sc.get_microphone(sc.default_speaker().name, include_loopback=True)
			self.system_choice.SetItems(systems)
			if self.selected_system.name in systems:
				self.system_choice.SetSelection(systems.index(self.selected_system.name))

		self.sample_rate = config.get("quality", self.sample_rate)
		if self.sample_rate in self.quality_options:
			self.quality_choice.SetSelection(self.quality_options.index(self.sample_rate))

		self.selected_format = config.get("format", self.selected_format)
		if self.selected_format in self.output_formats:
			self.format_choice.SetSelection(self.output_formats.index(self.selected_format))

		self.selected_bitrate = config.get("bitrate", self.selected_bitrate)
		if self.selected_bitrate in self.bitrate_options:
			self.bitrate_choice.SetSelection(self.bitrate_options.index(self.selected_bitrate))

		mic_volume = config.get("mic_volume", 50)
		self.mic_volume_slider.SetValue(mic_volume)
		self.mic_volume = mic_volume / 100.0

		system_volume = config.get("system_volume", 50)
		self.system_volume_slider.SetValue(system_volume)
		self.system_volume = system_volume / 100.0

		mode = config.get("mode", _("Estéreo"))
		if mode in [_("Mono"), _("Estéreo")]:
			self.mode_choice.SetSelection(0 if mode == _("Mono") else 1)

		mono_mix = config.get("mono_mix", False)
		self.mono_mix_checkbox.SetValue(mono_mix)

		self.separate_files_checkbox.SetValue(config.get("separate_files", False))

	def on_menu_button(self, event):
		menu = wx.Menu()

		submenu_idiomas = wx.Menu()
		if not self.recording_event.is_set():
			item_de = submenu_idiomas.AppendRadioItem(-1, _("Alemán"))
			item_es = submenu_idiomas.AppendRadioItem(-1, _("Español"))
			item_fr = submenu_idiomas.AppendRadioItem(-1, _("Francés"))
			item_en = submenu_idiomas.AppendRadioItem(-1, _("Inglés"))
			item_it = submenu_idiomas.AppendRadioItem(-1, _("Italiano"))
			item_pt = submenu_idiomas.AppendRadioItem(-1, _("Portugués"))
			item_tr = submenu_idiomas.AppendRadioItem(-1, _("Turco"))

			current_language = self.get.lang.current_lang
			if current_language == "es":
				item_es.Check(True)
			elif current_language == "en":
				item_en.Check(True)
			elif current_language == "it":
				item_it.Check(True)
			elif current_language == "fr":
				item_fr.Check(True)
			elif current_language == "pt":
				item_pt.Check(True)
			elif current_language == "de":
				item_de.Check(True)
			elif current_language == "tr":
				item_tr.Check(True)

			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('es'), item_es)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('en'), item_en)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('fr'), item_fr)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('it'), item_it)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('de'), item_de)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('pt'), item_pt)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('tr'), item_tr)

			item_opciones = menu.Append(-1, _("Opciones"))
			menu.AppendSubMenu(submenu_idiomas, _("Idioma"))
			item_abrir = menu.Append(-1, _("Abrir Grabaciones"))
			item_manual = menu.Append(-1, _("&Manual de usuario"))
			item_acerca = menu.Append(-1, _("Acerca &de..."))
			item_donar = menu.Append(-1, _("invítame a un &café si te gusta mi trabajo"))
			item_cerrar = menu.Append(-1, _("Salir"))

			self.Bind(wx.EVT_MENU, self.show_options_dialog, item_opciones)
			self.Bind(wx.EVT_MENU, self.open_recordings_directory, item_abrir)
			self.Bind(wx.EVT_MENU, self.on_show_manual, item_manual)
			self.Bind(wx.EVT_MENU, self.show_about, item_acerca)
			self.Bind(wx.EVT_MENU, self.on_donar, item_donar)
			self.Bind(wx.EVT_MENU, self.on_close, item_cerrar)
		else:
			item_abrir = menu.Append(-1, _("Abrir Grabaciones"))
			item_donar = menu.Append(-1, _("&invítame a un café si te gusta mi trabajo"))
			item_cerrar = menu.Append(-1, _("Cerrar"))
			self.Bind(wx.EVT_MENU, self.open_recordings_directory, item_abrir)
			self.Bind(wx.EVT_MENU, self.on_donar, item_donar)
			self.Bind(wx.EVT_MENU, self.on_close, item_cerrar)

		self.PopupMenu(menu)
		menu.Destroy()

	def cambiar_idioma(self, nuevo_idioma):
		if nuevo_idioma != self.get.lang.current_lang:
			msg = _("Para aplicar el nuevo idioma se necesita reiniciar la aplicación.\n¿Desea continuar?")
			res = mensaje(None, msg, _("Confirmar cambio de idioma"), wx.YES_NO | wx.ICON_QUESTION)
			if res == wx.YES:
				self.get.lang.set_language(nuevo_idioma)
				self.restart_app()

	def restart_app(self):
		"""
		Reinicia la aplicación respetando el entorno de ejecución, ya sea PyInstaller o no.
		"""
		try:
			# Cierra la aplicación actual
			self.Close()

			# Prepara los argumentos para reiniciar
			args = sys.argv[:]
			if hasattr(sys, '_MEIPASS'):  # Si está empaquetada con PyInstaller
				executable = sys.executable
			else:  # En desarrollo
				executable = sys.executable
				args.insert(0, executable)

			# Formatea los argumentos para Windows
			if sys.platform == 'win32':
				args = ['"%s"' % arg for arg in args]

			# Ejecuta el reinicio
			os.execv(executable, args)
		except Exception as e:
			self.show_error_message(f"Error al intentar reiniciar la aplicación: {e}")

	def show_options_dialog(self, event):
		from ui.options import OptionsDialog
		dlg = OptionsDialog(self)
		if dlg.ShowModal() == wx.ID_OK:
			general_changed, keyboard_changed = dlg.save_all_settings2()
			if keyboard_changed:
				self.validate_and_register_hotkeys()
				self.update_status_message(recording=self.recording_event.is_set())
		dlg.Destroy()

	def validate_and_register_hotkeys(self):
		from core.hotkeys import load_hotkeys_from_config, parse_hotkey, can_register_hotkey, save_hotkeys_to_config

		try:
			self.UnregisterHotKey(HOTKEY_ID_START)
			self.UnregisterHotKey(HOTKEY_ID_STOP)
		except:
			pass

		cfg = load_hotkeys_from_config()
		changed = False

		if cfg["hotkey_start"] != "Sin asignar":
			modifiers, key_code = parse_hotkey(cfg["hotkey_start"])
			if not self.RegisterHotKey(HOTKEY_ID_START, modifiers, key_code):
				cfg["hotkey_start"] = "Sin asignar"
				changed = True

		if cfg["hotkey_stop"] != "Sin asignar":
			modifiers, key_code = parse_hotkey(cfg["hotkey_stop"])
			if not self.RegisterHotKey(HOTKEY_ID_STOP, modifiers, key_code):
				cfg["hotkey_stop"] = "Sin asignar"
				changed = True

		if changed:
			save_hotkeys_to_config(cfg["hotkey_start"], cfg["hotkey_stop"])

	def update_status_message(self, recording=False):
		from core.hotkeys import load_hotkeys_from_config
		cfg = load_hotkeys_from_config()

		hotkey_start = cfg["hotkey_start"]
		hotkey_stop = cfg["hotkey_stop"]

		if recording:
			if hotkey_stop == "Sin asignar":
				self.status_box.SetValue(_("Grabando... (No hay hotkey de detener asignada)"))
			else:
				self.status_box.SetValue(_("Grabando... (Usa {hk} para detener)").format(hk=hotkey_stop))
		else:
			if hotkey_start == "Sin asignar":
				self.status_box.SetValue(_("En espera. Asigna teclas en Opciones o inicia manualmente."))
			else:
				self.status_box.SetValue(_("En espera (Usa {hk} para iniciar)").format(hk=hotkey_start))

	def show_test_audio(self, event):
		from ui.test_audio import TestAudioDialog

		separate_files_value = self.separate_files_checkbox.GetValue()
		mic_vol_slider_val = self.mic_volume_slider.GetValue()
		mic_volume = mic_vol_slider_val / 100.0
		system_vol_slider_val = self.system_volume_slider.GetValue()
		system_volume = system_vol_slider_val / 100.0
		mono_mix_enabled = self.mono_mix_checkbox.IsChecked()

		selected_quality_index = self.quality_choice.GetSelection()
		sample_rate = int(self.quality_choice.GetString(selected_quality_index))

		mode_index = self.mode_choice.GetSelection()
		mode_text = self.mode_choice.GetString(mode_index)
		channels = 1 if mode_text == _("Mono") else 2

		mic_index = self.mic_choice.GetSelection()
		mic_name = self.mic_choice.GetString(mic_index)
		selected_mic = update_selected_mic(mic_name)

		system_index = self.system_choice.GetSelection()
		system_name = self.system_choice.GetString(system_index)
		selected_system = update_selected_system(system_name)

		dlg = TestAudioDialog(
			parent=self,
			selected_mic=selected_mic,
			selected_system=selected_system,
			sample_rate=sample_rate,
			channels=channels,
			separate_files=separate_files_value,
			mono_mix=mono_mix_enabled,
			mic_volume=mic_volume,
			system_volume=system_volume
		)
		dlg.ShowModal()
		dlg.Destroy()

	def on_donar(self, event):
		wx.LaunchDefaultBrowser("https://paypal.me/hjbcdonaciones")

	def on_show_manual(self, event):
		# Suponiendo que _manual es tu cadena con el manual completo
		dialogo = ManualDialog(self, _manual)
		dialogo.ShowModal()
		dialogo.Destroy()