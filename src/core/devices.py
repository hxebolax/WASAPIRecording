#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para manejo de dispositivos de audio y actualización de parámetros.
"""

import soundcard as sc
import os
from core.utils import get_base_path
from core.logger import Logger  # Importar Logger

# Instanciar Logger
# Instanciar Logger con la ubicación de logs en la raíz del proyecto
logger = Logger(log_dir=os.path.join(get_base_path(), "logs"))

def refresh_devices(mic_choice, system_choice, status_box):
	"""
	Refresca la lista de dispositivos disponibles en los Choice de mic y sistema.

	:param mic_choice: Control wx.Choice para micrófono
	:param system_choice: Control wx.Choice para sistema
	:param status_box: Control wx.TextCtrl para mostrar estado
	"""
	try:
		logger.log_action("Iniciando actualización de dispositivos de audio.")

		# Actualizar micrófonos
		mic_list = [mic.name for mic in sc.all_microphones()]
		mic_choice.Clear()
		mic_choice.AppendItems(mic_list)
		if mic_list:
			mic_choice.SetSelection(0)
			logger.log_action(f"Micrófonos detectados: {mic_list}")
		else:
			logger.log_action("No se detectaron micrófonos.")

		# Actualizar dispositivos del sistema
		system_list = [sys.name for sys in sc.all_microphones(include_loopback=True)]
		system_choice.Clear()
		system_choice.AppendItems(system_list)
		if system_list:
			system_choice.SetSelection(0)
			logger.log_action(f"Dispositivos de sistema detectados: {system_list}")
		else:
			logger.log_action("No se detectaron dispositivos del sistema.")

		# Mostrar estado
		status_box.SetValue(_("Dispositivos actualizados correctamente."))
		logger.log_action("Dispositivos actualizados correctamente.")
	except Exception as e:
		error_message = f"Error al refrescar dispositivos: {e}"
		status_box.SetValue(_("Error al refrescar dispositivos: {error}").format(error=e))
		logger.log_error(error_message)

def update_selected_mic(selected_name):
	"""
	Retorna el objeto micrófono seleccionado a partir de su nombre.

	:param selected_name: Nombre del micrófono seleccionado.
	:return: Objeto del micrófono seleccionado o el micrófono predeterminado.
	"""
	try:
		logger.log_action(f"Actualizando micrófono seleccionado: {selected_name}")
		for mic in sc.all_microphones():
			if mic.name == selected_name:
				logger.log_action(f"Micrófono seleccionado: {mic.name}")
				return mic
		default_mic = sc.default_microphone()
		logger.log_action(f"Usando micrófono predeterminado: {default_mic.name}")
		return default_mic
	except Exception as e:
		logger.log_error(f"Error al seleccionar micrófono: {e}")
		return sc.default_microphone()

def update_selected_system(selected_name):
	"""
	Retorna el objeto del sistema (loopback) seleccionado a partir de su nombre.

	:param selected_name: Nombre del sistema seleccionado.
	:return: Objeto del sistema seleccionado o el sistema predeterminado.
	"""
	try:
		logger.log_action(f"Actualizando dispositivo del sistema seleccionado: {selected_name}")
		for sys in sc.all_microphones(include_loopback=True):
			if sys.name == selected_name:
				logger.log_action(f"Dispositivo del sistema seleccionado: {sys.name}")
				return sys
		default_system = sc.get_microphone(sc.default_speaker().name, include_loopback=True)
		logger.log_action(f"Usando dispositivo del sistema predeterminado: {default_system.name}")
		return default_system
	except Exception as e:
		logger.log_error(f"Error al seleccionar dispositivo del sistema: {e}")
		return sc.get_microphone(sc.default_speaker().name, include_loopback=True)

def update_quality(choice):
	"""
	Actualiza la calidad (sample_rate) a partir del wx.Choice de calidad.

	:param choice: Control wx.Choice con las opciones de calidad.
	:return: Valor seleccionado como entero.
	"""
	try:
		quality = int(choice.GetStringSelection())
		logger.log_action(f"Calidad de audio seleccionada: {quality}")
		return quality
	except Exception as e:
		logger.log_error(f"Error al actualizar calidad: {e}")
		return 44100  # Valor predeterminado

def update_output_format(choice):
	"""
	Retorna el formato seleccionado.

	:param choice: Control wx.Choice con las opciones de formato.
	:return: Formato seleccionado como cadena.
	"""
	try:
		output_format = choice.GetStringSelection()
		logger.log_action(f"Formato de salida seleccionado: {output_format}")
		return output_format
	except Exception as e:
		logger.log_error(f"Error al actualizar formato de salida: {e}")
		return "wav"  # Valor predeterminado

def update_bitrate(choice):
	"""
	Retorna el bitrate seleccionado.

	:param choice: Control wx.Choice con las opciones de bitrate.
	:return: Valor seleccionado como entero.
	"""
	try:
		bitrate = int(choice.GetStringSelection())
		logger.log_action(f"Bitrate seleccionado: {bitrate}")
		return bitrate
	except Exception as e:
		logger.log_error(f"Error al actualizar bitrate: {e}")
		return 128  # Valor predeterminado

def update_mic_volume(slider):
	"""
	Retorna el volumen del micrófono (0.0 a 1.0) a partir del slider.

	:param slider: Control wx.Slider para el volumen del micrófono.
	:return: Valor del volumen como flotante.
	"""
	try:
		volume = slider.GetValue() / 100.0
		logger.log_action(f"Volumen del micrófono actualizado: {volume}")
		return volume
	except Exception as e:
		logger.log_error(f"Error al actualizar volumen del micrófono: {e}")
		return 0.5  # Valor predeterminado

def update_system_volume(slider):
	"""
	Retorna el volumen del sistema (0.0 a 1.0) a partir del slider.

	:param slider: Control wx.Slider para el volumen del sistema.
	:return: Valor del volumen como flotante.
	"""
	try:
		volume = slider.GetValue() / 100.0
		logger.log_action(f"Volumen del sistema actualizado: {volume}")
		return volume
	except Exception as e:
		logger.log_error(f"Error al actualizar volumen del sistema: {e}")
		return 0.5  # Valor predeterminado
