#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que define un diálogo para mostrar un manual de uso en un TextCtrl de solo lectura.

Permite:
- Mostrar el contenido de un manual o documentación interna de la aplicación.
- Cerrar el diálogo con el botón "Aceptar" o presionando la tecla Escape.
"""

import os
import wx
from core.logger import Logger
from core.utils import get_base_path

logger = Logger(log_dir=os.path.join(get_base_path(), "logs"))

class ManualDialog(wx.Dialog):
	"""
	Diálogo para mostrar el contenido de un manual en un cuadro de texto multilinea.
	"""
	def __init__(self, parent, manual_text):
		"""
		Inicializa el diálogo con el manual.

		:param parent: Ventana padre (puede ser None).
		:param manual_text: Cadena de texto con el contenido del manual.
		"""
		super().__init__(
			parent,
			title=_("Manual de Uso"),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)
		logger.log_action("ManualDialog: Inicializando el diálogo.")

		panel = wx.Panel(self)
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		label = wx.StaticText(panel, label=_("&Manual de Uso:"))
		main_sizer.Add(label, 0, wx.ALL, 10)
		logger.log_action("ManualDialog: Añadida etiqueta descriptiva.")

		self.text_ctrl = wx.TextCtrl(
			panel,
			value=manual_text,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_BESTWRAP
		)
		main_sizer.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 10)
		logger.log_action("ManualDialog: Campo de texto multilinea añadido.")

		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		btn_ok = wx.Button(panel, wx.ID_OK, label=_("Aceptar"))
		btn_ok.Bind(wx.EVT_BUTTON, self.on_ok_clicked)
		btn_sizer.Add(btn_ok, 0, wx.ALL | wx.CENTER, 5)
		logger.log_action("ManualDialog: Botón 'Aceptar' añadido y evento vinculado.")

		main_sizer.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)
		panel.SetSizer(main_sizer)
		main_sizer.Fit(self)

		self.SetMinSize((600, 400))
		self.Centre()
		logger.log_action("ManualDialog: Tamaño mínimo establecido y diálogo centrado.")

		self.SetEscapeId(wx.ID_OK)
		logger.log_action("ManualDialog: Configurado para cerrar con la tecla Escape.")

	def on_ok_clicked(self, event):
		"""
		Maneja el clic en el botón "Aceptar", cerrando el diálogo.

		:param event: Evento de botón OK.
		"""
		logger.log_action("ManualDialog: Botón 'Aceptar' pulsado. Cerrando diálogo.")
		self.EndModal(wx.ID_OK)
