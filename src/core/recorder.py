#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que contiene la lógica de grabación.

Este módulo permite grabar audio desde micrófono y sistema (loopback), mezclarlos en tiempo 
real y guardar los resultados en archivos de audio con soporte para cancelación y pausa 
durante la grabación. También asegura que todos los archivos sean consistentes en formato 
(2 canales) para evitar problemas relacionados con dispositivos de hardware.

Estrategia:
- Se configuran los dispositivos con `channels=None` para adaptarse al hardware.
- Se permite grabar en modos "Mono" o "Estéreo", asegurando siempre 2 canales en los archivos.
- Se pueden controlar los eventos de grabación, pausa y cancelación.

Funciones principales:
- Convertir datos de audio entre modos mono y estéreo.
- Grabar audio en tiempo real con control de eventos.
- Ajustar dinámicamente el volumen de los canales.
- Eliminar archivos parciales si se cancela la grabación.

Clases: Ninguna.
Dependencias:
- `soundfile`: Para guardar audio en formato compatible.
- `numpy`: Para procesar datos de audio en arreglos multidimensionales.
- `core.logger`: Para registrar acciones y errores.
- `core.utils`: Para manejar rutas y configuraciones.
"""
import os
import sys
import soundfile as sf
import numpy as np
from core.logger import Logger
from core.utils import get_base_path
import time

logger = Logger(log_dir=os.path.abspath(os.path.join(get_base_path(), "logs")))

def expand_to_stereo(data):
	"""
	Duplica un array mono para generar 2 canales.

	:param data: Array numpy en forma (N,) o (N,1).
	:return: Array numpy en forma (N,2) con los mismos valores en ambos canales.
	"""
	if data.ndim == 1:
		# (N,) -> (N,1)
		data = data.reshape(-1, 1)
	# data ahora es (N,1)
	return np.concatenate([data, data], axis=1)

def to_mono(stereo_data):
	"""
	Convierte datos estéreo (N,2) a pseudo-mono (L=R) usando la media de ambos canales.

	:param stereo_data: Array numpy en forma (N,2).
	:return: Array numpy en forma (N,2) con ambos canales igualados al promedio.
	"""
	mono_data = stereo_data.mean(axis=1)
	# Generar (N,2) duplicando la media
	return np.column_stack((mono_data, mono_data))

def _adjust_user_mode(data, user_mode):
	"""
	Ajusta los datos de audio según el modo seleccionado por el usuario.

	- "Mono": Convierte los datos a mono asegurando 2 canales con L=R.
	- "Estéreo": Asegura que los datos tengan 2 canales sin alterarlos.

	:param data: Array numpy devuelto por el hardware.
	:param user_mode: "Mono" o "Estéreo" como cadena.
	:return: Array numpy ajustado a (N,2).
	"""
	# Asegurar forma 2D
	if data.ndim == 1:
		# (N,) -> (N,1)
		data = data.reshape(-1, 1)

	num_chan = data.shape[1]
	# Si hardware da 2 canales y user elige "Mono", downmix a L=R
	if num_chan == 2 and user_mode == "Mono":
		return to_mono(data)

	# Si hardware da 1 canal y user elige "Estéreo", expandimos a (N,2)
	if num_chan == 1 and user_mode == "Estéreo":
		return expand_to_stereo(data)

	# Si hardware da 1 canal y user elige "Mono", lo guardamos en L=R (en disco 2 canales)
	if num_chan == 1 and user_mode == "Mono":
		return expand_to_stereo(data)

	# Si hardware da 2 canales y user elige "Estéreo", no cambiamos nada
	# pero aseguramos que sea (N,2)
	if num_chan == 2:
		return data

	# Por si acaso, forzamos a estéreo
	return expand_to_stereo(data)

def record_audio(
	recording_event,
	selected_mic,
	selected_system,
	sample_rate,
	final_channels,
	output_dir,
	combined_output_path,
	mic_output_path=None,
	system_output_path=None,
	mic_volume=1.0,
	system_volume=0.5,
	mic_mode="Estéreo",
	system_mode="Estéreo",
	buffer_size=1024,
	pause_event=None,
	cancel_event=None
):
	"""
	Graba audio desde micrófono y sistema, ajustando volumen y modo según el usuario.

	La grabación soporta pausa y cancelación. En caso de cancelación, elimina los archivos
	parciales generados.

	:param recording_event: Evento para controlar inicio y finalización de la grabación.
	:param selected_mic: Dispositivo de micrófono seleccionado.
	:param selected_system: Dispositivo de loopback seleccionado.
	:param sample_rate: Tasa de muestreo en Hz.
	:param final_channels: Ignorado; siempre se graba en 2 canales en disco.
	:param output_dir: Directorio donde se guardan los archivos de audio.
	:param combined_output_path: Ruta del archivo combinado (micrófono + sistema).
	:param mic_output_path: (Opcional) Ruta del archivo separado del micrófono.
	:param system_output_path: (Opcional) Ruta del archivo separado del sistema.
	:param mic_volume: Volumen del micrófono como flotante (0.0 a 1.0).
	:param system_volume: Volumen del sistema como flotante (0.0 a 1.0).
	:param mic_mode: "Mono" o "Estéreo" para los datos del micrófono.
	:param system_mode: "Mono" o "Estéreo" para los datos del sistema.
	:param buffer_size: Tamaño del buffer de grabación en frames.
	:param pause_event: Evento para pausar la grabación.
	:param cancel_event: Evento para cancelar la grabación y eliminar archivos.
	"""
	try:
		if pause_event is None:
			# Si no se pasó un evento de pausa, creamos uno "dummy" en False
			import threading
			pause_event = threading.Event()

		if cancel_event is None:
			# Si no se pasó un evento de cancelar, creamos uno "dummy" en False
			import threading
			cancel_event = threading.Event()

		if sys.platform.startswith("win"):
			import pythoncom
			try:
				pythoncom.CoInitialize()
				logger.log_action("DEBUG: COM inicializado en el hilo de grabación.")
			except Exception as e:
				logger.log_error(f"Error al inicializar COM en hilo de grabación: {e}")

		os.makedirs(output_dir, exist_ok=True)
		logger.log_action(f"Directorio de salida creado/existente: {output_dir}")

		system_gain = 2.0
		mic_gain = 4.0

		logger.log_action(f"Archivo combinado: {combined_output_path}")
		if mic_output_path:
			logger.log_action(f"Archivo separado mic: {mic_output_path}")
		if system_output_path:
			logger.log_action(f"Archivo separado sistema: {system_output_path}")

		with selected_system.recorder(samplerate=sample_rate, channels=None) as system_rec, \
		     selected_mic.recorder(samplerate=sample_rate, channels=None) as mic_rec, \
		     sf.SoundFile(combined_output_path, mode='w', samplerate=sample_rate, channels=2) as combined_file:

			mic_file = None
			system_file = None
			if mic_output_path:
				mic_file = sf.SoundFile(mic_output_path, mode='w', samplerate=sample_rate, channels=2)
			if system_output_path:
				system_file = sf.SoundFile(system_output_path, mode='w', samplerate=sample_rate, channels=2)

			logger.log_action("Grabación iniciada correctamente.")

			try:
				while recording_event.is_set() and not cancel_event.is_set():
					# Si está en pausa, no escribimos nada
					if pause_event.is_set():
						time.sleep(0.1)
						continue

					system_data = system_rec.record(numframes=buffer_size)
					mic_data = mic_rec.record(numframes=buffer_size)

					system_data *= (system_volume * system_gain)
					mic_data *= (mic_volume * mic_gain)

					system_data = np.clip(system_data, -1.0, 1.0)
					mic_data = np.clip(mic_data, -1.0, 1.0)

					# Ajuste a user_mode => (N,2)
					system_data_2 = _adjust_user_mode(system_data, system_mode)
					mic_data_2 = _adjust_user_mode(mic_data, mic_mode)

					# Escritura en archivos separados
					if system_file is not None:
						system_file.write(system_data_2)
						system_file.flush()
					if mic_file is not None:
						mic_file.write(mic_data_2)
						mic_file.flush()

					# Combinación
					combined_data = (system_data_2 + mic_data_2) / 2
					combined_data = np.clip(combined_data, -1.0, 1.0)

					# Guardar el combinado, también 2 canales
					combined_file.write(combined_data)
					combined_file.flush()

				logger.log_action("Datos de audio grabados y almacenados correctamente.")
			finally:
				if mic_file is not None:
					mic_file.close()
					logger.log_action(f"Archivo de micrófono cerrado: {mic_output_path}")
				if system_file is not None:
					system_file.close()
					logger.log_action(f"Archivo del sistema cerrado: {system_output_path}")
				logger.log_action("Grabación finalizada.")
	except Exception as e:
		logger.log_error(f"Error en record_audio: {e}")
	finally:
		# Si se ha cancelado la grabación, se eliminan los archivos parciales
		if cancel_event.is_set():
			logger.log_action("Se detectó cancelación de la grabación. Eliminando archivos parciales...")
			for path in [combined_output_path, mic_output_path, system_output_path]:
				if path and os.path.exists(path):
					try:
						os.remove(path)
						logger.log_action(f"Archivo eliminado: {path}")
					except Exception as ex:
						logger.log_error(f"Error al eliminar {path}: {ex}")

		if sys.platform.startswith("win"):
			try:
				import pythoncom
				pythoncom.CoUninitialize()
				logger.log_action("DEBUG: COM liberado en el hilo de grabación.")
			except:
				pass
