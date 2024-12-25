#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que define el diálogo de Opciones con una pestaña General y otra para configurar Teclado (hotkeys).

Ahora, se implementa la devolución de dos valores (general_changed, keyboard_changed)
para que interface.py decida si necesita revalidar hotkeys o no.

Además, se añade la validación de que no se puedan asignar la misma combinación de teclas
para iniciar y detener grabación.
"""

import os
import wx
from core.config import load_config, save_config, get_base_path
from core.hotkeys import (
	start_capturing,
	stop_capturing,
	load_hotkeys_from_config,
	save_hotkeys_to_config
)
from ui.widgets import mensaje
from core.logger import Logger
from core.utils import get_base_path  # Asegúrate de tener esta función en core.utils

# Inicialización del logger
logger = Logger(log_dir=os.path.join(get_base_path(), "logs"))


class GeneralPanel(wx.Panel):
	"""
	Panel General del diálogo de opciones.
	Contiene la casilla para minimizar a la bandeja.
	"""

	def __init__(self, parent):
		"""
		Inicializa el panel General con el checkbox para minimizar a la bandeja.
		"""
		super().__init__(parent)
		logger.log_action("GeneralPanel: Inicializando el panel General.")
		sizer = wx.BoxSizer(wx.VERTICAL)

		self.config_file = os.path.join(get_base_path(), "WASAPIRecording.dat")
		self.cfg = load_config(self.config_file)
		logger.log_action(f"GeneralPanel: Configuración cargada desde {self.config_file}.")

		# Checkbox minimizar a bandeja
		self.minimize_checkbox = wx.CheckBox(self, label=_("Minimizar a la bandeja del sistema"))
		self.minimize_checkbox.SetValue(self.cfg.get("minimize_to_tray", False))
		sizer.Add(self.minimize_checkbox, 0, wx.ALL, 10)
		logger.log_action("GeneralPanel: Checkbox para minimizar a bandeja añadido.")

		self.SetSizer(sizer)

	def save_settings(self):
		"""
		Guarda la configuración del panel General en el archivo
		solo si hay cambios reales.
		Retorna True si cambió algo, False si no cambió nada.
		"""
		old_value = self.cfg.get("minimize_to_tray", False)
		new_value = self.minimize_checkbox.GetValue()

		if new_value != old_value:
			self.cfg["minimize_to_tray"] = new_value
			save_config(self.config_file, self.cfg)
			logger.log_action("GeneralPanel: Configuración de 'minimize_to_tray' guardada.")
			return True
		else:
			logger.log_action("GeneralPanel: No se detectaron cambios en 'minimize_to_tray'.")
			# No hay cambios
			return False


class KeyboardPanel(wx.Panel):
	"""
	Panel para configurar las hotkeys (Teclado).
	"""

	def __init__(self, parent):
		super().__init__(parent)
		logger.log_action("KeyboardPanel: Inicializando el panel de Teclado.")
		sizer = wx.BoxSizer(wx.VERTICAL)

		self.cfg = load_hotkeys_from_config()
		logger.log_action("KeyboardPanel: Configuración de hotkeys cargada.")

		self.is_capturing_start = False
		self.is_capturing_stop = False

		# Etiquetas y campos para hotkey de INICIAR
		sizer.Add(wx.StaticText(self, label=_("Combinación para Iniciar Grabación:")), 0, wx.ALL, 5)
		self.start_display = wx.TextCtrl(
			self, value=self.cfg["hotkey_start"],
			style=wx.TE_MULTILINE | wx.TE_READONLY
		)
		self.start_display.SetBackgroundColour(wx.Colour(240, 240, 240))
		sizer.Add(self.start_display, 0, wx.ALL | wx.EXPAND, 5)
		logger.log_action("KeyboardPanel: Campo de texto para hotkey de inicio añadido.")

		self.start_button = wx.Button(self, label=_("Capturar Hotkey Inicio"))
		self.start_button.Bind(wx.EVT_BUTTON, self.on_capture_start)
		sizer.Add(self.start_button, 0, wx.ALL | wx.CENTER, 5)
		logger.log_action("KeyboardPanel: Botón para capturar hotkey de inicio añadido y vinculado.")

		# Etiquetas y campos para hotkey de DETENER
		sizer.Add(wx.StaticText(self, label=_("Combinación para Detener Grabación:")), 0, wx.ALL, 5)
		self.stop_display = wx.TextCtrl(
			self, value=self.cfg["hotkey_stop"],
			style=wx.TE_MULTILINE | wx.TE_READONLY
		)
		self.stop_display.SetBackgroundColour(wx.Colour(240, 240, 240))
		sizer.Add(self.stop_display, 0, wx.ALL | wx.EXPAND, 5)
		logger.log_action("KeyboardPanel: Campo de texto para hotkey de detención añadido.")

		self.stop_button = wx.Button(self, label=_("Capturar Hotkey Parar"))
		self.stop_button.Bind(wx.EVT_BUTTON, self.on_capture_stop)
		sizer.Add(self.stop_button, 0, wx.ALL | wx.CENTER, 5)
		logger.log_action("KeyboardPanel: Botón para capturar hotkey de detención añadido y vinculado.")

		self.SetSizer(sizer)

	def on_capture_start(self, event):
		"""
		Comienza la captura para la hotkey de inicio.
		"""
		logger.log_action("KeyboardPanel: Iniciando captura de hotkey de inicio.")
		self.is_capturing_start = True
		self.is_capturing_stop = False
		self.start_display.SetValue(_("Esperando combinación..."))
		self.start_display.SetFocus()
		start_capturing()

	def on_capture_stop(self, event):
		"""
		Comienza la captura para la hotkey de parada.
		"""
		logger.log_action("KeyboardPanel: Iniciando captura de hotkey de detención.")
		self.is_capturing_stop = True
		self.is_capturing_start = False
		self.stop_display.SetValue(_("Esperando combinación..."))
		self.stop_display.SetFocus()
		start_capturing()

	def on_hotkey_captured(self, combination):
		"""
		Se llama desde hotkeys.py cuando se detecta la hotkey.
		"""
		logger.log_action(f"KeyboardPanel: Hotkey capturada: {combination}")
		if self.is_capturing_start:
			self.cfg["hotkey_start"] = combination
			self.start_display.SetValue(combination)
			self.is_capturing_start = False
			self.start_display.SetFocus()
			logger.log_action("KeyboardPanel: Hotkey de inicio actualizada.")
		elif self.is_capturing_stop:
			self.cfg["hotkey_stop"] = combination
			self.stop_display.SetValue(combination)
			self.is_capturing_stop = False
			self.stop_display.SetFocus()
			logger.log_action("KeyboardPanel: Hotkey de detención actualizada.")

	def on_hotkey_error(self):
		"""
		Si hubo error al registrar, se restaura la hotkey anterior.
		"""
		logger.log_error("KeyboardPanel: Error al capturar la hotkey.")
		if self.is_capturing_start:
			self.start_display.SetValue(self.cfg["hotkey_start"])
			self.is_capturing_start = False
			logger.log_action("KeyboardPanel: Hotkey de inicio revertida a anterior.")
		elif self.is_capturing_stop:
			self.stop_display.SetValue(self.cfg["hotkey_stop"])
			self.is_capturing_stop = False
			logger.log_action("KeyboardPanel: Hotkey de detención revertida a anterior.")

	def save_settings(self):
		"""
		Guarda las hotkeys en el archivo solo si hay cambios reales.
		Retorna True si hubo un cambio, False si no.
		
		Además, validamos que no sean la misma combinación para iniciar y detener
		(salvo que sea "Sin asignar", que se ignora).
		"""
		old_cfg = load_hotkeys_from_config()
		old_start = old_cfg["hotkey_start"]
		old_stop = old_cfg["hotkey_stop"]

		new_start = self.cfg["hotkey_start"]
		new_stop = self.cfg["hotkey_stop"]

		logger.log_action("KeyboardPanel: Guardando configuraciones de hotkeys.")

		# 1) Verificamos si el usuario puso la misma combinación en ambas:
		if (
			new_start != "Sin asignar" and
			new_stop != "Sin asignar" and
			new_start == new_stop
		):
			mensaje(
				self,
				_("No puede asignar la misma combinación a Iniciar y Detener.\nPor favor, elija una diferente.\nSe revertirán los cambios a los que tenia por defecto."),
				_("Error de Hotkeys"),
				style=wx.OK | wx.ICON_ERROR
			)
			logger.log_warning("KeyboardPanel: Usuario intentó asignar la misma hotkey a inicio y detención.")
			# Revertimos a lo anterior, para no guardar algo inválido.
			self.cfg["hotkey_start"] = old_start
			self.cfg["hotkey_stop"] = old_stop
			# Actualizamos displays:
			self.start_display.SetValue(old_start)
			self.stop_display.SetValue(old_stop)
			return False

		# 2) Si pasó la validación, vemos si hubo cambios:
		changed = False
		if new_start != old_start or new_stop != old_stop:
			save_hotkeys_to_config(new_start, new_stop)
			changed = True
			logger.log_action("KeyboardPanel: Hotkeys guardadas en configuración.")

		else:
			logger.log_action("KeyboardPanel: No se detectaron cambios en las hotkeys.")

		return changed


class OptionsDialog(wx.Dialog):
	"""
	Diálogo de opciones con un Notebook: General y Teclado.
	"""

	def __init__(self, parent):
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
		self.keyboard_panel.on_hotkey_captured(combination)
		logger.log_action(f"OptionsDialog: Hotkey capturada: {combination}")

	def on_hotkey_error(self):
		self.keyboard_panel.on_hotkey_error()
		logger.log_error("OptionsDialog: Error al capturar hotkey.")

	def save_all_settings2(self):
		"""
		Guarda la configuración en ambos paneles.
		Retorna una tupla (general_changed, keyboard_changed).
		
		Se llama desde interface.py al aceptar el diálogo.
		"""
		logger.log_action("OptionsDialog: Guardando configuraciones de ambos paneles.")
		general_changed = self.general_panel.save_settings()
		keyboard_changed = self.keyboard_panel.save_settings()
		logger.log_action(f"OptionsDialog: Configuración general cambiada: {general_changed}, "
						 f"Configuración de hotkeys cambiada: {keyboard_changed}.")
		return (general_changed, keyboard_changed)
