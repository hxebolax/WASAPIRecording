#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Internacionalización (I18n)

Este módulo gestiona la internacionalización de la aplicación, permitiendo cargar y cambiar
los idiomas disponibles para las traducciones. Utiliza la biblioteca `gettext` para cargar
archivos de traducción y ofrece una interfaz para cambiar el idioma durante la ejecución.

Funciones principales:
- Inicialización de las traducciones al iniciar la aplicación.
- Carga de archivos de traducción desde la ruta definida en la configuración.
- Cambio dinámico del idioma actual con manejo de errores.
- Registro de acciones y errores relacionados con la traducción utilizando el sistema de logging.

Clases:
- I18n: Clase principal que gestiona la configuración de idioma y la carga de traducciones.

Dependencias:
- gettext: Manejo de traducciones basadas en archivos `.mo`.
- core.config: Obtiene la ruta de traducciones y el idioma por defecto desde la configuración.
- core.logger: Registra acciones y errores en un archivo de logs.

"""
import gettext
import os
from core.config import get_translation_path, get_default_language, set_language_in_config
from core.logger import Logger

# Inicialización del logger
logger = Logger(log_dir=os.path.join(os.getcwd(), "logs"))

class I18n:
	def __init__(self):
		"""
		Inicializa el sistema de traducción.
		"""
		self.current_lang = get_default_language()
		self.translator = None
		logger.log_action(f"Idioma por defecto detectado: {self.current_lang}")
		self._load_language(self.current_lang)

	def _load_language(self, lang_code):
		"""
		Carga las traducciones para un idioma dado.
		
		:param lang_code: Código del idioma a cargar.
		"""
		locales_path = get_translation_path()
		try:
			self.translator = gettext.translation(
				"app", locales_path, languages=[lang_code], fallback=True
			)
			self.translator.install()
			logger.log_action(f"Traducciones cargadas para el idioma: {lang_code}")
		except FileNotFoundError:
			gettext.install("app", locales_path)
			logger.log_error(f"Archivo de traducción no encontrado para el idioma: {lang_code}. Usando valores por defecto.")

	def set_language(self, lang_code):
		"""
		Cambia el idioma actual de la aplicación.
		
		:param lang_code: Código del idioma a establecer.
		"""
		try:
			self._load_language(lang_code)
			self.current_lang = lang_code
			set_language_in_config(lang_code)
			logger.log_action(f"Idioma cambiado exitosamente a: {lang_code}")
		except Exception as e:
			logger.log_error(f"Error al cambiar el idioma a {lang_code}: {e}")
