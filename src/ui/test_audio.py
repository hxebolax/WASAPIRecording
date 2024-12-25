#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Diálogo para realizar una prueba de grabación y reproducción de audio,
usando los mismos parámetros que la ventana principal.

- No se puede cerrar con la X ni con Alt+F4; solo con "Cerrar".
- Si 'separate_files' está a True, se muestra un Choice tras detener la grabación
  para elegir entre "Prueba micrófono", "Prueba sistema" o "Ambos".
- El botón principal cambia según el estado interno (grabando, reproduciendo, etc.).
"""

import os
import wx
import tempfile
import winsound
import time
from threading import Thread, Event
import soundfile as sf
import soundcard as sc

from core.recorder import record_audio
from ui.widgets import mensaje
from core.logger import Logger
from core.utils import get_base_path  # Asegúrate de tener esta función en core.utils

# Inicialización del logger
logger = Logger(log_dir=os.path.join(get_base_path(), "logs"))


class TestAudioDialog(wx.Dialog):
	def __init__(self, parent, selected_mic, selected_system,
				 sample_rate, channels, separate_files,
				 mono_mix, mic_volume, system_volume):
		super().__init__(parent, title=_("Prueba de Audio"), style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)
		logger.log_action("TestAudioDialog: Inicializando el diálogo de prueba de audio.")

		# Bloqueamos la X, Alt+F4, etc.
		self.SetWindowStyleFlag(
			self.GetWindowStyleFlag()
			& ~wx.CLOSE_BOX
			& ~wx.MAXIMIZE_BOX
			& ~wx.MINIMIZE_BOX
			& ~wx.SYSTEM_MENU
		)
		# Evitar Alt+F4
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
		logger.log_action("TestAudioDialog: Configurado para bloquear cierre con la X y Alt+F4.")

		self.parent = parent
		self.selected_mic = selected_mic
		self.selected_system = selected_system
		self.sample_rate = sample_rate
		self.channels = channels
		self.separate_files = separate_files
		self.mono_mix = mono_mix
		self.mic_volume = mic_volume
		self.system_volume = system_volume

		# Estados
		self.is_recording = False
		self.is_recorded = False
		self.is_playing = False

		# Hilos y eventos
		self.recording_event = Event()
		self.recording_thread = None
		self.playback_timer = None
		self.playback_length_ms = 0

		# Rutas temporales
		self.temp_dir = tempfile.gettempdir()
		timestamp = time.strftime("%Y%m%d-%H%M%S")
		self.temp_combined = os.path.join(self.temp_dir, f"test_both_{timestamp}.wav")
		if self.separate_files:
			self.temp_mic = os.path.join(self.temp_dir, f"test_mic_{timestamp}.wav")
			self.temp_system = os.path.join(self.temp_dir, f"test_system_{timestamp}.wav")
		else:
			self.temp_mic = None
			self.temp_system = None

		logger.log_action(f"TestAudioDialog: Archivos temporales definidos: {self.temp_combined}, {self.temp_mic}, {self.temp_system}")

		# --------------------- UI Layout ---------------------
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		self.info_label = wx.StaticText(self, label=_("&Información:"))
		self.info_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
		self.info_text.SetMinSize((450, 200))
		main_sizer.Add(self.info_label, 0, wx.ALL | wx.EXPAND, 10)
		main_sizer.Add(self.info_text, 0, wx.ALL | wx.EXPAND, 10)
		self._set_explanation_text()
		logger.log_action("TestAudioDialog: Texto de explicación establecido.")

		hbox = wx.BoxSizer(wx.HORIZONTAL)

		# Creamos label y choice solo si separate_files == True
		# (Inicialmente ocultos, se mostrarán tras detener grabación)
		self.choice_label = None
		self.choice_play = None
		if self.separate_files:
			self.choice_label = wx.StaticText(self, label=_("&Selecciona qué archivo reproducir:"))
			self.choice_play = wx.Choice(self, choices=[
				_("Prueba micrófono"), _("Prueba sistema"), _("Ambos")
			])
			self.choice_play.SetSelection(2)  # "Ambos" por defecto
			# Ocultamos en principio
			self.choice_label.Hide()
			self.choice_play.Hide()

			hbox.Add(self.choice_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
			hbox.Add(self.choice_play, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
			logger.log_action("TestAudioDialog: Campos para selección de archivo de reproducción añadidos y ocultos inicialmente.")

		# Botón principal
		self.main_button = wx.Button(self, label=_("&Detener"))
		self.main_button.Bind(wx.EVT_BUTTON, self.on_main_button)
		hbox.Add(self.main_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
		logger.log_action("TestAudioDialog: Botón principal añadido y evento vinculado.")

		# Botón Cerrar
		self.close_button = wx.Button(self, label=_("&Cerrar"))
		self.close_button.Bind(wx.EVT_BUTTON, self.on_close_dialog)
		hbox.Add(self.close_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
		logger.log_action("TestAudioDialog: Botón 'Cerrar' añadido y evento vinculado.")

		main_sizer.Add(hbox, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)

		self.SetSizerAndFit(main_sizer)
		self.Centre()
		logger.log_action("TestAudioDialog: Layout configurado y diálogo centrado.")

		# Iniciar grabación
		self.start_recording()
		logger.log_action("TestAudioDialog: Grabación iniciada automáticamente al abrir el diálogo.")

	# ----------------- EVENTOS Y LÓGICA --------------------

	def on_key_down(self, event):
		key_code = event.GetKeyCode()
		# Si se presiona F4 con Alt, ignoramos
		if key_code == wx.WXK_F4 and event.AltDown():
			logger.log_action("TestAudioDialog: Se intentó cerrar el diálogo con Alt+F4, acción ignorada.")
			return
		event.Skip()

	def _set_explanation_text(self):
		explanation = _(
			"Esta ventana permite realizar una prueba de grabación y reproducción.\n\n"
			"1. Al abrirse, inicia la grabación con los mismos ajustes que la ventana principal.\n"
			"2. Para finalizar la grabación, pulsa 'Detener'. Entonces, el botón cambiará a 'Reproducir'.\n"
			"3. Si estaba activada la opción de 'Guardar archivos separados' en la ventana principal, "
			"se mostrará el menú desplegable para elegir si reproducir sólo micrófono, "
			"solo sistema o ambos (por defecto 'Ambos').\n"
			"4. Al pulsar 'Reproducir', se inicia la reproducción del WAV de forma asíncrona. "
			"El botón cambia a 'Detener' durante la reproducción. Al terminar la pista, "
			"volverá a 'Reproducir'.\n"
			"5. Si pulsas 'Cerrar' mientras graba, te preguntará si deseas cancelar la prueba (se borrarán "
			"los archivos). Si ya grabaste y/o terminaste, simplemente cerrará y también borrará los archivos.\n\n"
			"No puedes cerrar con Alt+F4 ni con la X de la ventana; solo con el botón 'Cerrar'.\n"
		)
		self.info_text.SetValue(explanation)
		logger.log_action("TestAudioDialog: Texto de información establecido.")

	# Inicia grabación
	def start_recording(self):
		self.is_recording = True
		self.is_recorded = False
		self.recording_event.set()
		self.recording_thread = Thread(target=record_audio, args=(
			self.recording_event,
			self.selected_mic,
			self.selected_system,
			self.sample_rate,
			self.channels,
			self.temp_dir,
			self.temp_combined,
			self.temp_mic,
			self.temp_system,
			self.mono_mix,
			self.mic_volume,
			self.system_volume
		))
		self.recording_thread.start()
		logger.log_action(f"TestAudioDialog: Thread de grabación iniciado para: {self.temp_combined}")

	# Detiene grabación
	def stop_recording(self):
		if self.is_recording:
			self.recording_event.clear()
			self.recording_thread.join()
			self.is_recording = False
			self.is_recorded = True
			logger.log_action("TestAudioDialog: Grabación detenida.")

	# Botón principal (Detener/Reproducir) => depende de is_recording / is_playing
	def on_main_button(self, event):
		if self.is_recording:
			# Estábamos grabando => detengo grabación
			self.stop_recording()
			self.main_button.SetLabel(_("Reproducir"))
			logger.log_action("TestAudioDialog: Botón principal cambiado a 'Reproducir' tras detener grabación.")
			# Si tenemos separate_files => mostrar choice
			if self.separate_files and self.choice_label and self.choice_play:
				self.choice_label.Show()
				self.choice_play.Show()
				self.choice_play.SetSelection(2)  # "Ambos"
				self.Layout()
				logger.log_action("TestAudioDialog: Campos de selección de archivo de reproducción mostrados.")
		elif not self.is_recording and not self.is_playing:
			# Ni grabando ni reproduciendo => iniciamos reproducción
			self.start_playback()
			self.main_button.SetLabel(_("Detener"))
			logger.log_action("TestAudioDialog: Botón principal cambiado a 'Detener' tras iniciar reproducción.")
		elif not self.is_recording and self.is_playing:
			# Estamos reproduciendo => lo detenemos
			self.stop_playback()
			self.main_button.SetLabel(_("Reproducir"))
			logger.log_action("TestAudioDialog: Botón principal cambiado a 'Reproducir' tras detener reproducción.")

	# Inicia reproducción del WAV (asíncrona con winsound)
	def start_playback(self):
		if not self.is_recorded:
			mensaje(self, _("No se ha grabado nada aún. Primero detenga la grabación."), _("Aviso"))
			logger.log_action("TestAudioDialog: Intento de reproducción sin haber grabado.")
			return
		if self.is_playing:
			logger.log_action("TestAudioDialog: Intento de iniciar reproducción mientras ya está reproduciendo.")
			return

		to_play = self._get_file_to_play()
		if not to_play or not os.path.isfile(to_play):
			mensaje(self, _("No existe el archivo a reproducir"), _("Error"), style=wx.ICON_ERROR)
			logger.log_error("TestAudioDialog: Archivo a reproducir no encontrado.")
			return

		duration_sec = self._get_wav_duration(to_play)
		self.playback_length_ms = int(duration_sec * 1000)

		try:
			winsound.PlaySound(to_play, winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.is_playing = True
			logger.log_action(f"TestAudioDialog: Reproducción iniciada para: {to_play}")
		except Exception as e:
			mensaje(self, str(e), _("Error"), style=wx.ICON_ERROR)
			logger.log_error(f"TestAudioDialog: Error al iniciar reproducción: {e}")
			return

		self.playback_timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.on_playback_timer, self.playback_timer)
		self.playback_timer.Start(self.playback_length_ms, oneShot=True)
		logger.log_action(f"TestAudioDialog: Timer de reproducción iniciado por {self.playback_length_ms} ms.")

	# Detiene reproducción
	def stop_playback(self):
		winsound.PlaySound(None, winsound.SND_PURGE)
		self.is_playing = False
		if self.playback_timer and self.playback_timer.IsRunning():
			self.playback_timer.Stop()
			logger.log_action("TestAudioDialog: Reproducción detenida manualmente.")
	
	def on_playback_timer(self, event):
		if self.is_playing:
			self.stop_playback()
			self.main_button.SetLabel(_("Reproducir"))
			logger.log_action("TestAudioDialog: Reproducción finalizada automáticamente al terminar el timer.")

	def on_close_dialog(self, event):
		# Si sigue grabando => pregunta
		if self.is_recording:
			resp = mensaje(
				self,
				_("La grabación sigue en curso. ¿Desea cancelar la prueba de sonido?"),
				_("Cancelar Prueba"),
				style=wx.YES_NO | wx.ICON_QUESTION
			)
			logger.log_action("TestAudioDialog: Usuario intentó cerrar el diálogo mientras grababa.")
			if resp == wx.YES:
				self.stop_recording()
				self.cleanup_temp_files()
				logger.log_action("TestAudioDialog: Grabación cancelada por el usuario.")
				self.EndModal(wx.ID_OK)
			else:
				logger.log_action("TestAudioDialog: Usuario canceló la acción de cerrar el diálogo durante grabación.")
				return
		else:
			# Si ya no graba => paramos reproducción y cerramos
			self.stop_playback()
			self.cleanup_temp_files()
			logger.log_action("TestAudioDialog: Cerrando diálogo después de detener reproducción.")
			self.EndModal(wx.ID_OK)

	def cleanup_temp_files(self):
		try:
			if os.path.isfile(self.temp_combined):
				os.remove(self.temp_combined)
				logger.log_action(f"TestAudioDialog: Archivo temporal eliminado: {self.temp_combined}")
			if self.temp_mic and os.path.isfile(self.temp_mic):
				os.remove(self.temp_mic)
				logger.log_action(f"TestAudioDialog: Archivo temporal de micrófono eliminado: {self.temp_mic}")
			if self.temp_system and os.path.isfile(self.temp_system):
				os.remove(self.temp_system)
				logger.log_action(f"TestAudioDialog: Archivo temporal de sistema eliminado: {self.temp_system}")
		except Exception as e:
			logger.log_error(f"TestAudioDialog: Error al limpiar archivos temporales: {e}")

	def _get_file_to_play(self):
		# Si tenemos separate_files y ya hay algo grabado => segun choice
		if self.separate_files and self.is_recorded and self.choice_label and self.choice_play and self.choice_play.IsShown():
			selection = self.choice_play.GetString(self.choice_play.GetSelection())
			if selection == _("Prueba micrófono"):
				logger.log_action("TestAudioDialog: Seleccionado para reproducir 'Prueba micrófono'.")
				return self.temp_mic
			elif selection == _("Prueba sistema"):
				logger.log_action("TestAudioDialog: Seleccionado para reproducir 'Prueba sistema'.")
				return self.temp_system
			else:
				logger.log_action("TestAudioDialog: Seleccionado para reproducir 'Ambos'.")
				return self.temp_combined
		else:
			# sino => reproducimos la mezcla (both)
			logger.log_action("TestAudioDialog: Reproduciendo mezcla combinada por defecto.")
			return self.temp_combined

	def _get_wav_duration(self, wav_path):
		try:
			with sf.SoundFile(wav_path) as f:
				duration = f.frames / float(f.samplerate)
			logger.log_action(f"TestAudioDialog: Duración del WAV obtenido: {duration} segundos.")
			return duration
		except Exception as e:
			logger.log_error(f"TestAudioDialog: Error al obtener duración del WAV: {e}")
			return 0
