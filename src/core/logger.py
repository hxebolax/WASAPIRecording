#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo Logger

Este módulo proporciona una clase para gestionar el registro de eventos, acciones, 
y errores en una aplicación. Facilita la escritura de logs tanto en consola como 
en archivos de texto y captura excepciones no controladas para un diagnóstico más completo.

Funciones principales:
- Registrar acciones informativas, errores y eventos críticos.
- Configurar un sistema de logging que escriba tanto en un archivo como en la consola.
- Capturar y registrar excepciones no controladas en un archivo de traza detallada.

Clases:
- Logger: Clase principal que maneja el sistema de logging y la captura de excepciones.

Características:
- Genera automáticamente un directorio para guardar logs si no existe.
- Captura excepciones globales no controladas con `sys.excepthook`.
- Registra mensajes en distintos niveles: INFO, WARNING, ERROR y CRITICAL.
- Crea un archivo adicional para registrar las trazas de excepciones (`error_traceback.log`).

Dependencias:
- logging: Biblioteca estándar de Python para manejo de logs.
- os: Gestión de directorios y rutas.
- sys: Captura de excepciones globales y salida estándar.
- traceback: Generación de trazas detalladas de excepciones.
"""
import logging
import os
import sys
import traceback

class Logger:
	"""
	Clase para manejar logs y capturar errores en un archivo de texto.

	Esta clase configura un sistema de logging que escribe mensajes tanto en consola como 
	en un archivo. Además, captura excepciones globales no controladas y las registra con 
	trazas detalladas en un archivo de error.
	"""
	def __init__(self, log_dir="logs", log_file="app.log"):
		"""
		Inicializa el logger y configura el sistema de registro.

		:param log_dir: Directorio donde se guardarán los logs.
		:param log_file: Nombre del archivo de log principal.
		"""
		self.log_dir = log_dir
		self.log_file = os.path.join(log_dir, log_file)

		# Crear el directorio si no existe
		os.makedirs(self.log_dir, exist_ok=True)

		# Configuración del logger
		logging.basicConfig(
			level=logging.DEBUG,
			format="%(asctime)s - %(levelname)s - %(message)s",
			handlers=[
				logging.FileHandler(self.log_file, encoding="utf-8"),
				logging.StreamHandler(sys.stdout)
			]
		)

		# Configurar el manejo de excepciones no controladas
		sys.excepthook = self._handle_exception

	def log_action(self, message):
		"""
		Registra una acción o evento en el log (nivel INFO).

		:param message: Mensaje de acción a registrar.
		"""
		logging.info(message)

	def log_warning(self, message):
		"""
		Registra un mensaje de advertencia en el log (nivel WARNING).

		:param message: Mensaje de advertencia a registrar.
		"""
		logging.warning(message)

	def log_error(self, error_message):
		"""
		Registra un mensaje de error en el log (nivel ERROR).

		:param error_message: Mensaje de error a registrar.
		"""
		logging.error(error_message)

	def log_critical(self, message):
		"""
		Registra un mensaje crítico en el log (nivel CRITICAL).

		:param message: Mensaje crítico a registrar.
		"""
		logging.critical(message)

	def _handle_exception(self, exc_type, exc_value, exc_traceback):
		"""
		Maneja excepciones no controladas y las registra en el archivo de log.

		:param exc_type: Tipo de excepción.
		:param exc_value: Valor de la excepción.
		:param exc_traceback: Traza de la excepción.
		"""
		if issubclass(exc_type, KeyboardInterrupt):
			# Dejar que KeyboardInterrupt salga sin loguearlo
			sys.__excepthook__(exc_type, exc_value, exc_traceback)
			return

		logging.error(
			"Excepción no capturada",
			exc_info=(exc_type, exc_value, exc_traceback)
		)

		# Guardar una traza más detallada en un archivo separado
		traceback_file = os.path.join(self.log_dir, "error_traceback.log")
		with open(traceback_file, "a", encoding="utf-8") as f:
			f.write("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
