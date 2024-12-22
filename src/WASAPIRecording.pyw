#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Punto de entrada de la aplicación. Inicia la interfaz gráfica.
"""

import wx
from core.i18n import I18n

def main():
	"""
	Función principal para iniciar la aplicación.
	"""
	try:
		i18n = I18n()
		from ui.interface import AudioRecorderApp
		app = AudioRecorderApp(i18n)
		app.MainLoop()
	except SystemExit:
		pass

if __name__ == "__main__":
	main()
