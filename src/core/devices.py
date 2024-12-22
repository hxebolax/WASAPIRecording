#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para manejo de dispositivos de audio y actualización de parámetros.
"""

import soundcard as sc

def refresh_devices(mic_choice, system_choice, status_box):
	"""
	Refresca la lista de dispositivos disponibles en los Choice de mic y sistema.

	:param mic_choice: Control wx.Choice para micrófono
	:param system_choice: Control wx.Choice para sistema
	:param status_box: Control wx.TextCtrl para mostrar estado
	"""
	try:
		mic_list = [mic.name for mic in sc.all_microphones()]
		mic_choice.Clear()
		mic_choice.AppendItems(mic_list)
		if mic_list:
			mic_choice.SetSelection(0)

		system_list = [sys.name for sys in sc.all_microphones(include_loopback=True)]
		system_choice.Clear()
		system_choice.AppendItems(system_list)
		if system_list:
			system_choice.SetSelection(0)

		status_box.SetValue(_("Dispositivos actualizados correctamente."))
	except Exception as e:
		status_box.SetValue(
			_("Error al refrescar dispositivos: {error}").format(error=e)
		)

def update_selected_mic(selected_name):
	"""
	Retorna el objeto micrófono seleccionado a partir de su nombre.
	"""
	for mic in sc.all_microphones():
		if mic.name == selected_name:
			return mic
	return sc.default_microphone()

def update_selected_system(selected_name):
	"""
	Retorna el objeto del sistema (loopback) seleccionado a partir de su nombre.
	"""
	for sys in sc.all_microphones(include_loopback=True):
		if sys.name == selected_name:
			return sys
	return sc.get_microphone(sc.default_speaker().name, include_loopback=True)

def update_quality(choice):
	"""
	Actualiza la calidad (sample_rate) a partir del wx.Choice de calidad.
	"""
	return int(choice.GetStringSelection())

def update_output_format(choice):
	"""
	Retorna el formato seleccionado.
	"""
	return choice.GetStringSelection()

def update_bitrate(choice):
	"""
	Retorna el bitrate seleccionado.
	"""
	return int(choice.GetStringSelection())

def update_mic_volume(slider):
	"""
	Retorna el volumen del micrófono (0.0 a 1.0) a partir del slider.
	"""
	return slider.GetValue() / 100.0

def update_system_volume(slider):
	"""
	Retorna el volumen del sistema (0.0 a 1.0) a partir del slider.
	"""
	return slider.GetValue() / 100.0
