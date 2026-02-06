#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Diálogo de prueba de audio.

Permite grabar unos segundos de prueba con la misma lógica usada por la aplicación,
y reproducir la grabación resultante para verificar dispositivos y configuraciones.
Puede guardar archivos temporales de micrófono y sistema por separado si así se selecciona.
"""

import os
import wx
import tempfile
import winsound
import time
from threading import Thread, Event
import soundfile as sf
from core.recorder import record_audio
from ui.widgets import mensaje
from core.logger import Logger
from core.utils import get_base_path
import numpy as np

logger = Logger(log_dir=os.path.abspath(os.path.join(get_base_path(), "logs")))

class TestAudioDialog(wx.Dialog):
	"""
	Diálogo para grabar una prueba de audio y luego reproducirla para verificar la configuración.
	"""
	def __init__(
		self,
		parent,
		selected_mic,
		selected_system,
		sample_rate,
		final_channels,
		separate_files,
		mic_volume,
		system_volume,
		mic_mode="Estéreo",
		system_mode="Estéreo",
		buffer_size=1024
	):
		"""
		Constructor del TestAudioDialog.

		:param parent: Ventana padre.
		:param selected_mic: Dispositivo de micrófono seleccionado.
		:param selected_system: Dispositivo de loopback seleccionado.
		:param sample_rate: Tasa de muestreo.
		:param final_channels: Cantidad de canales finales (normalmente 2).
		:param separate_files: Indica si se grabarán archivos separados de micrófono y sistema.
		:param mic_volume: Volumen del micrófono (0.0 a 1.0).
		:param system_volume: Volumen del sistema (0.0 a 1.0).
		:param mic_mode: "Mono" o "Estéreo" para el micrófono.
		:param system_mode: "Mono" o "Estéreo" para el sistema.
		:param buffer_size: Tamaño del buffer de grabación.
		"""
		super().__init__(parent, title=_("Prueba de Audio"), style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)
		self.SetWindowStyleFlag(
			self.GetWindowStyleFlag()
			& ~wx.CLOSE_BOX
			& ~wx.MAXIMIZE_BOX
			& ~wx.MINIMIZE_BOX
			& ~wx.SYSTEM_MENU
		)
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)

		self.parent = parent
		self.selected_mic = selected_mic
		self.selected_system = selected_system
		self.sample_rate = sample_rate
		self.final_channels = final_channels
		self.separate_files = separate_files
		self.mic_volume = mic_volume
		self.system_volume = system_volume
		self.mic_mode = mic_mode
		self.system_mode = system_mode
		self.buffer_size = buffer_size

		self.is_recording = False
		self.is_recorded = False
		self.is_playing = False

		self.recording_event = Event()
		self.pause_event = Event()
		self.cancel_event = Event()

		self.recording_thread = None
		self.playback_timer = None
		self.playback_length_ms = 0

		self.temp_dir = tempfile.gettempdir()
		timestamp = time.strftime("%Y%m%d-%H%M%S")
		self.temp_combined = os.path.abspath(os.path.join(self.temp_dir, f"test_both_{timestamp}.wav"))
		self.temp_mic = None
		self.temp_system = None
		if self.separate_files:
			self.temp_mic = os.path.abspath(os.path.join(self.temp_dir, f"test_mic_{timestamp}.wav"))
			self.temp_system = os.path.abspath(os.path.join(self.temp_dir, f"test_system_{timestamp}.wav"))

		logger.log_action(
			f"DEBUG TestAudioDialog - Rutas temporales:\n - combined: {self.temp_combined}\n"
			f" - mic: {self.temp_mic}\n - system: {self.temp_system}"
		)

		main_sizer = wx.BoxSizer(wx.VERTICAL)

		self.info_label = wx.StaticText(self, label=_("&Información:"))
		self.info_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
		self.info_text.SetMinSize((450, 200))

		main_sizer.Add(self.info_label, 0, wx.ALL | wx.EXPAND, 10)
		main_sizer.Add(self.info_text, 0, wx.ALL | wx.EXPAND, 10)
		self._set_explanation_text()

		hbox = wx.BoxSizer(wx.HORIZONTAL)

		self.choice_label = None
		self.choice_play = None
		if self.separate_files:
			self.choice_label = wx.StaticText(self, label=_("&Selecciona qué archivo reproducir:"))
			self.choice_play = wx.Choice(self, choices=[_("Prueba micrófono"), _("Prueba sistema"), _("Ambos")])
			self.choice_play.SetSelection(2)
			self.choice_label.Hide()
			self.choice_play.Hide()
			hbox.Add(self.choice_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
			hbox.Add(self.choice_play, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

		self.main_button = wx.Button(self, label=_("&Detener"))
		self.main_button.Bind(wx.EVT_BUTTON, self.on_main_button)
		hbox.Add(self.main_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

		self.close_button = wx.Button(self, label=_("&Cerrar"))
		self.close_button.Bind(wx.EVT_BUTTON, self.on_close_dialog)
		hbox.Add(self.close_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)

		main_sizer.Add(hbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
		self.SetSizerAndFit(main_sizer)
		self.Centre()

		self.start_recording()

	def on_key_down(self, event):
		"""
		Bloquea Alt+F4 en el diálogo, impidiendo su cierre sin pulsar 'Cerrar'.

		:param event: Evento de teclado.
		"""
		key_code = event.GetKeyCode()
		if key_code == wx.WXK_F4 and event.AltDown():
			logger.log_action("TestAudioDialog: se intentó Alt+F4, bloqueado.")
			return
		event.Skip()

	def _set_explanation_text(self):
		"""
		Establece el texto explicativo en el cuadro de texto de información.
		"""
		explanation = _(
			"Esta ventana realiza una prueba de grabación y reproducción con los mismos ajustes.\n"
			"Al pulsar 'Detener', podrás luego 'Reproducir'. Si guardas archivos separados, podrás elegir "
			"micrófono, sistema o ambos.\n"
			"No se puede cerrar con Alt+F4 ni con la X; sólo con 'Cerrar'."
		)
		self.info_text.SetValue(explanation)

	def start_recording(self):
		"""
		Inicia la grabación de prueba, creando un hilo que use la misma lógica de 'record_audio'.
		"""
		self.is_recording = True
		self.is_recorded = False
		self.recording_event.set()
		logger.log_action("TestAudioDialog: Iniciando grabación de prueba...")

		self.recording_thread = Thread(
			target=record_audio,
			args=(
				self.recording_event,
				self.selected_mic,
				self.selected_system,
				self.sample_rate,
				self.final_channels,
				self.temp_dir,
				self.temp_combined,
				self.temp_mic,
				self.temp_system,
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

	def stop_recording(self):
		"""
		Detiene la grabación de prueba y marca el archivo resultante como listo para reproducir.
		"""
		if self.is_recording:
			self.recording_event.clear()
			self.recording_thread.join()
			self.is_recording = False
			self.is_recorded = True
			logger.log_action("TestAudioDialog: Grabación de prueba detenida.")

	def on_main_button(self, event):
		"""
		Maneja el botón principal que detiene la grabación o maneja la reproducción (Play/Stop).

		:param event: Evento de clic en el botón principal.
		"""
		if self.is_recording:
			self.stop_recording()
			self.main_button.SetLabel(_("Reproducir"))
			logger.log_action("Botón principal cambiado a 'Reproducir' tras detener grabación.")
			if self.separate_files and self.choice_label and self.choice_play:
				self.choice_label.Show()
				self.choice_play.Show()
				self.choice_play.SetSelection(2)
				self.Layout()
		elif not self.is_recording and not self.is_playing:
			self.start_playback()
			self.main_button.SetLabel(_("Detener"))
			logger.log_action("Reproducción iniciada. Botón principal cambiado a 'Detener'.")
		elif not self.is_recording and self.is_playing:
			self.stop_playback()
			self.main_button.SetLabel(_("Reproducir"))
			logger.log_action("Reproducción detenida. Botón principal cambiado a 'Reproducir'.")

	def start_playback(self):
		"""
		Inicia la reproducción del archivo (micrófono, sistema o ambos) según la configuración y
		configura un temporizador para detener el sonido al finalizar.
		"""
		if not self.is_recorded:
			mensaje(self, _("No se ha grabado nada aún."), _("Aviso"))
			return
		if self.is_playing:
			return

		to_play = self._get_file_to_play()
		if not to_play or not os.path.isfile(to_play):
			mensaje(self, _("No existe el archivo a reproducir"), _("Error"), style=wx.ICON_ERROR)
			logger.log_error("Archivo a reproducir no encontrado.")
			return

		duration_sec = self._get_wav_duration(to_play)
		self.playback_length_ms = int(duration_sec * 1000)

		try:
			winsound.PlaySound(to_play, winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.is_playing = True
			logger.log_action(f"Iniciando reproducción de: {to_play}")
		except Exception as e:
			mensaje(self, str(e), _("Error"), style=wx.ICON_ERROR)
			logger.log_error(f"Error al reproducir: {e}")
			return

		self.playback_timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.on_playback_timer, self.playback_timer)
		self.playback_timer.Start(self.playback_length_ms, oneShot=True)

	def stop_playback(self):
		"""
		Detiene la reproducción de sonido y, si hay un temporizador activo, lo detiene.
		"""
		winsound.PlaySound(None, winsound.SND_PURGE)
		self.is_playing = False
		if self.playback_timer and self.playback_timer.IsRunning():
			self.playback_timer.Stop()
			logger.log_action("Reproducción detenida manualmente.")

	def on_playback_timer(self, event):
		"""
		Se ejecuta cuando el temporizador de reproducción termina, para detener el sonido.

		:param event: Evento wx.EVT_TIMER.
		"""
		if self.is_playing:
			self.stop_playback()
			self.main_button.SetLabel(_("Reproducir"))
			logger.log_action("Reproducción finalizada por temporizador.")

	def on_close_dialog(self, event):
		"""
		Cierra el diálogo de prueba. Si la grabación sigue en curso, pregunta si cancelar.

		:param event: Evento de clic en botón 'Cerrar'.
		"""
		if self.is_recording:
			resp = mensaje(
				self,
				_("La grabación sigue en curso. ¿Deseas cancelar la prueba de sonido?"),
				_("Cancelar Prueba"),
				style=wx.YES_NO | wx.ICON_QUESTION
			)
			if resp == wx.YES:
				self.stop_recording()
				self.cleanup_temp_files()
				logger.log_action("Grabación de prueba cancelada por el usuario.")
				self.EndModal(wx.ID_OK)
			else:
				logger.log_action("Cierre del diálogo cancelado por el usuario (seguía grabando).")
				return
		else:
			self.stop_playback()
			self.cleanup_temp_files()
			logger.log_action("Cerrando TestAudioDialog tras finalizar grabación/reproducción.")
			self.EndModal(wx.ID_OK)

	def cleanup_temp_files(self):
		"""
		Elimina los archivos WAV temporales utilizados en la prueba.
		"""
		def remove_file_if_exists(path):
			if path and os.path.isfile(path):
				try:
					os.remove(path)
					logger.log_action(f"Archivo temporal eliminado: {path}")
				except Exception as e:
					logger.log_error(f"Error al eliminar archivo temporal {path}: {e}")

		remove_file_if_exists(self.temp_combined)
		remove_file_if_exists(self.temp_mic)
		remove_file_if_exists(self.temp_system)

	def _get_file_to_play(self):
		"""
		Determina qué archivo WAV reproducir: micrófono, sistema o ambos (combinado).

		:return: Ruta del archivo a reproducir.
		"""
		if self.separate_files and self.is_recorded and self.choice_label and self.choice_play and self.choice_play.IsShown():
			selection = self.choice_play.GetString(self.choice_play.GetSelection())
			if selection == _("Prueba micrófono"):
				return self.temp_mic
			elif selection == _("Prueba sistema"):
				return self.temp_system
			else:
				return self.temp_combined
		else:
			return self.temp_combined

	def _get_wav_duration(self, wav_path):
		"""
		Obtiene la duración (en segundos) de un archivo WAV.

		:param wav_path: Ruta del archivo WAV.
		:return: Duración en segundos.
		"""
		try:
			with sf.SoundFile(wav_path) as f:
				duration = f.frames / float(f.samplerate)
			logger.log_action(f"Duración calculada para WAV: {duration} seg.")
			return duration
		except Exception as e:
			logger.log_error(f"Error al obtener duración del WAV: {e}")
			return 0
