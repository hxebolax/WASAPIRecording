import gettext
import os
from core.config import get_translation_path, get_default_language, set_language_in_config

class I18n:
	def __init__(self):
		"""
		Inicializa el sistema de traducción.
		"""
		self.current_lang = get_default_language()
		self.translator = None
		self._load_language(self.current_lang)

	def _load_language(self, lang_code):
		"""
		Carga las traducciones para un idioma dado.
		"""
		locales_path = get_translation_path()
		try:
			self.translator = gettext.translation(
				"app", locales_path, languages=[lang_code], fallback=True
			)
			self.translator.install()
		except FileNotFoundError:
			gettext.install("app", locales_path)

	def set_language(self, lang_code):
		"""
		Cambia el idioma actual de la aplicación.
		"""
		self._load_language(lang_code)
		self.current_lang = lang_code
		set_language_in_config(lang_code)
