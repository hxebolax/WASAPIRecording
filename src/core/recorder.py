#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que contiene la lógica de grabación usando BASS y WASAPI.
"""

import os
import sys
import time
import ctypes
from core.logger import Logger
from core.utils import get_base_path

import sound_lib.external.pybass as pybass
import sound_lib.external.pybasswasapi as pybasswasapi
import sound_lib.external.pybassmix as pybassmix
import sound_lib.external.pybassenc as pybassenc

logger = Logger(log_dir=os.path.abspath(os.path.join(get_base_path(), "logs")))

# Callbacks de WASAPI
def wasapi_capture_callback(buffer, length, user):
	"""
	Callback llamado por BASSWASAPI cuando hay nuevos datos capturados.
	Empuja los datos al stream de BASS correspondiente.
	"""
	if user:
		pybass.BASS_StreamPutData(user, buffer, length)
	return 1

# Envoltura de callback para ctypes
WASAPIPROC = pybasswasapi.WASAPIPROC(wasapi_capture_callback)

def record_audio(
	recording_event,
	selected_mic_index,
	selected_system_index,
	sample_rate,
	final_channels,
	output_dir,
	combined_output_path,
	mic_output_path=None,
	system_output_path=None,
	mic_volume=1.0,
	system_volume=1.0,
	mic_mode="Estéreo",
	system_mode="Estéreo",
	buffer_size=1024,
	pause_event=None,
	cancel_event=None
):
	"""
	Graba audio usando BASSWASAPI y BASSMIX.
	"""
	try:
		if pause_event is None:
			import threading
			pause_event = threading.Event()
		if cancel_event is None:
			import threading
			cancel_event = threading.Event()

		os.makedirs(output_dir, exist_ok=True)
		logger.log_action(f"Grabación BASSWASAPI iniciada. Mic: {selected_mic_index}, System: {selected_system_index}")

		# 1. Crear Mixer (decodificador, para que nosotros tiremos de él)
		# Usamos BASS_STREAM_DECODE para que sea el bucle de Python quien controle el flujo
		mixer = pybassmix.BASS_Mixer_StreamCreate(sample_rate, 2, pybass.BASS_STREAM_DECODE)
		if not mixer:
			logger.log_error(f"Error creando mixer BASS: {pybass.BASS_ErrorGetCode()}")
			return

		streams = []
		wasapi_sessions = []
		
		# 2. Configurar dispositivos
		def setup_device(idx, name_label):
			if idx < 0: return None, None
			
			# Info del dispositivo para saber su frecuencia nativa
			info = pybasswasapi.BASS_WASAPI_DEVICEINFO()
			pybasswasapi.BASS_WASAPI_GetDeviceInfo(idx, ctypes.byref(info))
			native_freq = info.mixfreq
			native_chans = info.mixchans
			
			# Crear Push Stream en BASS con el formato nativo del dispositivo
			# O forzar el formato que queremos. BASS_StreamCreate soporta push streams.
			# Usamos BASS_STREAM_DECODE porque se mezclará
			push = pybass.BASS_StreamCreate(native_freq, native_chans, pybass.BASS_STREAM_DECODE, pybass.STREAMPROC_PUSH, None)
			
			# Inicializar WASAPI
			# BASS_WASAPI_Init(device, freq, chans, flags, buffer, period, proc, user)
			# Usamos AUTOFORMAT para que BASS se encargue de las conversiones si es necesario
			flags = pybasswasapi.BASS_WASAPI_AUTOFORMAT
			if not pybasswasapi.BASS_WASAPI_Init(idx, 0, 0, flags, 0.4, 0.05, WASAPIPROC, ctypes.c_void_p(push)):
				logger.log_error(f"Error init WASAPI dispositivo {idx} ({name_label}): {pybass.BASS_ErrorGetCode()}")
				pybass.BASS_StreamFree(push)
				return None, None
			
			return idx, push

		mic_idx, mic_push = setup_device(selected_mic_index, "Mic")
		sys_idx, sys_push = setup_device(selected_system_index, "System")

		# 3. Añadir al mixer y configurar volúmenes/modos
		if mic_push:
			# Añadir al mixer con resampleo automático
			pybassmix.BASS_Mixer_StreamAddChannel(mixer, mic_push, pybassmix.BASS_MIXER_DOWNMIX | pybassmix.BASS_MIXER_LIMIT)
			pybassmix.BASS_Mixer_ChannelSetAttribute(mic_push, pybass.BASS_ATTRIB_VOL, mic_volume)
			if mic_mode == "Mono": # o _("Mono")
				# BASSMIX puede hacer downmix a mono, pero aquí el mixer es estéreo. 
				# Podemos usar una matriz de mezcla si fuera necesario, pero por ahora volumen es suficiente.
				pass

		if sys_push:
			pybassmix.BASS_Mixer_StreamAddChannel(mixer, sys_push, pybassmix.BASS_MIXER_DOWNMIX | pybassmix.BASS_MIXER_LIMIT)
			pybassmix.BASS_Mixer_ChannelSetAttribute(sys_push, pybass.BASS_ATTRIB_VOL, system_volume)

		# 4. Iniciar encoders (grabación a WAV)
		# BASS_Encode_Start(handle, cmdline, flags, proc, user)
		def start_wav_encoder(handle, path):
			# BASS_ENCODE_PCM escribe un WAV. BASS_UNICODE para rutas con caracteres especiales.
			return pybassenc.BASS_Encode_Start(handle, path.encode('utf-16le'), pybassenc.BASS_ENCODE_PCM | pybass.BASS_UNICODE | pybassenc.BASS_ENCODE_AUTOFREE, None, None)

		enc_combined = start_wav_encoder(mixer, combined_output_path)
		enc_mic = start_wav_encoder(mic_push, mic_output_path) if mic_output_path and mic_push else None
		enc_sys = start_wav_encoder(sys_push, system_output_path) if system_output_path and sys_push else None

		# 5. Iniciar captura WASAPI
		if mic_idx is not None:
			pybasswasapi.BASS_WASAPI_SetDevice(mic_idx)
			pybasswasapi.BASS_WASAPI_Start()
		if sys_idx is not None:
			pybasswasapi.BASS_WASAPI_SetDevice(sys_idx)
			pybasswasapi.BASS_WASAPI_Start()

		# 6. Bucle de bombeo de datos
		# Como el mixer y los push streams son DECODE, tenemos que pedirle datos al mixer
		# para que el encoder reciba los datos y los escriba.
		temp_buf_size = 20480 # 20KB approx
		temp_buf = (ctypes.c_byte * temp_buf_size)()
		
		logger.log_action("Grabación en bucle iniciada.")
		
		try:
			while recording_event.is_set() and not cancel_event.is_set():
				if pause_event.is_set():
					# Si está en pausa, podríamos detener WASAPI o simplemente dejar de bombear.
					# Detener bombeo es más fácil.
					time.sleep(0.1)
					continue
				
				# Extraer datos del mixer (esto dispara el encoder)
				got = pybass.BASS_ChannelGetData(mixer, temp_buf, temp_buf_size)
				if got == -1:
					break
				if got == 0:
					time.sleep(0.01)
					continue
				
				# Si queremos archivos separados, el bombeo del mixer solo dispara el encoder del mixer.
				# Los encoders de los canales individuales se disparan cuando los datos entran en el mixer.
				# Espera: BASS_Mixer_StreamAddChannel con BASS_STREAM_DECODE canales:
				# Cuando el mixer pide datos a los canales, los datos pasan por los canales.
				# Así que enc_mic y enc_sys deberían funcionar.

			logger.log_action("Bucle de grabación finalizado.")
		finally:
			# 7. Limpieza
			if mic_idx is not None:
				pybasswasapi.BASS_WASAPI_SetDevice(mic_idx)
				pybasswasapi.BASS_WASAPI_Stop(True)
				pybasswasapi.BASS_WASAPI_Free()
			if sys_idx is not None:
				pybasswasapi.BASS_WASAPI_SetDevice(sys_idx)
				pybasswasapi.BASS_WASAPI_Stop(True)
				pybasswasapi.BASS_WASAPI_Free()
			
			if enc_combined: pybassenc.BASS_Encode_Stop(enc_combined)
			if enc_mic: pybassenc.BASS_Encode_Stop(enc_mic)
			if enc_sys: pybassenc.BASS_Encode_Stop(enc_sys)
			
			pybass.BASS_StreamFree(mixer)
			if mic_push: pybass.BASS_StreamFree(mic_push)
			if sys_push: pybass.BASS_StreamFree(sys_push)

		if cancel_event.is_set():
			logger.log_action("Cancelación detectada. Eliminando archivos parciales...")
			for path in [combined_output_path, mic_output_path, system_output_path]:
				if path and os.path.exists(path):
					try: os.remove(path)
					except: pass

	except Exception as e:
		logger.log_error(f"Error en record_audio (BASS): {e}")
		import traceback
		logger.log_error(traceback.format_exc())
