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
		sizer = wx.BoxSizer(wx.VERTICAL)

		self.config_file = os.path.join(get_base_path(), "WASAPIRecording.dat")
		self.cfg = load_config(self.config_file)

		# Checkbox minimizar a bandeja
		self.minimize_checkbox = wx.CheckBox(self, label=_("Minimizar a la bandeja del sistema"))
		self.minimize_checkbox.SetValue(self.cfg.get("minimize_to_tray", False))
		sizer.Add(self.minimize_checkbox, 0, wx.ALL, 10)

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
			return True
		else:
			# No hay cambios
			return False


class KeyboardPanel(wx.Panel):
	"""
	Panel para configurar las hotkeys (Teclado).
	"""
	def __init__(self, parent):
		super().__init__(parent)
		sizer = wx.BoxSizer(wx.VERTICAL)

		self.cfg = load_hotkeys_from_config()
		self.is_capturing_start = False
		self.is_capturing_stop = False

		# Etiquetas y campos para hotkey de INICIAR
		sizer.Add(wx.StaticText(self, label=_("Combinación para Iniciar Grabación:")), 0, wx.ALL, 5)
		self.start_display = wx.TextCtrl(self, value=self.cfg["hotkey_start"], 
										 style=wx.TE_MULTILINE | wx.TE_READONLY)
		self.start_display.SetBackgroundColour(wx.Colour(240,240,240))
		sizer.Add(self.start_display, 0, wx.ALL|wx.EXPAND, 5)

		self.start_button = wx.Button(self, label=_("Capturar Hotkey Inicio"))
		self.start_button.Bind(wx.EVT_BUTTON, self.on_capture_start)
		sizer.Add(self.start_button, 0, wx.ALL|wx.CENTER, 5)

		# Etiquetas y campos para hotkey de DETENER
		sizer.Add(wx.StaticText(self, label=_("Combinación para Detener Grabación:")), 0, wx.ALL, 5)
		self.stop_display = wx.TextCtrl(self, value=self.cfg["hotkey_stop"], 
										style=wx.TE_MULTILINE | wx.TE_READONLY)
		self.stop_display.SetBackgroundColour(wx.Colour(240,240,240))
		sizer.Add(self.stop_display, 0, wx.ALL|wx.EXPAND, 5)

		self.stop_button = wx.Button(self, label=_("Capturar Hotkey Parar"))
		self.stop_button.Bind(wx.EVT_BUTTON, self.on_capture_stop)
		sizer.Add(self.stop_button, 0, wx.ALL|wx.CENTER, 5)

		self.SetSizer(sizer)

	def on_capture_start(self, event):
		"""
		Comienza la captura para la hotkey de inicio.
		"""
		self.is_capturing_start = True
		self.is_capturing_stop = False
		self.start_display.SetValue(_("Esperando combinación..."))
		self.start_display.SetFocus()
		start_capturing()

	def on_capture_stop(self, event):
		"""
		Comienza la captura para la hotkey de parada.
		"""
		self.is_capturing_stop = True
		self.is_capturing_start = False
		self.stop_display.SetValue(_("Esperando combinación..."))
		self.stop_display.SetFocus()
		start_capturing()

	def on_hotkey_captured(self, combination):
		"""
		Se llama desde hotkeys.py cuando se detecta la hotkey.
		"""
		if self.is_capturing_start:
			self.cfg["hotkey_start"] = combination
			self.start_display.SetValue(combination)
			self.is_capturing_start = False
			self.start_display.SetFocus()

		elif self.is_capturing_stop:
			self.cfg["hotkey_stop"] = combination
			self.stop_display.SetValue(combination)
			self.is_capturing_stop = False
			self.stop_display.SetFocus()

	def on_hotkey_error(self):
		"""
		Si hubo error al registrar, se restaura la hotkey anterior.
		"""
		if self.is_capturing_start:
			self.start_display.SetValue(self.cfg["hotkey_start"])
			self.is_capturing_start = False
		elif self.is_capturing_stop:
			self.stop_display.SetValue(self.cfg["hotkey_stop"])
			self.is_capturing_stop = False

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

		return changed


class OptionsDialog(wx.Dialog):
	"""
	Diálogo de opciones con un Notebook: General y Teclado.
	"""
	def __init__(self, parent):
		super().__init__(parent, title=_("Opciones"), style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

		sizer = wx.BoxSizer(wx.VERTICAL)
		# Podrías usar wx.Notebook, wx.Listbook, etc. Aquí seguimos tu estilo original.
		notebook = wx.Listbook(self)

		self.general_panel = GeneralPanel(notebook)
		self.keyboard_panel = KeyboardPanel(notebook)

		notebook.AddPage(self.general_panel, _("General"))
		notebook.AddPage(self.keyboard_panel, _("Teclado"))

		sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 10)

		btn_sizer = wx.StdDialogButtonSizer()
		ok_btn = wx.Button(self, wx.ID_OK, label=_("Aceptar"))
		cancel_btn = wx.Button(self, wx.ID_CANCEL, label=_("Cancelar"))
		btn_sizer.AddButton(ok_btn)
		btn_sizer.AddButton(cancel_btn)
		btn_sizer.Realize()
		sizer.Add(btn_sizer, 0, wx.ALL|wx.EXPAND, 10)

		self.SetSizerAndFit(sizer)
		self.Centre()

	def on_hotkey_captured(self, combination):
		self.keyboard_panel.on_hotkey_captured(combination)

	def on_hotkey_error(self):
		self.keyboard_panel.on_hotkey_error()

	def save_all_settings2(self):
		"""
		Guarda la configuración en ambos paneles.
		Retorna una tupla (general_changed, keyboard_changed).
		
		Se llama desde interface.py al aceptar el diálogo.
		"""
		general_changed = self.general_panel.save_settings()
		keyboard_changed = self.keyboard_panel.save_settings()
		return (general_changed, keyboard_changed)
