#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que define un diálogo para mostrar un manual de uso en un TextCtrl de solo lectura.
Incluye un botón "Aceptar" y permite cerrar el diálogo al pulsar la tecla Escape.
"""

import wx

class ManualDialog(wx.Dialog):
	"""
	Diálogo para mostrar el contenido de un manual en un cuadro de texto multilinea.
	"""

	def __init__(self, parent, manual_text):
		"""
		Inicializa el diálogo con el manual.

		:param parent: Referencia a la ventana padre (puede ser None).
		:param manual_text: Cadena de texto que contiene todo el manual a mostrar.
		"""
		super().__init__(
			parent, 
			title=_("Manual de Uso"), 
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
		)

		# Creamos un panel principal
		panel = wx.Panel(self)

		# Creamos un sizer vertical para acomodar los elementos
		main_sizer = wx.BoxSizer(wx.VERTICAL)

		# Etiqueta que describe el propósito
		label = wx.StaticText(panel, label=_("&Manual de Uso:"))
		main_sizer.Add(label, 0, wx.ALL, 10)

		# Campo de texto multilinea de solo lectura
		self.text_ctrl = wx.TextCtrl(
			panel,
			value=manual_text,
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_BESTWRAP
		)
		main_sizer.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 10)

		# Sizer para el botón "Aceptar"
		btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
		btn_ok = wx.Button(panel, wx.ID_OK, label="Aceptar")
		btn_ok.Bind(wx.EVT_BUTTON, self.on_ok_clicked)
		btn_sizer.Add(btn_ok, 0, wx.ALL | wx.CENTER, 5)

		main_sizer.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 5)

		# Asignamos el sizer al panel y ajustamos
		panel.SetSizer(main_sizer)
		main_sizer.Fit(self)

		# Fijamos un tamaño mínimo al diálogo y lo centramos
		self.SetMinSize((600, 400))
		self.Centre()

		# Permite cerrar con Escape (asocia el ESC con el botón OK)
		self.SetEscapeId(wx.ID_OK)

	def on_ok_clicked(self, event):
		"""
		Maneja el clic en el botón "Aceptar" cerrando el diálogo.
		"""
		self.EndModal(wx.ID_OK)
