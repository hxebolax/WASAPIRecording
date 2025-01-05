#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que contiene la interfaz gráfica wxPython.

Este módulo permite:
 - Elegir la carpeta de grabaciones en las opciones de la pestaña General.
 - Usar la carpeta configurada para abrir el directorio de grabación.
 - Mantener './recording' por defecto si el usuario no cambia la carpeta.
 - Al detener la grabación (y no ser cancelada), preguntar con Sí/No si se desea abrir la carpeta de grabaciones.

Incluye las clases y funciones principales para el control de la ventana principal,
la bandeja del sistema, la lógica de conversión, y la configuración de la aplicación.
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
from core.recorder import record_audio
from ui.widgets import mensaje
from ui.manual import ManualDialog
from ui.update import UpdateDialog
from core.hotkeys import load_hotkeys_from_config, parse_hotkey, save_hotkeys_to_config
from core.info import _version, _nombre, _manual, _icono
from core.logger import Logger

logger = Logger(log_dir=os.path.abspath(os.path.join(get_base_path(), "logs")))

HOTKEY_ID_START = wx.NewIdRef()
HOTKEY_ID_STOP = wx.NewIdRef()
HOTKEY_ID_PAUSE = wx.NewIdRef()
HOTKEY_ID_CANCEL = wx.NewIdRef()

class MyTaskBarIcon(wx.adv.TaskBarIcon):
	"""
	Clase que representa el ícono en la bandeja del sistema.

	Permite:
	- Mostrar y ocultar el ícono.
	- Crear un menú contextual con opciones para mostrar la ventana principal o cerrar la aplicación.
	- Detectar doble clic izquierdo para restaurar la ventana.
	"""
	def __init__(self, parent_frame):
		"""
		Constructor de la clase MyTaskBarIcon.

		:param parent_frame: Ventana principal asociada al ícono de bandeja.
		"""
		super().__init__()
		self.parent_frame = parent_frame
		self._visible = False

		self.icon = self._create_icon_from_base64(_icono)
		logger.log_action("Icono de la bandeja creado.")
		self.RemoveIcon()
		self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.on_left_double_click)

	def _create_icon_from_base64(self, icon_b64):
		"""
		Crea un ícono a partir de datos en Base64.

		:param icon_b64: Cadena de texto en Base64 representando la imagen del ícono.
		:return: Objeto wx.Icon o ícono por defecto en caso de error.
		"""
		try:
			icon_bytes = base64.b64decode(icon_b64)
			stream = io.BytesIO(icon_bytes)
			icon_image = wx.Image(stream, wx.BITMAP_TYPE_PNG)
			bitmap = wx.Bitmap(icon_image)
			icon = wx.Icon()
			icon.CopyFromBitmap(bitmap)
			logger.log_action("Icono creado desde base64 exitosamente.")
			return icon
		except Exception as e:
			logger.log_error(f"Error al crear icono desde base64: {e}")
			return wx.Icon()

	def show_icon(self):
		"""
		Muestra el ícono en la bandeja del sistema.
		"""
		if self.icon.IsOk():
			self.SetIcon(self.icon, "WASAPIRecording")
			logger.log_action("Icono mostrado en la bandeja.")
		else:
			self.SetIcon(wx.Icon(), "WASAPIRecording")
			logger.log_error("Icono no válido. Se muestra un icono por defecto.")
		self._visible = True

	def hide_icon(self):
		"""
		Oculta y elimina el ícono de la bandeja del sistema.
		"""
		self.RemoveIcon()
		logger.log_action("Icono ocultado y eliminado de la bandeja.")
		self._visible = False

	def CreatePopupMenu(self):
		"""
		Crea el menú contextual para el ícono de la bandeja.

		:return: Menú wx.Menu con opciones para mostrar la aplicación o cerrarla.
		"""
		menu = wx.Menu()
		item_show = menu.Append(-1, _("Mostrar aplicación"))
		item_close = menu.Append(-1, _("Cerrar"))
		self.Bind(wx.EVT_MENU, self.on_show_app, item_show)
		self.Bind(wx.EVT_MENU, self.on_close_app, item_close)
		logger.log_action("Menú contextual creado en el icono de la bandeja.")
		return menu

	def on_left_double_click(self, event):
		"""
		Maneja el evento de doble clic izquierdo sobre el ícono de la bandeja.

		:param event: Evento wx.EVT_TASKBAR_LEFT_DCLICK.
		"""
		logger.log_action("Doble clic detectado en el icono de la bandeja.")
		self.on_show_app(event)

	def on_show_app(self, event):
		"""
		Muestra o restaura la ventana principal de la aplicación.

		:param event: Evento de menú asociado.
		"""
		logger.log_action("Mostrando la ventana principal desde el icono de la bandeja.")
		self.parent_frame.Show()
		self.parent_frame.Iconize(False)
		self.parent_frame.Raise()

	def on_close_app(self, event):
		"""
		Cierra la aplicación desde el ícono de la bandeja.

		:param event: Evento de menú asociado.
		"""
		logger.log_action("Cerrando la aplicación desde el icono de la bandeja.")
		self.parent_frame.on_close(None)

class PleaseWaitDialog(wx.Dialog):
	"""
	Diálogo que muestra un mensaje de espera y reproduce un tono recurrente
	mientras se realiza una tarea en segundo plano (por ejemplo, conversión de formato).
	"""
	def __init__(self, parent, message=_("Espere por favor... Procesando")):
		"""
		Constructor del diálogo.

		:param parent: Ventana padre.
		:param message: Mensaje a mostrar en la interfaz.
		"""
		super().__init__(parent, title=_("Procesando"), style=wx.STAY_ON_TOP | wx.BORDER_NONE)
		self.SetWindowStyleFlag(
			self.GetWindowStyleFlag()
			& ~wx.CLOSE_BOX
			& ~wx.MAXIMIZE_BOX
			& ~wx.MINIMIZE_BOX
			& ~wx.SYSTEM_MENU
		)
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
		logger.log_action("Diálogo 'Por favor espere' creado y sonido iniciado.")

	def on_key_down(self, event):
		"""
		Maneja la presión de teclas dentro del diálogo, bloquea Alt+F4.

		:param event: Evento de teclado.
		"""
		key_code = event.GetKeyCode()
		if key_code == wx.WXK_F4 and event.AltDown():
			return
		event.Skip()

	def play_tone(self):
		"""
		Reproduce un tono de manera recurrente mientras keep_playing sea True.
		"""
		try:
			import winsound
			while self.keep_playing:
				winsound.Beep(800, 200)
				time.sleep(0.3)
		except Exception as e:
			logger.log_error(f"Error al reproducir tono en el diálogo 'Por favor espere': {e}")

	def stop_tone(self):
		"""
		Detiene la reproducción del tono y finaliza el hilo asociado.
		"""
		self.keep_playing = False
		self.sound_thread.join()
		logger.log_action("Tono del diálogo 'Por favor espere' detenido.")

class ConversionThread(Thread):
	"""
	Hilo que realiza la conversión de formatos de audio
	para no bloquear la interfaz principal durante la operación.
	"""
	def __init__(self, parent, wav_path, target_format, separate_files, mic_path, system_path):
		"""
		Constructor del hilo de conversión.

		:param parent: Referencia a la ventana principal (AudioRecorderFrame).
		:param wav_path: Ruta del archivo WAV combinado.
		:param target_format: Formato de salida deseado (MP3, WAV, etc.).
		:param separate_files: Booleano que indica si se están grabando archivos por separado.
		:param mic_path: Ruta del archivo WAV de micrófono.
		:param system_path: Ruta del archivo WAV de sistema.
		"""
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
		"""
		Inicia la conversión de los archivos y actualiza la interfaz
		sobre el éxito o fracaso de la operación.
		"""
		try:
			logger.log_action(f"Iniciando conversión de {self.wav_path} a {self.target_format}.")
			self.final_path = self.parent.convert_to_final_format(
				self.wav_path,
				self.target_format,
				self.separate_files,
				self.mic_path,
				self.system_path
			)
			logger.log_action(f"Conversión completada: {self.final_path}.")
		except Exception as e:
			self.exception = e
			logger.log_error(f"Error durante la conversión: {e}")

class AudioRecorderApp(wx.App):
	"""
	Clase que representa la aplicación wxPython. Maneja:
	- El control de una sola instancia.
	- La inicialización de la ventana principal.
	- El idioma actual.
	"""
	def __init__(self, lang):
		"""
		Constructor de la clase AudioRecorderApp.

		:param lang: Objeto que gestiona el idioma y las traducciones (core.i18n.I18n).
		"""
		self.lang = lang
		super().__init__()

	def OnInit(self):
		"""
		Método que se llama al iniciar la aplicación.

		:return: True si se crea la ventana principal, False si no.
		"""
		self.name = f"WASAPIRecording{wx.GetUserId()}"
		self.instance = wx.SingleInstanceChecker(self.name)
		if self.instance.IsAnotherRunning():
			msg = _("""WASAPIRecording ya se encuentra en ejecución.
No se pueden tener dos instancias a la vez.""")
			mensaje(None, msg, "Error", style=wx.OK | wx.ICON_ERROR)
			logger.log_error("Intento de iniciar una segunda instancia de la aplicación.")
			return False

		self.frame = AudioRecorderFrame()
		self.frame.Show()
		logger.log_action("Aplicación iniciada y ventana principal mostrada.")
		return True

class AudioRecorderFrame(wx.Frame):
	"""
	Ventana principal de la aplicación WASAPIRecording.

	Contiene la lógica para:
	- Configurar dispositivos (micrófono, sistema).
	- Ajustar calidad, formato, bitrate, volumen y buffer.
	- Iniciar, pausar, detener y cancelar grabaciones.
	- Manejar hotkeys globales para controlar la grabación.
	- Mostrar menús, manual de usuario y opciones de configuración.
	"""
	def __init__(self):
		"""
		Constructor de la ventana principal.
		"""
		super().__init__(
			None, style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN
		)

		self.get = wx.GetApp()
		self.icon = self._create_icon_from_base64(_icono)
		if self.icon.IsOk():
			self.SetIcon(self.icon)
			logger.log_action("Icono de la ventana principal establecido correctamente.")
		else:
			logger.log_error("Icono de la ventana principal no es válido.")

		self.SetTitle(f"WASAPIRecording v{_version}")

		self.CONFIG_FILE = os.path.abspath(os.path.join(get_base_path(), "WASAPIRecording.dat"))
		config_data = load_config(self.CONFIG_FILE)
		default_dir = os.path.abspath(os.path.join(get_base_path(), "recording"))
		self.output_dir = config_data.get("recording_dir", "")
		if not self.output_dir:
			self.output_dir = default_dir

		logger.log_action(f"DEBUG: Directorio de grabaciones inicial => {self.output_dir}")

		self.is_update = False
		self.recording_event = Event()
		self.pause_event = Event()
		self.cancel_event = Event()
		self.recording_thread = None
		self.sample_rate = 48000

		self.channels = 2  # Siempre estéreo

		self.mic_volume = 0.5
		self.system_volume = 0.5
		self.selected_mic = sc.default_microphone()
		self.selected_system = sc.get_microphone(sc.default_speaker().name, include_loopback=True)
		self.quality_options = [22050, 44100, 48000]
		self.selected_quality = 48000
		self.output_formats = ["MP3", "WAV", "FLAC", "OGG", "AIFF"]
		self.selected_format = "MP3"
		self.bitrate_options = [32, 64, 96, 128, 160, 192, 256, 320]
		self.selected_bitrate = 192

		self.mic_mode = "Estéreo"
		self.system_mode = "Estéreo"

		self.separate_files = False
		self.combined_output_path = None
		self.mic_output_path = None
		self.system_output_path = None
		self.want_to_close = False

		self.buffer_size = 1024

		panel = wx.Panel(self)
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		# Sección Dispositivos
		device_box = wx.StaticBoxSizer(wx.StaticBox(panel, label=_("Dispositivos")), wx.VERTICAL)
		device_box.Add(wx.StaticText(panel, label=_("Micrófon&o:")), 0, wx.ALL, 5)
		self.mic_choice = wx.Choice(panel, choices=[mic.name for mic in sc.all_microphones()])
		self.mic_choice.SetSelection(0)
		self.mic_choice.Bind(wx.EVT_CHOICE, self.on_update_selected_mic)
		device_box.Add(self.mic_choice, 0, wx.ALL | wx.EXPAND, 5)

		device_box.Add(wx.StaticText(panel, label=_("&Sistema (loopback):")), 0, wx.ALL, 5)
		self.system_choice = wx.Choice(
			panel, choices=[sysdev.name for sysdev in sc.all_microphones(include_loopback=True)]
		)
		self.system_choice.SetSelection(0)
		self.system_choice.Bind(wx.EVT_CHOICE, self.on_update_selected_system)
		device_box.Add(self.system_choice, 0, wx.ALL | wx.EXPAND, 5)

		self.refresh_button = wx.Button(panel, label=_("&Refrescar Dispositivos"))
		self.refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh_devices)
		device_box.Add(self.refresh_button, 0, wx.ALL | wx.CENTER, 5)
		main_sizer.Add(device_box, 0, wx.ALL | wx.EXPAND, 10)

		main_sizer.Add(wx.StaticLine(panel), 0, wx.ALL | wx.EXPAND, 10)

		# Sección Configuración
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

		config_box.Add(wx.StaticText(panel, label=_("Modo Micrófon&o:")), 0, wx.ALL, 5)
		self.mic_mode_choice = wx.Choice(panel, choices=[_("Mono"), _("Estéreo")])
		self.mic_mode_choice.SetSelection(1)
		self.mic_mode_choice.Bind(wx.EVT_CHOICE, self.on_update_mic_mode)
		config_box.Add(self.mic_mode_choice, 0, wx.ALL | wx.EXPAND, 5)

		config_box.Add(wx.StaticText(panel, label=_("Modo &Sistema (loopback):")), 0, wx.ALL, 5)
		self.system_mode_choice = wx.Choice(panel, choices=[_("Mono"), _("Estéreo")])
		self.system_mode_choice.SetSelection(1)
		self.system_mode_choice.Bind(wx.EVT_CHOICE, self.on_update_system_mode)
		config_box.Add(self.system_mode_choice, 0, wx.ALL | wx.EXPAND, 5)

		config_box.Add(wx.StaticText(panel, label=_("&Tamaño de buffer (frames):")), 0, wx.ALL, 5)
		self.buffer_spin = wx.SpinCtrl(panel, value=str(self.buffer_size), min=128, max=8192)
		self.buffer_spin.Bind(wx.EVT_SPINCTRL, self.on_update_buffer_size)
		config_box.Add(self.buffer_spin, 0, wx.ALL | wx.EXPAND, 5)

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
		main_sizer.Add(wx.StaticLine(panel), 0, wx.ALL | wx.EXPAND, 10)

		control_box = wx.BoxSizer(wx.HORIZONTAL)
		self.start_button = wx.Button(panel, label=_("&Iniciar Grabación"))
		self.start_button.Bind(wx.EVT_BUTTON, self.start_recording)
		control_box.Add(self.start_button, 0, wx.ALL | wx.EXPAND, 5)

		self.pause_button = wx.Button(panel, label=_("&Pausar"))
		self.pause_button.Disable()
		self.pause_button.Bind(wx.EVT_BUTTON, self.on_pause_recording)
		control_box.Add(self.pause_button, 0, wx.ALL | wx.EXPAND, 5)

		self.stop_button = wx.Button(panel, label=_("&Detener Grabación"))
		self.stop_button.Disable()
		self.stop_button.Bind(wx.EVT_BUTTON, self.stop_recording)
		control_box.Add(self.stop_button, 0, wx.ALL | wx.EXPAND, 5)

		self.cancel_button = wx.Button(panel, label=_("&Cancelar"))
		self.cancel_button.Disable()
		self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel_recording)
		control_box.Add(self.cancel_button, 0, wx.ALL | wx.EXPAND, 5)

		self.test_audio_button = wx.Button(panel, label=_("&Prueba de Audio"))
		self.test_audio_button.Bind(wx.EVT_BUTTON, self.show_test_audio)
		control_box.Add(self.test_audio_button, 0, wx.ALL | wx.EXPAND, 5)

		self.menu_button = wx.Button(panel, label=_("&Menú"))
		self.menu_button.Bind(wx.EVT_BUTTON, self.on_menu_button)
		control_box.Add(self.menu_button, 0, wx.ALL | wx.EXPAND, 5)

		main_sizer.Add(control_box, 0, wx.ALL | wx.CENTER, 10)
		main_sizer.Add(wx.StaticLine(panel), 0, wx.ALL | wx.EXPAND, 10)

		cfg = load_hotkeys_from_config()
		hotkey_start = cfg["hotkey_start"]
		initial_text = _("En espera (Usa {hk} para iniciar)").format(hk=hotkey_start)

		status_box = wx.StaticBoxSizer(wx.StaticBox(panel, label=_("Estado")), wx.VERTICAL)
		self.status_box = wx.TextCtrl(panel, value=initial_text,
			style=wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY)
		status_box.Add(self.status_box, 1, wx.ALL | wx.EXPAND, 5)
		main_sizer.Add(status_box, 1, wx.ALL | wx.EXPAND, 10)

		panel.SetSizer(main_sizer)
		main_sizer.Fit(self)
		self.SetMinSize(self.GetSize())
		self.Centre()

		self.tray_icon = MyTaskBarIcon(self)
		self.tray_icon.hide_icon()

		self.Bind(wx.EVT_CLOSE, self.on_close)
		self.Bind(wx.EVT_ICONIZE, self.on_iconify)
		self.Bind(wx.EVT_HOTKEY, self.on_hotkey)

		self.load_config()
		self.validate_and_register_hotkeys()
		self.update_status_message(recording=False)

		logger.log_action("Interfaz gráfica inicializada correctamente.")
		logger.log_action(f"DEBUG: output_dir => {self.output_dir}")

	def _create_icon_from_base64(self, icon_b64):
		"""
		Crea el ícono de la ventana principal a partir de datos Base64.

		:param icon_b64: Cadena Base64 con la imagen del ícono.
		:return: Objeto wx.Icon, o ícono por defecto en caso de error.
		"""
		try:
			icon_bytes = base64.b64decode(icon_b64)
			stream = io.BytesIO(icon_bytes)
			icon_image = wx.Image(stream, wx.BITMAP_TYPE_PNG)
			bitmap = wx.Bitmap(icon_image)
			icon = wx.Icon()
			icon.CopyFromBitmap(bitmap)
			logger.log_action("Icono creado desde base64 exitosamente.")
			return icon
		except Exception as e:
			logger.log_error(f"Error al crear icono desde base64: {e}")
			return wx.Icon()

	def on_iconify(self, event):
		"""
		Maneja el evento de minimizar la ventana, revisa si se debe ocultar a la bandeja.

		:param event: Evento wx.EVT_ICONIZE.
		"""
		config = load_config(self.CONFIG_FILE)
		minimize_to_tray = config.get("minimize_to_tray", False)
		if event.IsIconized() and minimize_to_tray:
			self.Hide()
			self.tray_icon.show_icon()
			logger.log_action("Aplicación minimizada a la bandeja.")
		else:
			event.Skip()

	def on_hotkey(self, event):
		"""
		Maneja eventos de hotkeys globales.

		:param event: Evento wx.EVT_HOTKEY.
		"""
		hotkey_id = event.GetId()
		logger.log_action(f"Hotkey detectada con ID: {hotkey_id}")

		if hotkey_id == HOTKEY_ID_START:
			self.start_recording()
		elif hotkey_id == HOTKEY_ID_STOP:
			self.stop_recording()
		elif hotkey_id == HOTKEY_ID_PAUSE:
			self.on_pause_recording(None)
		elif hotkey_id == HOTKEY_ID_CANCEL:
			self.on_cancel_recording(None)

	def on_close(self, event):
		"""
		Maneja el evento de cierre de la aplicación.

		Si hay una grabación en curso, pregunta al usuario si desea detenerla.
		Si se está realizando una conversión, espera a que termine antes de cerrar.
		"""
		logger.log_action("Intento de cierre de la aplicación.")
		if self.recording_event.is_set():
			resp = mensaje(
				None,
				_("Hay una grabación en curso. ¿Desea detenerla y salir?"),
				_("Confirmar cierre"),
				wx.YES_NO | wx.ICON_WARNING
			)
			logger.log_action("Confirmación de cierre solicitada al usuario.")
			if resp == wx.NO:
				if event:
					event.Veto()
				logger.log_action("Cierre de la aplicación cancelado por el usuario.")
				return
			else:
				self.want_to_close = True
				self.stop_recording(None)
		else:
			if hasattr(self, "conversion_thread") and self.conversion_thread.is_alive():
				logger.log_action("Conversión en curso al intentar cerrar la aplicación.")
				wait_dlg = PleaseWaitDialog(self, _("Por favor espere, finalizando conversión..."))
				wait_dlg.Show()
				while self.conversion_thread.is_alive():
					wx.Yield()
					time.sleep(0.1)
				wait_dlg.stop_tone()
				wait_dlg.Destroy()
				logger.log_action("Conversión finalizada durante el cierre de la aplicación.")
			self.final_close()

	def final_close(self):
		"""
		Ejecución final de cierre: Desregistra hotkeys, oculta y destruye el ícono de bandeja,
		guarda la configuración y destruye la ventana.
		"""
		try:
			self.UnregisterHotKey(HOTKEY_ID_START)
			self.UnregisterHotKey(HOTKEY_ID_STOP)
			self.UnregisterHotKey(HOTKEY_ID_PAUSE)
			self.UnregisterHotKey(HOTKEY_ID_CANCEL)
			logger.log_action("Hotkeys globales desregistradas.")
		except Exception as e:
			logger.log_error(f"Error al desregistrar hotkeys: {e}")

		if hasattr(self, "tray_icon"):
			self.tray_icon.hide_icon()
			self.tray_icon.Destroy()
			logger.log_action("Icono de la bandeja ocultado y destruido.")

		self.save_config_wrapper()
		logger.log_action("Configuración guardada antes del cierre.")
		self.Destroy()
		logger.log_action("Aplicación cerrada exitosamente.")

	def on_refresh_devices(self, event):
		"""
		Refresca la lista de dispositivos disponibles para micrófono y sistema,
		y actualiza el cuadro de estado.

		:param event: Evento de botón "Refrescar Dispositivos".
		"""
		logger.log_action("Actualizando lista de dispositivos.")
		refresh_devices(self.mic_choice, self.system_choice, self.status_box)

	def on_update_selected_mic(self, event):
		"""
		Actualiza el micrófono seleccionado según la elección del usuario.

		:param event: Evento wx.EVT_CHOICE de mic_choice.
		"""
		selected_name = self.mic_choice.GetStringSelection()
		self.selected_mic = update_selected_mic(selected_name)
		logger.log_action(f"Micrófono seleccionado: {selected_name}")

	def on_update_selected_system(self, event):
		"""
		Actualiza el dispositivo de sistema (loopback) seleccionado.

		:param event: Evento wx.EVT_CHOICE de system_choice.
		"""
		selected_name = self.system_choice.GetStringSelection()
		self.selected_system = update_selected_system(selected_name)
		logger.log_action(f"Sistema (loopback) seleccionado: {selected_name}")

	def on_update_quality(self, event):
		"""
		Actualiza la calidad (sample_rate) seleccionada.

		:param event: Evento wx.EVT_CHOICE de quality_choice.
		"""
		self.selected_quality = update_quality(self.quality_choice)
		self.sample_rate = self.selected_quality
		logger.log_action(f"Calidad de grabación actualizada a: {self.selected_quality} Hz")

	def on_update_output_format(self, event):
		"""
		Actualiza el formato de salida seleccionado (MP3, WAV, etc.).

		:param event: Evento wx.EVT_CHOICE de format_choice.
		"""
		self.selected_format = update_output_format(self.format_choice)
		logger.log_action(f"Formato de salida actualizado a: {self.selected_format}")

	def on_update_bitrate(self, event):
		"""
		Actualiza el bitrate de MP3 seleccionado.

		:param event: Evento wx.EVT_CHOICE de bitrate_choice.
		"""
		self.selected_bitrate = update_bitrate(self.bitrate_choice)
		logger.log_action(f"Bitrate MP3 actualizado a: {self.selected_bitrate} kbps")

	def on_update_mic_volume(self, event):
		"""
		Actualiza el volumen del micrófono (slider) y registra la acción.

		:param event: Evento wx.EVT_SLIDER de mic_volume_slider.
		"""
		self.mic_volume = update_mic_volume(self.mic_volume_slider)
		logger.log_action(f"Volumen del micrófono actualizado a: {self.mic_volume * 100}%")

	def on_update_system_volume(self, event):
		"""
		Actualiza el volumen del sistema (slider).

		:param event: Evento wx.EVT_SLIDER de system_volume_slider.
		"""
		self.system_volume = update_system_volume(self.system_volume_slider)
		logger.log_action(f"Volumen del sistema actualizado a: {self.system_volume * 100}%")

	def on_update_mic_mode(self, event):
		"""
		Actualiza el modo de micrófono (Mono/Estéreo) seleccionado.

		:param event: Evento wx.EVT_CHOICE de mic_mode_choice.
		"""
		self.mic_mode = self.mic_mode_choice.GetStringSelection()
		logger.log_action(f"Modo de micrófono actualizado a: {self.mic_mode}")

	def on_update_system_mode(self, event):
		"""
		Actualiza el modo del sistema (Mono/Estéreo) seleccionado.

		:param event: Evento wx.EVT_CHOICE de system_mode_choice.
		"""
		self.system_mode = self.system_mode_choice.GetStringSelection()
		logger.log_action(f"Modo de sistema actualizado a: {self.system_mode}")

	def on_update_buffer_size(self, event):
		"""
		Actualiza el tamaño de buffer para la grabación.

		:param event: Evento wx.EVT_SPINCTRL de buffer_spin.
		"""
		self.buffer_size = self.buffer_spin.GetValue()
		logger.log_action(f"Tamaño de buffer actualizado a: {self.buffer_size} frames")

	def toggle_controls(self, enable):
		"""
		Habilita o deshabilita los controles principales de la interfaz.

		:param enable: Booleano que indica si se habilitan (True) o deshabilitan (False).
		"""
		self.mic_choice.Enable(enable)
		self.system_choice.Enable(enable)
		self.quality_choice.Enable(enable)
		self.format_choice.Enable(enable)
		self.bitrate_choice.Enable(enable)
		self.mic_mode_choice.Enable(enable)
		self.system_mode_choice.Enable(enable)
		self.buffer_spin.Enable(enable)
		self.separate_files_checkbox.Enable(enable)
		self.start_button.Enable(enable)
		self.refresh_button.Enable(enable)
		self.test_audio_button.Enable(enable)
		logger.log_action(f"Controles {'habilitados' if enable else 'deshabilitados'}.")

	def start_recording(self, event=None):
		"""
		Inicia la grabación de audio si no hay otra en curso y no hay actualización pendiente.
		"""
		if self.is_update:
			logger.log_action("Grabación cancelada debido a una actualización en curso.")
			return

		if not self.recording_event.is_set():
			self.recording_event.set()
			self.pause_event.clear()
			self.cancel_event.clear()

			self.toggle_controls(False)
			self.pause_button.Enable()
			self.stop_button.Enable()
			self.cancel_button.Enable()
			self.stop_button.SetFocus()

			logger.log_action("Inicio de grabación de audio.")
			self.update_status_message(recording=True)
			winsound.Beep(1000, 200)

			self.separate_files = self.separate_files_checkbox.GetValue()
			final_channels = 2

			timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
			self.combined_output_path = os.path.abspath(os.path.join(self.output_dir, f"recording_{timestamp}.wav"))

			self.mic_output_path = (
				os.path.abspath(os.path.join(self.output_dir, f"recording_mic_{timestamp}.wav"))
				if self.separate_files
				else None
			)
			self.system_output_path = (
				os.path.abspath(os.path.join(self.output_dir, f"recording_system_{timestamp}.wav"))
				if self.separate_files
				else None
			)

			logger.log_action(f"DEBUG: combined_output_path => {self.combined_output_path}")
			if self.mic_output_path:
				logger.log_action(f"DEBUG: mic_output_path => {self.mic_output_path}")
			if self.system_output_path:
				logger.log_action(f"DEBUG: system_output_path => {self.system_output_path}")

			self.recording_thread = Thread(
				target=record_audio,
				args=(
					self.recording_event,
					self.selected_mic,
					self.selected_system,
					self.sample_rate,
					final_channels,
					self.output_dir,
					self.combined_output_path,
					self.mic_output_path,
					self.system_output_path,
					self.mic_volume,
					self.system_volume,
					self.mic_mode,
					self.system_mode,
					self.buffer_size,
					self.pause_event,
					self.cancel_event
				)
			)
			self.recording_thread.start()
			logger.log_action("Thread de grabación iniciado.")

	def on_pause_recording(self, event):
		"""
		Pausa o reanuda la grabación de audio según el estado actual.

		:param event: Evento de botón Pausar/Reanudar.
		"""
		if self.recording_event.is_set():
			if not self.pause_event.is_set():
				self.pause_event.set()
				self.pause_button.SetLabel(_("&Reanudar"))
				self.update_status_message(recording=True, paused=True)
				logger.log_action("Grabación pausada por el usuario.")
				winsound.Beep(700, 150)
			else:
				self.pause_event.clear()
				self.pause_button.SetLabel(_("&Pausar"))
				self.update_status_message(recording=True, paused=False)
				logger.log_action("Grabación reanudada por el usuario.")
				winsound.Beep(1400, 150)

	def on_cancel_recording(self, event):
		"""
		Cancela la grabación en curso y elimina los archivos generados.

		:param event: Evento de botón Cancelar.
		"""
		if self.recording_event.is_set():
			self.cancel_event.set()
			self.recording_event.clear()
			logger.log_action("Se ha pulsado 'Cancelar'. Grabación cancelada.")
			self.post_stop_actions()

	def stop_recording(self, event=None):
		"""
		Detiene la grabación en curso de manera normal (sin cancelar).

		:param event: Evento de botón Detener (opcional).
		"""
		if self.recording_event.is_set():
			self.recording_event.clear()
			logger.log_action("Detención de grabación solicitada.")
			self.post_stop_actions()

	def post_stop_actions(self):
		"""
		Acciones posteriores a detener/cancelar la grabación:
		- Deshabilitar botones de pausa/cancelar.
		- Habilitar controles principales.
		- Realizar conversión de formato si no se canceló.
		"""
		self.pause_event.clear()
		self.pause_button.SetLabel(_("&Pausar"))
		self.pause_button.Disable()
		self.cancel_button.Disable()

		self.toggle_controls(True)
		self.stop_button.Disable()
		self.start_button.SetFocus()

		self.update_status_message(recording=False)
		winsound.Beep(500, 200)

		if self.recording_thread:
			self.recording_thread.join()
			logger.log_action("Thread de grabación finalizado.")

		if self.cancel_event.is_set():
			if self.want_to_close:
				self.final_close()
			else:
				self.show_info_message(_("Grabación cancelada. Se han eliminado los archivos."), _("Grabación"))
			return

		# Grabación no cancelada => conversión si es distinto de WAV
		if self.selected_format != "WAV":
			self.dialog = PleaseWaitDialog(self, _("Por favor espere, convirtiendo a formato final..."))
			self.dialog.Show()
			logger.log_action("Diálogo de espera para conversión mostrado.")

			self.conversion_thread = ConversionThread(
				self,
				self.combined_output_path,
				self.selected_format,
				self.separate_files,
				self.mic_output_path,
				self.system_output_path
			)
			self.conversion_thread.start()
			logger.log_action("Thread de conversión iniciado.")

			self.timer = wx.Timer(self)
			self.Bind(wx.EVT_TIMER, self.on_conversion_check, self.timer)
			self.timer.Start(500)
		else:
			self.after_recording_completed()

	def after_recording_completed(self):
		"""
		Acciones tras completarse la grabación y/o conversión:
		Muestra un diálogo preguntando si se desea abrir la carpeta de grabaciones.
		Si se cierra la aplicación, procede con final_close().
		"""
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

		message += _("\n\n¿Desea abrir la carpeta de grabaciones?")

		resp = mensaje(None, message, _("Grabación"), style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		logger.log_action("Mensaje de grabación completada con opción de abrir carpeta mostrado al usuario.")

		if resp == wx.YES:
			self.open_recordings_directory(None)
			logger.log_action("El usuario eligió abrir la carpeta de grabaciones.")
		else:
			logger.log_action("El usuario eligió NO abrir la carpeta de grabaciones.")

		if self.want_to_close:
			self.final_close()

	def on_conversion_check(self, event):
		"""
		Verifica si el hilo de conversión ha terminado y maneja excepciones.

		:param event: Evento wx.EVT_TIMER.
		"""
		if not hasattr(self, "conversion_thread"):
			return
		if self.conversion_thread.is_alive():
			return

		self.timer.Stop()
		self.dialog.stop_tone()
		self.dialog.Destroy()
		logger.log_action("Diálogo de espera para conversión cerrado.")

		if self.conversion_thread.exception:
			error_message = f"Error al convertir el archivo: {self.conversion_thread.exception}"
			self.show_error_message(error_message)
			logger.log_error(error_message)
			if self.want_to_close:
				self.final_close()
		else:
			self.after_recording_completed()

	def convert_to_final_format(self, wav_path, target_format, separate_files, mic_path, system_path):
		"""
		Realiza la conversión de un archivo WAV a otro formato (MP3, FLAC, etc.).
		Si están separados, convierte también micrófono y sistema.

		:param wav_path: Ruta del archivo WAV combinado.
		:param target_format: Formato de salida (MP3, WAV, etc.).
		:param separate_files: Indica si hay archivos separados de mic y sistema.
		:param mic_path: Ruta del archivo WAV de micrófono.
		:param system_path: Ruta del archivo WAV de sistema.
		:return: Ruta final del archivo convertido.
		"""
		try:
			logger.log_action(f"Iniciando convert_to_final_format() desde {wav_path} a {target_format}")
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
			logger.log_action(f"Conversión finalizada en convert_to_final_format: {final_path}")
			return final_path
		except Exception as e:
			logger.log_error(f"Error en convert_to_final_format: {e}")
			raise

	def save_as_mp3(self, wav_file_path):
		"""
		Convierte un archivo WAV a MP3 utilizando la librería `lameenc`.

		:param wav_file_path: Ruta del archivo WAV a convertir.
		:return: Ruta del archivo MP3 generado.
		"""
		try:
			import lameenc
			data, samplerate = sf.read(wav_file_path)

			channels = data.shape[1] if len(data.shape) > 1 else 1

			encoder = lameenc.Encoder()
			encoder.set_bit_rate(self.selected_bitrate)
			encoder.set_in_sample_rate(samplerate)
			encoder.set_channels(channels)
			encoder.set_quality(2)

			data_int16 = (data * 32767).astype(np.int16).tobytes()
			mp3_data = encoder.encode(data_int16) + encoder.flush()

			mp3_path = wav_file_path.replace(".wav", ".mp3")
			with open(mp3_path, "wb") as mp3_file:
				mp3_file.write(mp3_data)

			os.remove(wav_file_path)
			logger.log_action(f"Archivo convertido a MP3 y borrado WAV original: {mp3_path}")
			return mp3_path
		except Exception as e:
			logger.log_error(f"Error al convertir a MP3: {e}")
			raise

	def save_as_format(self, wav_file_path, target_format):
		"""
		Convierte un archivo WAV a un formato soportado por `soundfile` (FLAC, OGG, AIFF...).

		:param wav_file_path: Ruta del archivo WAV a convertir.
		:param target_format: Formato de salida (FLAC, OGG, AIFF, etc.).
		:return: Ruta final del archivo convertido.
		"""
		try:
			data, samplerate = sf.read(wav_file_path)
			out_path = wav_file_path.replace(".wav", f".{target_format.lower()}")
			sf.write(out_path, data, samplerate, format=target_format)
			os.remove(wav_file_path)
			logger.log_action(f"Archivo convertido a {target_format} y borrado WAV original: {out_path}")
			return out_path
		except Exception as e:
			logger.log_error(f"Error al convertir a {target_format}: {e}")
			raise

	def show_error_message(self, message, title=_("Error")):
		"""
		Muestra un mensaje de error en un cuadro de diálogo.

		:param message: Texto del error.
		:param title: Título del cuadro de diálogo.
		"""
		mensaje(None, message, title, style=wx.OK | wx.ICON_ERROR)
		logger.log_error(f"Mensaje de error mostrado al usuario: {message}")

	def show_info_message(self, message, title=_("Información")):
		"""
		Muestra un mensaje informativo en un cuadro de diálogo.

		:param message: Texto informativo.
		:param title: Título del cuadro de diálogo.
		"""
		mensaje(None, message, title, style=wx.OK | wx.ICON_INFORMATION)
		logger.log_action(f"Mensaje de información mostrado al usuario: {message}")

	def save_config_wrapper(self):
		"""
		Guarda la configuración actual de la aplicación en WASAPIRecording.dat.
		"""
		try:
			config_file = os.path.abspath(os.path.join(get_base_path(), "WASAPIRecording.dat"))
			config = load_config(config_file)

			config["mic_name"] = self.selected_mic.name if self.selected_mic else ""
			config["system_name"] = self.selected_system.name if self.selected_system else ""
			config["quality"] = self.sample_rate
			config["format"] = self.selected_format
			config["bitrate"] = self.selected_bitrate
			config["mic_volume"] = self.mic_volume_slider.GetValue()
			config["system_volume"] = self.system_volume_slider.GetValue()
			config["mic_mode"] = self.mic_mode_choice.GetStringSelection()
			config["system_mode"] = self.system_mode_choice.GetStringSelection()
			config["separate_files"] = self.separate_files_checkbox.GetValue()
			config["buffer_size"] = self.buffer_size

			config["recording_dir"] = self.output_dir

			save_config(config_file, config)
			logger.log_action("Configuración guardada exitosamente.")
			self.get.lang.set_language(self.get.lang.current_lang)
		except Exception as e:
			logger.log_error(f"Error al guardar la configuración: {e}")

	def load_config(self):
		"""
		Carga la configuración desde WASAPIRecording.dat y ajusta
		los controles de la interfaz en consecuencia.
		"""
		try:
			config = load_config(self.CONFIG_FILE)
			logger.log_action("Configuración cargada exitosamente.")

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
				logger.log_warning(f"Micrófono configurado no encontrado: {mic_name}. Se usa el predeterminado.")

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
				logger.log_warning(f"Sistema configurado no encontrado: {system_name}. Se usa el predeterminado.")

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

			mic_mode_ = config.get("mic_mode", _("Estéreo"))
			if mic_mode_ in [_("Mono"), _("Estéreo")]:
				self.mic_mode_choice.SetStringSelection(mic_mode_)
				self.mic_mode = mic_mode_

			sys_mode_ = config.get("system_mode", _("Estéreo"))
			if sys_mode_ in [_("Mono"), _("Estéreo")]:
				self.system_mode_choice.SetStringSelection(sys_mode_)
				self.system_mode = sys_mode_

			self.separate_files_checkbox.SetValue(config.get("separate_files", False))

			self.buffer_size = config.get("buffer_size", self.buffer_size)
			self.buffer_spin.SetValue(self.buffer_size)

			user_dir = config.get("recording_dir", "")
			default_dir = os.path.abspath(os.path.join(get_base_path(), "recording"))
			if user_dir:
				self.output_dir = user_dir
				logger.log_action(f"Directorio de grabaciones cargado desde config: {user_dir}")
			else:
				self.output_dir = default_dir
				logger.log_action(f"Directorio de grabaciones por defecto: {self.output_dir}")

		except Exception as e:
			logger.log_error(f"Error al cargar la configuración: {e}")

	def show_test_audio(self, event):
		"""
		Abre el diálogo de prueba de audio, utilizando la misma lógica de grabación
		para verificar la configuración actual.

		:param event: Evento de botón "Prueba de Audio".
		"""
		from ui.test_audio import TestAudioDialog
		separate_files_value = self.separate_files_checkbox.GetValue()

		mic_vol_slider_val = self.mic_volume_slider.GetValue()
		mic_volume = mic_vol_slider_val / 100.0
		system_vol_slider_val = self.system_volume_slider.GetValue()
		system_volume = system_vol_slider_val / 100.0

		final_channels = 2

		mic_index = self.mic_choice.GetSelection()
		mic_name = self.mic_choice.GetString(mic_index)
		selected_mic = update_selected_mic(mic_name)

		system_index = self.system_choice.GetSelection()
		system_name = self.system_choice.GetString(system_index)
		selected_system = update_selected_system(system_name)

		buffer_size = self.buffer_spin.GetValue()

		dlg = TestAudioDialog(
			parent=self,
			selected_mic=selected_mic,
			selected_system=selected_system,
			sample_rate=self.sample_rate,
			final_channels=final_channels,
			separate_files=separate_files_value,
			mic_volume=mic_volume,
			system_volume=system_volume,
			mic_mode=self.mic_mode_choice.GetStringSelection(),
			system_mode=self.system_mode_choice.GetStringSelection(),
			buffer_size=buffer_size
		)
		dlg.ShowModal()
		dlg.Destroy()
		logger.log_action("Prueba de audio iniciada por el usuario.")

	def on_menu_button(self, event):
		"""
		Muestra un menú principal con opciones de:
		- Cambiar idioma.
		- Buscar actualizaciones.
		- Abrir carpeta de grabaciones.
		- Manual de usuario.
		- Acerca de...
		- Donar.
		- Salir.

		Si hay grabación en curso, muestra un menú simplificado.
		"""
		menu = wx.Menu()
		submenu_idiomas = wx.Menu()
		if not self.recording_event.is_set():
			item_de = submenu_idiomas.AppendRadioItem(-1, _("Alemán"))
			item_ar = submenu_idiomas.AppendRadioItem(-1, _("Árabe"))
			item_es = submenu_idiomas.AppendRadioItem(-1, _("Español"))
			item_fr = submenu_idiomas.AppendRadioItem(-1, _("Francés"))
			item_en = submenu_idiomas.AppendRadioItem(-1, _("Inglés"))
			item_it = submenu_idiomas.AppendRadioItem(-1, _("Italiano"))
			item_pt = submenu_idiomas.AppendRadioItem(-1, _("Portugués"))
			item_tr = submenu_idiomas.AppendRadioItem(-1, _("Turco"))
			item_vi = submenu_idiomas.AppendRadioItem(-1, _("Vietnamita"))

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
			elif current_language == "ar":
				item_ar.Check(True)
			elif current_language == "vi":
				item_vi.Check(True)

			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('es'), item_es)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('en'), item_en)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('fr'), item_fr)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('it'), item_it)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('de'), item_de)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('pt'), item_pt)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('tr'), item_tr)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('ar'), item_ar)
			self.Bind(wx.EVT_MENU, lambda e: self.cambiar_idioma('vi'), item_vi)

			item_opciones = menu.Append(-1, _("Opciones"))
			item_actualizar = menu.Append(-1, _("Buscar actualizaciones"))
			menu.AppendSubMenu(submenu_idiomas, _("Idioma"))
			item_abrir = menu.Append(-1, _("Abrir Grabaciones"))
			item_manual = menu.Append(-1, _("&Manual de usuario"))
			item_acerca = menu.Append(-1, _("Acerca &de..."))
			item_donar = menu.Append(-1, _("invítame a un &café si te gusta mi trabajo"))
			item_cerrar = menu.Append(-1, _("Salir"))

			self.Bind(wx.EVT_MENU, self.show_options_dialog, item_opciones)
			self.Bind(wx.EVT_MENU, self.on_update_app, item_actualizar)
			self.Bind(wx.EVT_MENU, self.open_recordings_directory, item_abrir)
			self.Bind(wx.EVT_MENU, self.on_show_manual, item_manual)
			self.Bind(wx.EVT_MENU, self.show_about, item_acerca)
			self.Bind(wx.EVT_MENU, self.on_donar, item_donar)
			self.Bind(wx.EVT_MENU, self.on_close, item_cerrar)
			logger.log_action("Menú principal mostrado y opciones vinculadas.")
		else:
			item_abrir = menu.Append(-1, _("Abrir Grabaciones"))
			item_donar = menu.Append(-1, _("&invítame a un café si te gusta mi trabajo"))
			item_cerrar = menu.Append(-1, _("Cerrar"))
			self.Bind(wx.EVT_MENU, self.open_recordings_directory, item_abrir)
			self.Bind(wx.EVT_MENU, self.on_donar, item_donar)
			self.Bind(wx.EVT_MENU, self.on_close, item_cerrar)
			logger.log_action("Menú simplificado mostrado mientras hay una grabación en curso.")

		self.PopupMenu(menu)
		menu.Destroy()

	def cambiar_idioma(self, nuevo_idioma):
		"""
		Cambia el idioma de la aplicación y solicita reiniciar si el usuario confirma.

		:param nuevo_idioma: Código ISO del idioma a utilizar (ej. 'es', 'en').
		"""
		if nuevo_idioma != self.get.lang.current_lang:
			msg = _("Para aplicar el nuevo idioma se necesita reiniciar la aplicación.\n¿Desea continuar?")
			res = mensaje(None, msg, _("Confirmar cambio de idioma"), wx.YES_NO | wx.ICON_QUESTION)
			logger.log_action(f"Usuario eligió cambiar el idioma a: {nuevo_idioma}")
			if res == wx.YES:
				self.get.lang.set_language(nuevo_idioma)
				logger.log_action(f"Idioma cambiado a: {nuevo_idioma}. Reiniciando aplicación.")
				self.restart_app()
			else:
				logger.log_action("Cambio de idioma cancelado por el usuario.")

	def restart_app(self):
		"""
		Cierra la aplicación y la reinicia con los mismos parámetros de ejecución.
		"""
		try:
			self.Close()
			logger.log_action("Aplicación cerrada para reinicio.")

			args = sys.argv[:]
			if hasattr(sys, '_MEIPASS'):
				executable = sys.executable
			else:
				executable = sys.executable
				args.insert(0, executable)

			if sys.platform == 'win32':
				args = ['"%s"' % arg for arg in args]

			os.execv(executable, args)
			logger.log_action("Aplicación reiniciada exitosamente.")
		except Exception as e:
			error_message = f"Error al intentar reiniciar la aplicación: {e}"
			self.show_error_message(error_message)
			logger.log_error(error_message)

	def show_options_dialog(self, event):
		"""
		Muestra el diálogo de opciones, donde se configuran:
		- Ajustes generales (minimizar a bandeja, carpeta de grabaciones).
		- Hotkeys de inicio, pausa, detener, cancelar.

		:param event: Evento de menú asociado.
		"""
		from ui.options import OptionsDialog
		dlg = OptionsDialog(self)
		if dlg.ShowModal() == wx.ID_OK:
			general_changed, keyboard_changed = dlg.save_all_settings2()
			if general_changed:
				logger.log_action("Configuraciones generales actualizadas desde el diálogo de opciones.")
				new_cfg = load_config(self.CONFIG_FILE)
				possible_dir = new_cfg.get("recording_dir", "")
				default_dir = os.path.abspath(os.path.join(get_base_path(), "recording"))
				self.output_dir = possible_dir if possible_dir else default_dir
				logger.log_action(f"Directorio de grabaciones actualizado (opciones): {self.output_dir}")

			if keyboard_changed:
				self.validate_and_register_hotkeys()
				self.update_status_message(recording=self.recording_event.is_set())
				logger.log_action("Hotkeys actualizadas desde el diálogo de opciones.")
		dlg.Destroy()

	def validate_and_register_hotkeys(self):
		"""
		Desregistra y vuelve a registrar las hotkeys globales según la configuración actual,
		asignando "Sin asignar" a las que no se puedan registrar.
		"""
		try:
			self.UnregisterHotKey(HOTKEY_ID_START)
			self.UnregisterHotKey(HOTKEY_ID_STOP)
			self.UnregisterHotKey(HOTKEY_ID_PAUSE)
			self.UnregisterHotKey(HOTKEY_ID_CANCEL)
			logger.log_action("Hotkeys globales desregistradas para actualización.")
		except Exception as e:
			logger.log_error(f"Error al desregistrar hotkeys: {e}")

		cfg = load_hotkeys_from_config()
		changed = False

		if cfg["hotkey_start"] != "Sin asignar":
			mod_s, code_s = parse_hotkey(cfg["hotkey_start"])
			if not self.RegisterHotKey(HOTKEY_ID_START, mod_s, code_s):
				cfg["hotkey_start"] = "Sin asignar"
				changed = True
				logger.log_warning(f"No se pudo registrar la hotkey de inicio: {cfg['hotkey_start']}")

		if cfg["hotkey_stop"] != "Sin asignar":
			mod_p, code_p = parse_hotkey(cfg["hotkey_stop"])
			if not self.RegisterHotKey(HOTKEY_ID_STOP, mod_p, code_p):
				cfg["hotkey_stop"] = "Sin asignar"
				changed = True
				logger.log_warning(f"No se pudo registrar la hotkey de detención: {cfg['hotkey_stop']}")

		if cfg["hotkey_pause"] != "Sin asignar":
			mod_h, code_h = parse_hotkey(cfg["hotkey_pause"])
			if not self.RegisterHotKey(HOTKEY_ID_PAUSE, mod_h, code_h):
				cfg["hotkey_pause"] = "Sin asignar"
				changed = True
				logger.log_warning(f"No se pudo registrar la hotkey de pausa: {cfg['hotkey_pause']}")

		if cfg["hotkey_cancel"] != "Sin asignar":
			mod_c, code_c = parse_hotkey(cfg["hotkey_cancel"])
			if not self.RegisterHotKey(HOTKEY_ID_CANCEL, mod_c, code_c):
				cfg["hotkey_cancel"] = "Sin asignar"
				changed = True
				logger.log_warning(f"No se pudo registrar la hotkey de cancelar: {cfg['hotkey_cancel']}")

		if changed:
			save_hotkeys_to_config(
				cfg["hotkey_start"],
				cfg["hotkey_stop"],
				cfg["hotkey_pause"],
				cfg["hotkey_cancel"]
			)
			logger.log_action("Hotkeys actualizadas en la configuración debido a fallos de registro.")
		else:
			logger.log_action("Hotkeys registradas exitosamente.")

	def update_status_message(self, recording=False, paused=False):
		"""
		Actualiza el cuadro de estado de la interfaz, mostrando
		el estado actual de grabación o pausa, así como las hotkeys disponibles.

		:param recording: Indica si se está grabando.
		:param paused: Indica si está en pausa.
		"""
		cfg = load_hotkeys_from_config()
		hotkey_start = cfg["hotkey_start"]
		hotkey_stop = cfg["hotkey_stop"]
		hotkey_pause = cfg["hotkey_pause"]

		if recording:
			if paused:
				self.status_box.SetValue(_("Grabación en pausa."))
				logger.log_action("Estado actualizado a: Grabación en pausa.")
			else:
				if hotkey_stop == "Sin asignar":
					self.status_box.SetValue(_("Grabando... (No hay hotkey de detener asignada)"))
				else:
					self.status_box.SetValue(_("Grabando... (Usa {hk} para detener)").format(hk=hotkey_stop))
				logger.log_action("Estado actualizado a: Grabando.")
		else:
			if hotkey_start == "Sin asignar":
				self.status_box.SetValue(_("En espera. Asigna teclas en Opciones o inicia manualmente."))
			else:
				self.status_box.SetValue(_("En espera (Usa {hk} para iniciar)").format(hk=hotkey_start))
			logger.log_action("Estado actualizado a: En espera.")

	def on_donar(self, event):
		"""
		Abre la página de donaciones en el navegador.

		:param event: Evento de menú asociado.
		"""
		wx.LaunchDefaultBrowser("https://paypal.me/hjbcdonaciones")
		logger.log_action("Usuario abrió la página de donaciones.")

	def on_show_manual(self, event):
		"""
		Muestra el manual de usuario en un diálogo especial.

		:param event: Evento de menú asociado.
		"""
		dialogo = ManualDialog(self, _manual)
		dialogo.ShowModal()
		dialogo.Destroy()
		logger.log_action("Manual de usuario mostrado al usuario.")

	def on_update_app(self, event):
		"""
		Inicia el proceso de actualización buscando nuevas versiones en GitHub.

		:param event: Evento de menú asociado.
		"""
		self.is_update = True
		logger.log_action("Proceso de actualización iniciado por el usuario.")
		dialog = UpdateDialog(None, "hxebolax", "WASAPIRecording", _version)
		dialog.ShowModal()
		dialog.Destroy()
		logger.log_action("Proceso de actualización finalizado.")
		self.is_update = False

	def open_recordings_directory(self, event):
		"""
		Abre la carpeta de grabaciones en el explorador de archivos.

		:param event: Evento de menú o diálogo.
		"""
		try:
			if not os.path.exists(self.output_dir):
				os.makedirs(self.output_dir)
				logger.log_action(f"Directorio de grabaciones creado: {self.output_dir}")
			os.startfile(self.output_dir)
			logger.log_action(f"Directorio de grabaciones abierto: {self.output_dir}")
		except Exception as e:
			error_message = _("No se pudo abrir el directorio de grabaciones: {error}").format(error=e)
			self.show_error_message(error_message)
			logger.log_error(f"Error al abrir el directorio de grabaciones: {e}")

	def show_about(self, event):
		"""
		Muestra un cuadro de diálogo "Acerca de..." con la versión, el autor y los traductores.

		:param event: Evento de menú asociado.
		"""
		msg = _("""WASAPIRecording
Versión: {}
Creado por: {}
Copyright © 2025

Traductores:
🇹🇷 Turco: Umut Korkmaz
🇸🇦 Árabe: moataz geba
🇮🇹 Italiano: Alessio Lenzi
🇻🇳 Vietnamita: Đào Đức Trung""").format(_version, _nombre)
		self.show_info_message(msg, _("Acerca de..."))
		logger.log_action("Información 'Acerca de' mostrada al usuario.")

