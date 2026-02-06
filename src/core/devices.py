#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para manejo de dispositivos de audio usando BASSWASAPI.
"""
import os
import ctypes
from core.utils import get_base_path
from core.logger import Logger
from ui.widgets import mensaje
import wx

import sound_lib.external.pybass as pybass
import sound_lib.external.pybasswasapi as pybasswasapi

logger = Logger(log_dir=os.path.abspath(os.path.join(get_base_path(), "logs")))

def get_wasapi_devices():
	"""
	Enumera dispositivos WASAPI disponibles.
	Retorna dos listas de tuplas (índice, nombre): (micrófonos, loopbacks).
	"""
	mics = []
	loopbacks = []
	
	i = 0
	info = pybasswasapi.BASS_WASAPI_DEVICEINFO()
	while pybasswasapi.BASS_WASAPI_GetDeviceInfo(i, ctypes.byref(info)):
		if info.flags & pybasswasapi.BASS_DEVICE_ENABLED:
			try:
				name = info.name.decode('mbcs')
			except:
				name = info.name.decode('utf-8', 'replace')
			
			# En BASSWASAPI:
			# Loopback tiene BASS_DEVICE_LOOPBACK
			# Input tiene BASS_DEVICE_INPUT
			if info.flags & pybasswasapi.BASS_DEVICE_LOOPBACK:
				loopbacks.append((i, name))
			elif info.flags & pybasswasapi.BASS_DEVICE_INPUT:
				mics.append((i, name))
		i += 1
	return mics, loopbacks

def refresh_devices(mic_choice, system_choice, status_box):
	"""
	Refresca las listas de dispositivos disponibles para micrófono y sistema.
	"""
	try:
		logger.log_action("Iniciando actualización de dispositivos de audio WASAPI.")

		mics, loopbacks = get_wasapi_devices()

		mic_choice.Clear()
		for idx, name in mics:
			mic_choice.Append(name, idx)
		
		if mics:
			mic_choice.SetSelection(0)
			logger.log_action(f"Micrófonos detectados: {[m[1] for m in mics]}")
		else:
			logger.log_action("No se detectaron micrófonos WASAPI.")

		system_choice.Clear()
		for idx, name in loopbacks:
			system_choice.Append(name, idx)
		
		if loopbacks:
			system_choice.SetSelection(0)
			logger.log_action(f"Dispositivos de sistema (loopback) detectados: {[l[1] for l in loopbacks]}")
		else:
			logger.log_action("No se detectaron dispositivos de sistema (loopback) WASAPI.")

		status_box.SetValue(_("Dispositivos actualizados correctamente."))
		logger.log_action("Dispositivos actualizados correctamente.")
	except Exception as e:
		error_message = f"Error al refrescar dispositivos: {e}"
		status_box.SetValue(_("Error al refrescar dispositivos: {error}").format(error=e))
		logger.log_error(error_message)

def update_selected_mic(selected_name, mic_choice):
	"""
	Retorna el índice del dispositivo de micrófono seleccionado.
	"""
	sel = mic_choice.GetSelection()
	if sel != wx.NOT_FOUND:
		idx = mic_choice.GetClientData(sel)
		logger.log_action(f"Micrófono seleccionado: {selected_name} (Index: {idx})")
		return idx
	return -1

def update_selected_system(selected_name, system_choice):
	"""
	Retorna el índice del dispositivo de sistema seleccionado.
	"""
	sel = system_choice.GetSelection()
	if sel != wx.NOT_FOUND:
		idx = system_choice.GetClientData(sel)
		logger.log_action(f"Sistema seleccionado: {selected_name} (Index: {idx})")
		return idx
	return -1

def update_quality(choice):
	try:
		quality = int(choice.GetStringSelection())
		logger.log_action(f"Calidad de audio seleccionada: {quality}")
		return quality
	except Exception as e:
		logger.log_error(f"Error al actualizar calidad: {e}")
		return 44100

def update_output_format(choice):
	try:
		output_format = choice.GetStringSelection()
		logger.log_action(f"Formato de salida seleccionado: {output_format}")
		return output_format
	except Exception as e:
		logger.log_error(f"Error al actualizar formato de salida: {e}")
		return "wav"

def update_bitrate(choice):
	try:
		bitrate = int(choice.GetStringSelection())
		logger.log_action(f"Bitrate seleccionado: {bitrate}")
		return bitrate
	except Exception as e:
		logger.log_error(f"Error al actualizar bitrate: {e}")
		return 128

def update_mic_volume(slider):
	try:
		volume = slider.GetValue() / 100.0
		logger.log_action(f"Volumen del micrófono actualizado: {volume}")
		return volume
	except Exception as e:
		logger.log_error(f"Error al actualizar volumen del micrófono: {e}")
		return 0.5

def update_system_volume(slider):
	try:
		volume = slider.GetValue() / 100.0
		logger.log_action(f"Volumen del sistema actualizado: {volume}")
		return volume
	except Exception as e:
		logger.log_error(f"Error al actualizar volumen del sistema: {e}")
		return 0.5

def check_audio_hardware():
	"""
	Verificación básica de que BASS y WASAPI están disponibles.
	"""
	try:
		mics, loopbacks = get_wasapi_devices()
		if not mics and not loopbacks:
			logger.log_error("No se detectaron dispositivos WASAPI.")
			mensaje(None,
					_("No se detectó ningún dispositivo de audio WASAPI habilitado."),
					_("Error de Audio"),
					style=wx.OK | wx.ICON_ERROR)
			return False
		return True
	except Exception as e:
		logger.log_error(f"Error verificando hardware: {e}")
		return False
