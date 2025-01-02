#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que contiene el diálogo de opciones, dividido en pestañas para:
- Configuraciones generales (minimizar a bandeja, carpeta de grabaciones).
- Configuración de hotkeys (inicio, pausa, detener, cancelar).

Cada pestaña es manejada por un panel específico. Al hacer clic en "Aceptar",
se guardan los cambios en la configuración.
"""

import os
import wx
from core.hotkeys import (
	start_capturing,
	stop_capturing,
	load_hotkeys_from_config,
	save_hotkeys_to_config
)
from ui.widgets import mensaje
from core.logger import Logger
from core.config import load_config, save_config, get_base_path

logger = Logger(log_dir=os.path.join(get_base_path(), "logs"))

class GeneralPanel(wx.Panel):
	"""
	Panel con la configuración general de la aplicación,
	como minimizar a la bandeja y elegir la carpeta de grabaciones.
	"""
	def __init__(self, parent):
		"""
		Constructor del panel General.

		:param parent: Objeto padre (el notebook del diálogo).
		"""
		super().__init__(parent)
		logger.log_action("GeneralPanel: Inicializando el panel General.")
		sizer = wx.BoxSizer(wx.VERTICAL)

		self.config_file = os.path.join(get_base_path(), "WASAPIRecording.dat")
		self.cfg = load_config(self.config_file)
		logger.log_action(f"GeneralPanel: Configuración cargada desde {self.config_file}.")

		self.minimize_checkbox = wx.CheckBox(self, label=_("Minimizar a la bandeja del sistema"))
		self.minimize_checkbox.SetValue(self.cfg.get("minimize_to_tray", False))
		sizer.Add(self.minimize_checkbox, 0, wx.ALL, 10)
		logger.log_action("GeneralPanel: Checkbox para minimizar a bandeja añadido.")

		sizer.Add(wx.StaticText(self, label=_("Carpeta de grabaciones:")), 0, wx.TOP | wx.LEFT, 10)
		self.recording_dir = self.cfg.get("recording_dir", "")
		self.recording_dir_text = wx.TextCtrl(
			self, value=self.recording_dir,
			style=wx.TE_MULTILINE | wx.TE_READONLY
		)
		sizer.Add(self.recording_dir_text, 0, wx.ALL | wx.EXPAND, 10)

		self.browse_button = wx.Button(self, label=_("Cambiar carpeta..."))
		self.browse_button.Bind(wx.EVT_BUTTON, self.on_browse_recording_dir)
		sizer.Add(self.browse_button, 0, wx.BOTTOM | wx.LEFT, 10)

		self.SetSizer(sizer)

	def on_browse_recording_dir(self, event):
		"""
		Abre un diálogo para seleccionar la carpeta de grabaciones.

		:param event: Evento de botón.
		"""
		dialog = wx.DirDialog(
			self,
			message=_("Selecciona la carpeta donde se guardarán las grabaciones"),
			defaultPath=self.recording_dir or os.path.abspath(os.path.join(get_base_path(), "recording")),
			style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
		)
		if dialog.ShowModal() == wx.ID_OK:
			new_dir = dialog.GetPath()
			self.recording_dir = new_dir
			self.recording_dir_text.SetValue(new_dir)
			logger.log_action(f"GeneralPanel: Usuario eligió la carpeta de grabaciones: {new_dir}")
		dialog.Destroy()

	def save_settings(self):
		"""
		Guarda la configuración del panel si hay cambios.

		:return: True si hubo cambios y se guardó, False si no hubo cambios.
		"""
		old_value = self.cfg.get("minimize_to_tray", False)
		new_value = self.minimize_checkbox.GetValue()

		old_dir = self.cfg.get("recording_dir", "")
		new_dir = self.recording_dir

		changed = False

		if new_value != old_value:
			self.cfg["minimize_to_tray"] = new_value
			changed = True

		if new_dir != old_dir:
			self.cfg["recording_dir"] = new_dir
			changed = True

		if changed:
			save_config(self.config_file, self.cfg)
			logger.log_action("GeneralPanel: Configuración de 'minimize_to_tray' y/o 'recording_dir' guardada.")
			return True
		else:
			logger.log_action("GeneralPanel: No se detectaron cambios en 'minimize_to_tray' o 'recording_dir'.")
			return False

class KeyboardPanel(wx.Panel):
	"""
	Panel para gestionar las hotkeys de la aplicación: Iniciar, Detener, Pausar, Cancelar.
	"""
	def __init__(self, parent):
		"""
		Constructor del panel de teclado.

		:param parent: Objeto padre (el notebook del diálogo).
		"""
		super().__init__(parent)
		logger.log_action("KeyboardPanel: Inicializando el panel de Teclado.")
		sizer = wx.BoxSizer(wx.VERTICAL)

		self.cfg = load_hotkeys_from_config()
		logger.log_action("KeyboardPanel: Configuración de hotkeys cargada.")

		self.capturing = None  # "start", "stop", "pause", "cancel"

		sizer.Add(wx.StaticText(self, label=_("Combinación para Iniciar Grabación:")), 0, wx.ALL, 5)
		self.start_display = wx.TextCtrl(
			self,
			value=self.cfg["hotkey_start"],
			style=wx.TE_MULTILINE | wx.TE_READONLY
		)
		self.start_display.SetBackgroundColour(wx.Colour(240, 240, 240))
		sizer.Add(self.start_display, 0, wx.ALL | wx.EXPAND, 5)

		self.start_button = wx.Button(self, label=_("Capturar Hotkey Inicio"))
		self.start_button.Bind(wx.EVT_BUTTON, lambda evt: self.on_capture("start"))
		sizer.Add(self.start_button, 0, wx.ALL | wx.CENTER, 5)

		sizer.Add(wx.StaticText(self, label=_("Combinación para Detener Grabación:")), 0, wx.ALL, 5)
		self.stop_display = wx.TextCtrl(
			self,
			value=self.cfg["hotkey_stop"],
			style=wx.TE_MULTILINE | wx.TE_READONLY
		)
		self.stop_display.SetBackgroundColour(wx.Colour(240, 240, 240))
		sizer.Add(self.stop_display, 0, wx.ALL | wx.EXPAND, 5)

		self.stop_button = wx.Button(self, label=_("Capturar Hotkey Detener"))
		self.stop_button.Bind(wx.EVT_BUTTON, lambda evt: self.on_capture("stop"))
		sizer.Add(self.stop_button, 0, wx.ALL | wx.CENTER, 5)

		sizer.Add(wx.StaticText(self, label=_("Combinación para Pausar/Reanudar:")), 0, wx.ALL, 5)
		self.pause_display = wx.TextCtrl(
			self,
			value=self.cfg["hotkey_pause"],
			style=wx.TE_MULTILINE | wx.TE_READONLY
		)
		self.pause_display.SetBackgroundColour(wx.Colour(240, 240, 240))
		sizer.Add(self.pause_display, 0, wx.ALL | wx.EXPAND, 5)

		self.pause_button = wx.Button(self, label=_("Capturar Hotkey Pausa"))
		self.pause_button.Bind(wx.EVT_BUTTON, lambda evt: self.on_capture("pause"))
		sizer.Add(self.pause_button, 0, wx.ALL | wx.CENTER, 5)

		sizer.Add(wx.StaticText(self, label=_("Combinación para Cancelar Grabación:")), 0, wx.ALL, 5)
		self.cancel_display = wx.TextCtrl(
			self,
			value=self.cfg["hotkey_cancel"],
			style=wx.TE_MULTILINE | wx.TE_READONLY
		)
		self.cancel_display.SetBackgroundColour(wx.Colour(240, 240, 240))
		sizer.Add(self.cancel_display, 0, wx.ALL | wx.EXPAND, 5)

		self.cancel_button = wx.Button(self, label=_("Capturar Hotkey Cancelar"))
		self.cancel_button.Bind(wx.EVT_BUTTON, lambda evt: self.on_capture("cancel"))
		sizer.Add(self.cancel_button, 0, wx.ALL | wx.CENTER, 5)

		self.SetSizer(sizer)

	def on_capture(self, which):
		"""
		Inicia la captura de la hotkey para la acción especificada.

		:param which: Puede ser "start", "stop", "pause" o "cancel".
		"""
		self.capturing = which
		if which == "start":
			self.start_display.SetValue(_("Esperando combinación..."))
			self.start_display.SetFocus()
		elif which == "stop":
			self.stop_display.SetValue(_("Esperando combinación..."))
			self.stop_display.SetFocus()
		elif which == "pause":
			self.pause_display.SetValue(_("Esperando combinación..."))
			self.pause_display.SetFocus()
		elif which == "cancel":
			self.cancel_display.SetValue(_("Esperando combinación..."))
			self.cancel_display.SetFocus()

		start_capturing()

	def on_hotkey_captured(self, combination):
		"""
		Llamado cuando se captura una hotkey global.

		:param combination: La combinación capturada (ej. "Ctrl+Shift+F1").
		"""
		logger.log_action(f"KeyboardPanel: Hotkey capturada: {combination}")
		if self.capturing == "start":
			self.cfg["hotkey_start"] = combination
			self.start_display.SetValue(combination)
			self.start_display.SetFocus()
		elif self.capturing == "stop":
			self.cfg["hotkey_stop"] = combination
			self.stop_display.SetValue(combination)
			self.stop_display.SetFocus()
		elif self.capturing == "pause":
			self.cfg["hotkey_pause"] = combination
			self.pause_display.SetValue(combination)
			self.pause_display.SetFocus()
		elif self.capturing == "cancel":
			self.cfg["hotkey_cancel"] = combination
			self.cancel_display.SetValue(combination)
			self.cancel_display.SetFocus()

		self.capturing = None

	def on_hotkey_error(self):
		"""
		Llamado cuando ocurre un error al capturar la hotkey (combinación no válida o en uso).
		Revierte el campo de texto al valor anterior.
		"""
		logger.log_error("KeyboardPanel: Error al capturar la hotkey.")
		if self.capturing == "start":
			self.start_display.SetValue(self.cfg["hotkey_start"])
			self.start_display.SetFocus()
		elif self.capturing == "stop":
			self.stop_display.SetValue(self.cfg["hotkey_stop"])
			self.stop_display.SetFocus()
		elif self.capturing == "pause":
			self.pause_display.SetValue(self.cfg["hotkey_pause"])
			self.pause_display.SetFocus()
		elif self.capturing == "cancel":
			self.cancel_display.SetValue(self.cfg["hotkey_cancel"])
			self.cancel_display.SetFocus()
		self.capturing = None

	def save_settings(self):
		"""
		Guarda los valores de las hotkeys si hubo cambios y son válidas.

		:return: True si hubo cambios, False si no.
		"""
		old_cfg = load_hotkeys_from_config()
		old_start = old_cfg["hotkey_start"]
		old_stop = old_cfg["hotkey_stop"]
		old_pause = old_cfg["hotkey_pause"]
		old_cancel = old_cfg["hotkey_cancel"]

		new_start = self.cfg["hotkey_start"]
		new_stop = self.cfg["hotkey_stop"]
		new_pause = self.cfg["hotkey_pause"]
		new_cancel = self.cfg["hotkey_cancel"]

		all_hotkeys = []
		for val in [new_start, new_stop, new_pause, new_cancel]:
			if val != "Sin asignar":
				all_hotkeys.append(val)

		if len(all_hotkeys) != len(set(all_hotkeys)):
			mensaje(
				self,
				_("No puede asignar la misma combinación a más de una acción.\nSe revertirán los cambios."),
				_("Error de Hotkeys"),
				style=wx.OK | wx.ICON_ERROR
			)
			self.cfg["hotkey_start"] = old_start
			self.cfg["hotkey_stop"] = old_stop
			self.cfg["hotkey_pause"] = old_pause
			self.cfg["hotkey_cancel"] = old_cancel

			self.start_display.SetValue(old_start)
			self.stop_display.SetValue(old_stop)
			self.pause_display.SetValue(old_pause)
			self.cancel_display.SetValue(old_cancel)
			return False

		changed = False
		if (new_start != old_start) or (new_stop != old_stop) or (new_pause != old_pause) or (new_cancel != old_cancel):
			save_hotkeys_to_config(new_start, new_stop, new_pause, new_cancel)
			changed = True
			logger.log_action("KeyboardPanel: Hotkeys guardadas en configuración.")
		else:
			logger.log_action("KeyboardPanel: No se detectaron cambios en las hotkeys.")

		return changed

class OptionsDialog(wx.Dialog):
	"""
	Diálogo principal de opciones, con un wx.Listbook que contiene:
	- GeneralPanel (configuraciones generales).
	- KeyboardPanel (hotkeys).
	"""
	def __init__(self, parent):
		"""
		Constructor del diálogo de opciones.

		:param parent: Ventana padre (AudioRecorderFrame).
		"""
		super().__init__(parent, title=_("Opciones"), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
		logger.log_action("OptionsDialog: Inicializando el diálogo de opciones.")

		sizer = wx.BoxSizer(wx.VERTICAL)
		notebook = wx.Listbook(self)

		self.general_panel = GeneralPanel(notebook)
		self.keyboard_panel = KeyboardPanel(notebook)

		notebook.AddPage(self.general_panel, _("General"))
		notebook.AddPage(self.keyboard_panel, _("Teclado"))
		logger.log_action("OptionsDialog: Páginas 'General' y 'Teclado' añadidas al notebook.")

		sizer.Add(notebook, 1, wx.ALL | wx.EXPAND, 10)

		btn_sizer = wx.StdDialogButtonSizer()
		ok_btn = wx.Button(self, wx.ID_OK, label=_("Aceptar"))
		cancel_btn = wx.Button(self, wx.ID_CANCEL, label=_("Cancelar"))
		btn_sizer.AddButton(ok_btn)
		btn_sizer.AddButton(cancel_btn)
		btn_sizer.Realize()
		sizer.Add(btn_sizer, 0, wx.ALL | wx.EXPAND, 10)
		logger.log_action("OptionsDialog: Botones 'Aceptar' y 'Cancelar' añadidos.")

		self.SetSizerAndFit(sizer)
		self.Centre()
		logger.log_action("OptionsDialog: Sizer principal asignado y diálogo centrado.")

	def on_hotkey_captured(self, combination):
		"""
		Maneja la hotkey capturada y la pasa al panel de teclado.

		:param combination: Cadena con la combinación (ej. "Ctrl+Shift+F2").
		"""
		self.keyboard_panel.on_hotkey_captured(combination)
		logger.log_action(f"OptionsDialog: Hotkey capturada: {combination}")

	def on_hotkey_error(self):
		"""
		Maneja el error al capturar una hotkey, informando al panel de teclado.
		"""
		self.keyboard_panel.on_hotkey_error()
		logger.log_error("OptionsDialog: Error al capturar hotkey.")

	def save_all_settings2(self):
		"""
		Guarda la configuración de ambos paneles y retorna si hubo cambios
		en configuración general y/o hotkeys.

		:return: (bool, bool) => (general_changed, keyboard_changed).
		"""
		logger.log_action("OptionsDialog: Guardando configuraciones de ambos paneles.")
		general_changed = self.general_panel.save_settings()
		keyboard_changed = self.keyboard_panel.save_settings()
		logger.log_action(f"OptionsDialog: Configuración general cambiada: {general_changed}, Hotkeys cambiadas: {keyboard_changed}.")
		return (general_changed, keyboard_changed)
