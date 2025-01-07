#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Este módulo actúa como punto de entrada para la aplicación de WASAPIRecording.
Se encarga de configurar el entorno inicial, como la limpieza de logs, 
la inicialización de la internacionalización, y el arranque de la interfaz gráfica.
"""
import os
import wx
from core.utils import get_base_path, limpiar_directorio_logs

# Ruta del directorio de logs
LOGS_DIR = os.path.join(get_base_path(), "logs")

def main():
	"""
	Función principal que inicializa y ejecuta la aplicación.

	Realiza las siguientes tareas:
	- Configura la librería COM en sistemas Windows para la gestión de componentes.
	- Inicializa la configuración de internacionalización para el soporte multilingüe.
	- Lanza la interfaz gráfica principal de la aplicación y entra en su bucle de eventos.
	- Maneja excepciones para registrar errores y finalizar la aplicación correctamente.
	"""
	# Inicializar COM explícitamente en Windows
	try:
		import pythoncom
		pythoncom.CoInitialize()  # o CoInitializeEx(0)
		logger.log_action("Librería pythoncom inicializada correctamente.")
	except Exception as e:
		logger.log_error(f"Error al inicializar COM: {e}")
	from core.i18n import I18n
	try:
		logger.log_action("Iniciando la aplicación WASAPIRecording...")

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
	"""
	Punto de entrada del script.

	Se encarga de realizar las siguientes tareas:
	- Limpia el directorio de logs al inicio de la ejecución.
	- Configura un sistema de registro de eventos para toda la aplicación.
	- Llama a la función `main` para iniciar el flujo principal de la aplicación.
	"""
	# Limpiar el directorio de logs antes de iniciar el logger
	limpiar_directorio_logs(LOGS_DIR)
	# Crear una instancia global de Logger
	from core.logger import Logger  # Importa la clase Logger
	logger = Logger()
	logger.log_action("Ejecutando el módulo principal de la aplicación.")
	main()
