#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada de la aplicación. Inicia la interfaz gráfica.
"""
import os
import wx
import shutil
from core.utils import get_base_path

# Ruta del directorio de logs
LOGS_DIR = os.path.join(get_base_path(), "logs")

def limpiar_directorio_logs(directorio):
	"""
	Elimina todos los archivos en un directorio dado.

	Args:
		directorio (str): Ruta al directorio que contiene los archivos de log.
	"""
	if not os.path.exists(directorio):
		os.makedirs(directorio)  # Crear el directorio si no existe
	else:
		for archivo in os.listdir(directorio):
			ruta_archivo = os.path.join(directorio, archivo)
			try:
				if os.path.isfile(ruta_archivo) or os.path.islink(ruta_archivo):
					os.remove(ruta_archivo)  # Eliminar el archivo o enlace simbólico
				elif os.path.isdir(ruta_archivo):
					shutil.rmtree(ruta_archivo)  # Eliminar subdirectorios si existen
			except Exception as e:
				pass

def main():
	"""
	Función principal para iniciar la aplicación.
	"""
	from core.i18n import I18n
	try:
		logger.log_action("Iniciando la aplicación de Audio Recorder...")

		# Inicializar la internacionalización
		i18n = I18n()
		logger.log_action("Internacionalización inicializada correctamente.")

		# Importar e iniciar la interfaz gráfica
		from ui.interface import AudioRecorderApp
		app = AudioRecorderApp(i18n)
		logger.log_action("Interfaz gráfica iniciada. Entrando en el bucle principal.")
		app.MainLoop()
	except SystemExit:
		logger.log_action("La aplicación se cerró normalmente.")
	except Exception as e:
		logger.log_error(f"Se produjo un error inesperado: {e}")
		raise  # Re-lanzar el error para depuración si es necesario

if __name__ == "__main__":
	# Limpiar el directorio de logs antes de iniciar el logger
	limpiar_directorio_logs(LOGS_DIR)
	# Crear una instancia global de Logger
	from core.logger import Logger  # Importa la clase Logger
	logger = Logger()
	logger.log_action("Ejecutando el módulo principal de la aplicación.")
	main()
