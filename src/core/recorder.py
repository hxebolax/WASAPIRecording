#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que contiene la lógica de grabación. Se mezcla y guarda el audio en tiempo real.
Se asegura flush en cada escritura para que los archivos vayan creciendo en tiempo real.
"""

import os
import soundfile as sf
import numpy as np
from core.logger import Logger

# Inicialización del logger
logger = Logger(log_dir=os.path.join(os.getcwd(), "logs"))

def record_audio(recording_event, selected_mic, selected_system, sample_rate, channels, output_dir,
				combined_output_path, mic_output_path=None, system_output_path=None,
				mono_mix=False, mic_volume=1.0, system_volume=0.5):
	"""
	Graba audio desde los dispositivos seleccionados y lo mezcla en tiempo real.
	Se guarda directamente el audio combinado en un archivo final (WAV), evitando posprocesamiento.
	Se llama flush() después de cada escritura para que el archivo refleje inmediatamente el contenido.
	
	:param recording_event: Evento que controla la grabación.
	:param selected_mic: Dispositivo de entrada de micrófono.
	:param selected_system: Dispositivo de entrada del sistema.
	:param sample_rate: Tasa de muestreo.
	:param channels: Número de canales (1 para mono, 2 para estéreo).
	:param output_dir: Directorio donde se guardarán los archivos.
	:param combined_output_path: Ruta del archivo combinado de salida.
	:param mic_output_path: (Opcional) Ruta del archivo de salida para el micrófono.
	:param system_output_path: (Opcional) Ruta del archivo de salida para el sistema.
	:param mono_mix: (Opcional) Si es True, mezcla estéreo a mono.
	:param mic_volume: (Opcional) Volumen del micrófono.
	:param system_volume: (Opcional) Volumen del sistema.
	"""
	os.makedirs(output_dir, exist_ok=True)
	logger.log_action(f"Directorio de salida creado o ya existente: {output_dir}")

	numframes = 1024
	
	system_gain = 2.0
	mic_gain = 4.0

	with selected_system.recorder(samplerate=sample_rate, channels=channels) as system_rec, \
		selected_mic.recorder(samplerate=sample_rate, channels=channels) as mic_rec, \
		sf.SoundFile(combined_output_path, mode='w', samplerate=sample_rate, channels=channels) as combined_file:

		mic_file = sf.SoundFile(mic_output_path, mode='w', samplerate=sample_rate, channels=channels) if mic_output_path else None
		system_file = sf.SoundFile(system_output_path, mode='w', samplerate=sample_rate, channels=channels) if system_output_path else None

		logger.log_action(f"Grabación iniciada. Archivo combinado: {combined_output_path}")

		try:
			while recording_event.is_set():
				system_data = system_rec.record(numframes=numframes)
				mic_data = mic_rec.record(numframes=numframes)

				system_data *= (system_volume * system_gain)
				mic_data *= (mic_volume * mic_gain)

				system_data = np.clip(system_data, -1.0, 1.0)
				mic_data = np.clip(mic_data, -1.0, 1.0)

				if channels == 2 and mono_mix:
					mic_data = to_mono(mic_data)
					system_data = to_mono(system_data)

				combined_data = (system_data + mic_data) / 2
				combined_data = np.clip(combined_data, -1.0, 1.0)

				combined_file.write(combined_data)
				combined_file.flush()

				if mic_file is not None:
					mic_file.write(mic_data)
					mic_file.flush()
				if system_file is not None:
					system_file.write(system_data)
					system_file.flush()
			logger.log_action("Datos de audio grabados y almacenados correctamente.")
		finally:
			if mic_file is not None:
				mic_file.close()
				logger.log_action(f"Archivo de micrófono cerrado: {mic_output_path}")
			if system_file is not None:
				system_file.close()
				logger.log_action(f"Archivo del sistema cerrado: {system_output_path}")
			logger.log_action("Grabación finalizada correctamente.")

def to_mono(stereo_data):
	"""
	Convierte datos estéreo a mono duplicando el promedio de ambos canales.
	
	:param stereo_data: Datos en formato estéreo (numpy array).
	:return: Datos convertidos a mono (numpy array).
	"""
	mono_data = stereo_data.mean(axis=1)
	logger.log_action("Datos convertidos a mono.")
	return np.column_stack((mono_data, mono_data))
