#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Diálogo y Notificaciones Accesibles.

Proporciona:
- Un cuadro de diálogo personalizado con iconos, sonidos y botones según el estilo.
- Funciones auxiliares para mostrar mensajes y notificaciones en la bandeja del sistema.
"""

import wx
import wx.adv
import winsound

class AccessibleDialogMenssage(wx.Dialog):
	"""
	Cuadro de diálogo personalizado con mejor accesibilidad para lectores de pantalla.
	Soporta asignar un botón por defecto (NO_DEFAULT) si se desea que 'No' o 'Cancelar' sea el predeterminado.
	"""
	def __init__(self, parent, message, caption='Mensaje', style=wx.OK | wx.ICON_INFORMATION):
		"""
		Constructor del diálogo accesible.

		:param parent: Ventana padre.
		:param message: Texto a mostrar en el cuadro de diálogo.
		:param caption: Título del diálogo.
		:param style: Estilos combinados (wx.OK, wx.CANCEL, wx.YES_NO, wx.NO_DEFAULT, etc.).
		"""
		super().__init__(parent, title=caption, style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)

		main_sizer = wx.BoxSizer(wx.VERTICAL)

		self._play_sound(style)

		icon = None
		if style & wx.ICON_ERROR:
			icon = wx.ART_ERROR
		elif style & wx.ICON_WARNING:
			icon = wx.ART_WARNING
		elif style & wx.ICON_INFORMATION:
			icon = wx.ART_INFORMATION
		elif style & wx.ICON_QUESTION:
			icon = wx.ART_QUESTION

		if icon:
			icon_bitmap = wx.ArtProvider.GetBitmap(icon, wx.ART_MESSAGE_BOX, (32, 32))
			icon_ctrl = wx.StaticBitmap(self, bitmap=icon_bitmap)
			main_sizer.Add(icon_ctrl, 0, wx.ALL | wx.ALIGN_CENTER, 10)

		message_ctrl = wx.StaticText(self, label=message)
		message_ctrl.Wrap(300)
		main_sizer.Add(message_ctrl, 0, wx.ALL | wx.EXPAND, 10)

		button_sizer = self._create_button_sizer(style)
		main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 10)

		self.SetSizerAndFit(main_sizer)
		self.Centre()

	def _play_sound(self, style):
		"""
		Reproduce un sonido de sistema según el tipo de icono (Error, Warning, Info, Question).

		:param style: Estilos combinados que indican el tipo de icono.
		"""
		if style & wx.ICON_ERROR:
			winsound.MessageBeep(winsound.MB_ICONHAND)
		elif style & wx.ICON_WARNING:
			winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
		elif style & wx.ICON_INFORMATION:
			winsound.MessageBeep(winsound.MB_ICONASTERISK)
		elif style & wx.ICON_QUESTION:
			winsound.MessageBeep(winsound.MB_ICONQUESTION)

	def _create_button_sizer(self, style):
		"""
		Crea los botones según el style (YES_NO, OK, CANCEL, etc.) y asocia los eventos.

		:param style: Estilos combinados.
		:return: Sizer con los botones correspondientes.
		"""
		button_sizer = wx.BoxSizer(wx.HORIZONTAL)

		self.yes_button = None
		self.no_button = None
		self.ok_button = None
		self.cancel_button = None

		if style & wx.YES_NO:
			self.yes_button = wx.Button(self, id=wx.ID_YES, label=get_label(wx.ID_YES))
			self.yes_button.Bind(wx.EVT_BUTTON, self._on_close)
			button_sizer.Add(self.yes_button, 0, wx.ALL, 5)

			self.no_button = wx.Button(self, id=wx.ID_NO, label=get_label(wx.ID_NO))
			self.no_button.Bind(wx.EVT_BUTTON, self._on_close)
			button_sizer.Add(self.no_button, 0, wx.ALL, 5)

		if style & wx.OK and not (style & wx.YES_NO):
			self.ok_button = wx.Button(self, id=wx.ID_OK, label=get_label(wx.ID_OK))
			self.ok_button.Bind(wx.EVT_BUTTON, self._on_close)
			button_sizer.Add(self.ok_button, 0, wx.ALL, 5)

		if style & wx.CANCEL and not (style & wx.YES_NO):
			self.cancel_button = wx.Button(self, id=wx.ID_CANCEL, label=get_label(wx.ID_CANCEL))
			self.cancel_button.Bind(wx.EVT_BUTTON, self._on_close)
			button_sizer.Add(self.cancel_button, 0, wx.ALL, 5)

		self._assign_default_button(style)
		return button_sizer

	def _assign_default_button(self, style):
		"""
		Asigna el botón por defecto (Sí/OK o No/Cancelar) según wx.NO_DEFAULT.

		:param style: Estilos combinados que determinan la configuración de botones.
		"""
		if style & wx.YES_NO:
			if style & wx.NO_DEFAULT and self.no_button:
				self.SetDefaultItem(self.no_button)
				self.no_button.SetFocus()
			else:
				if self.yes_button:
					self.SetDefaultItem(self.yes_button)
		else:
			if (style & wx.NO_DEFAULT) and self.cancel_button:
				self.SetDefaultItem(self.cancel_button)
			else:
				if self.ok_button:
					self.SetDefaultItem(self.ok_button)

	def _on_close(self, event):
		"""
		Cierra el diálogo devolviendo el valor correspondiente al botón (OK, CANCEL, YES, NO).

		:param event: Evento de clic en botón.
		"""
		id_to_style = {
			wx.ID_OK: wx.OK,
			wx.ID_CANCEL: wx.CANCEL,
			wx.ID_YES: wx.YES,
			wx.ID_NO: wx.NO
		}
		self.EndModal(id_to_style.get(event.GetId(), event.GetId()))

def get_label(button_id):
	"""
	Devuelve una etiqueta con atajo en español para un botón dado, según su id.

	:param button_id: Identificador del botón (wx.ID_OK, wx.ID_CANCEL, etc.).
	:return: Cadena con la etiqueta traducida y atajo de teclado.
	"""
	if button_id == wx.ID_OK:
		return _("&Aceptar")
	elif button_id == wx.ID_CANCEL:
		return _("&Cancelar")
	elif button_id == wx.ID_YES:
		return _("&Sí")
	elif button_id == wx.ID_NO:
		return _("&No")
	else:
		return ""

def mensaje(parent, message, caption='Mensaje', style=wx.OK | wx.ICON_INFORMATION):
	"""
	Crea y muestra un diálogo accesible con iconos, sonidos y botones según el estilo.
	Devuelve el resultado de ShowModal() (wx.OK, wx.CANCEL, wx.YES, wx.NO, etc.).

	:param parent: Ventana padre (o None).
	:param message: Cadena de texto con el mensaje a mostrar.
	:param caption: Título del cuadro de diálogo.
	:param style: Estilos combinados (wx.OK, wx.CANCEL, wx.YES_NO, wx.NO_DEFAULT, etc.).
	:return: Entero que indica qué botón se pulsó (ej. wx.YES, wx.NO, wx.OK, wx.CANCEL).
	"""
	dialog = AccessibleDialogMenssage(parent, message, caption, style)
	result = dialog.ShowModal()
	dialog.Destroy()
	return result

def notification_area(title, message, flag, timeout=5):
	"""
	Muestra una notificación en el área de notificaciones del sistema.

	:param title: Título de la notificación.
	:param message: Texto del mensaje a mostrar.
	:param flag: Bandera que indica el tipo de ícono (ej. wx.ICON_INFORMATION).
	:param timeout: Tiempo en segundos antes de que la notificación desaparezca.
	"""
	notify = wx.adv.NotificationMessage(
		title=title,
		message=message,
		parent=None,
		flags=flag
	)
	notify.Show(timeout=timeout)
