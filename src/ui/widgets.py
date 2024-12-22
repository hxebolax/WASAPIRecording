import wx
import wx.adv
import winsound

class AccessibleDialogMenssage(wx.Dialog):
	"""
	Cuadro de diálogo personalizado con mejor accesibilidad para lectores de pantalla.
	"""
	def __init__(self, parent, message, caption='Mensaje', style=wx.OK | wx.ICON_INFORMATION):
		super().__init__(parent, title=caption, style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)

		main_sizer = wx.BoxSizer(wx.VERTICAL)

		self._play_sound(style)
		icon = None
		if style & wx.ICON_INFORMATION:
			icon = wx.ART_INFORMATION
		elif style & wx.ICON_WARNING:
			icon = wx.ART_WARNING
		elif style & wx.ICON_ERROR:
			icon = wx.ART_ERROR
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
		if style & wx.ICON_ERROR:
			winsound.MessageBeep(winsound.MB_ICONHAND)
		elif style & wx.ICON_WARNING:
			winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
		elif style & wx.ICON_INFORMATION:
			winsound.MessageBeep(winsound.MB_ICONASTERISK)
		elif style & wx.ICON_QUESTION:
			winsound.MessageBeep(winsound.MB_ICONQUESTION)

	def _create_button_sizer(self, style):
		button_sizer = wx.BoxSizer(wx.HORIZONTAL)

		if style & wx.YES_NO:
			yes_button = wx.Button(self, id=wx.ID_YES, label=get_label(wx.ID_YES))
			yes_button.Bind(wx.EVT_BUTTON, self._on_close)
			button_sizer.Add(yes_button, 0, wx.ALL, 5)

			no_button = wx.Button(self, id=wx.ID_NO, label=get_label(wx.ID_NO))
			no_button.Bind(wx.EVT_BUTTON, self._on_close)
			button_sizer.Add(no_button, 0, wx.ALL, 5)

		# Aseguramos que los botones OK y CANCEL no se añaden si ya existe YES_NO
		if style & wx.OK and not (style & wx.YES_NO):
			ok_button = wx.Button(self, id=wx.ID_OK, label=get_label(wx.ID_OK))
			ok_button.Bind(wx.EVT_BUTTON, self._on_close)
			button_sizer.Add(ok_button, 0, wx.ALL, 5)

		if style & wx.CANCEL and not (style & wx.YES_NO):
			cancel_button = wx.Button(self, id=wx.ID_CANCEL, label=get_label(wx.ID_CANCEL))
			cancel_button.Bind(wx.EVT_BUTTON, self._on_close)
			button_sizer.Add(cancel_button, 0, wx.ALL, 5)

		return button_sizer

	def _on_close(self, event):
		"""
		Finaliza el diálogo devolviendo el valor correspondiente.
		"""
		id_to_style = {
			wx.ID_OK: wx.OK,
			wx.ID_CANCEL: wx.CANCEL,
			wx.ID_YES: wx.YES,
			wx.ID_NO: wx.NO
		}
		self.EndModal(id_to_style.get(event.GetId(), event.GetId()))

def get_label(button_id):
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
	dialog = AccessibleDialogMenssage(parent, message, caption, style)
	result = dialog.ShowModal()
	dialog.Destroy()
	return result

def notification_area(title, message, flag, timeout=5):
	"""
	Muestra una notificación en el área de notificaciones del sistema.
	"""
	notify = wx.adv.NotificationMessage(
		title=title,
		message=message,
		parent=None,
		flags=flag
	)
	notify.Show(timeout=timeout)
