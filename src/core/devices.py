#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para manejo de dispositivos de audio y actualización de parámetros.

Este módulo permite gestionar dispositivos de entrada y salida de audio, incluyendo 
micrófonos y sistemas de loopback. Proporciona funciones para actualizar las listas 
de dispositivos disponibles, seleccionar micrófonos o sistemas específicos, y ajustar 
parámetros como calidad, formato, bitrate y volúmenes.

No se modifica la parte de refrescar dispositivos, ya que la apertura real se realiza 
en el módulo 'recording.py' con la configuración `channels=None`. Aquí se maneja y 
retorna únicamente la referencia a cada dispositivo.
"""
import soundcard as sc
import os
from core.utils import get_base_path
from core.logger import Logger
import wx

logger = Logger(log_dir=os.path.abspath(os.path.join(get_base_path(), "logs")))

def refresh_devices(mic_choice, system_choice, status_box):
	"""
	Refresca las listas de dispositivos disponibles para micrófono y sistema.

	:param mic_choice: Control wx.Choice para mostrar micrófonos disponibles.
	:param system_choice: Control wx.Choice para mostrar sistemas disponibles (loopback incluido).
	:param status_box: Control wx.TextCtrl para mostrar mensajes de estado al usuario.
	"""
	try:
		logger.log_action("Iniciando actualización de dispositivos de audio.")

		mic_list = [mic.name for mic in sc.all_microphones()]
		mic_choice.Clear()
		mic_choice.AppendItems(mic_list)
		if mic_list:
			mic_choice.SetSelection(0)
			logger.log_action(f"Micrófonos detectados: {mic_list}")
		else:
			logger.log_action("No se detectaron micrófonos.")

		system_list = [sysdev.name for sysdev in sc.all_microphones(include_loopback=True)]
		system_choice.Clear()
		system_choice.AppendItems(system_list)
		if system_list:
			system_choice.SetSelection(0)
			logger.log_action(f"Dispositivos de sistema detectados: {system_list}")
		else:
			logger.log_action("No se detectaron dispositivos del sistema.")

		status_box.SetValue(_("Dispositivos actualizados correctamente."))
		logger.log_action("Dispositivos actualizados correctamente.")
	except Exception as e:
		error_message = f"Error al refrescar dispositivos: {e}"
		status_box.SetValue(_("Error al refrescar dispositivos: {error}").format(error=e))
		logger.log_error(error_message)

def update_selected_mic(selected_name):
	"""
	Selecciona y retorna el micrófono correspondiente al nombre indicado.

	:param selected_name: Nombre del micrófono seleccionado.
	:return: Objeto del micrófono seleccionado o, en su defecto, el micrófono predeterminado.
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
	Selecciona y retorna el sistema (loopback) correspondiente al nombre indicado.

	:param selected_name: Nombre del sistema seleccionado.
	:return: Objeto del sistema seleccionado o, en su defecto, el sistema predeterminado.
	"""
	try:
		logger.log_action(f"Actualizando dispositivo del sistema seleccionado: {selected_name}")
		for sysdev in sc.all_microphones(include_loopback=True):
			if sysdev.name == selected_name:
				logger.log_action(f"Dispositivo del sistema seleccionado: {sysdev.name}")
				return sysdev
		default_system = sc.get_microphone(sc.default_speaker().name, include_loopback=True)
		logger.log_action(f"Usando dispositivo del sistema predeterminado: {default_system.name}")
		return default_system
	except Exception as e:
		logger.log_error(f"Error al seleccionar dispositivo del sistema: {e}")
		return sc.get_microphone(sc.default_speaker().name, include_loopback=True)

def update_quality(choice):
	"""
	Actualiza y retorna la calidad de audio seleccionada a partir de un control wx.Choice.

	:param choice: Control wx.Choice que contiene las opciones de calidad de audio.
	:return: Valor de calidad seleccionado como entero (sample rate).
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
	Selecciona y retorna el formato de salida desde un control wx.Choice.

	:param choice: Control wx.Choice con las opciones de formato de salida.
	:return: Formato de salida seleccionado como cadena (ejemplo: "wav").
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
	Selecciona y retorna el bitrate desde un control wx.Choice.

	:param choice: Control wx.Choice con las opciones de bitrate.
	:return: Valor de bitrate seleccionado como entero.
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
	Actualiza y retorna el volumen del micrófono a partir de un control wx.Slider.

	:param slider: Control wx.Slider para ajustar el volumen del micrófono.
	:return: Valor del volumen como flotante (rango: 0.0 a 1.0).
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
	Actualiza y retorna el volumen del sistema a partir de un control wx.Slider.

	:param slider: Control wx.Slider para ajustar el volumen del sistema.
	:return: Valor del volumen como flotante (rango: 0.0 a 1.0).
	"""
	try:
		volume = slider.GetValue() / 100.0
		logger.log_action(f"Volumen del sistema actualizado: {volume}")
		return volume
	except Exception as e:
		logger.log_error(f"Error al actualizar volumen del sistema: {e}")
		return 0.5  # Valor predeterminado
