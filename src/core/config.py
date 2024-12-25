#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para manejar la carga y guardado de configuración en un archivo JSON.
"""

import json
import os
import base64
import locale
from core.utils import get_base_path
from core.logger import Logger  # Importar Logger

# Instanciar Logger con la ubicación de logs en la raíz del proyecto
logger = Logger(log_dir=os.path.join(get_base_path(), "logs"))

# Clave generada automáticamente para codificación. Asegúrate de mantener esta clave segura.
ENCODE_KEY = "uHx2K9L9Ga92YZg7"

def xor_encrypt_decrypt(data, key):
	"""
	Realiza un XOR entre los datos y la clave para codificar/decodificar.

	:param data: Datos en forma de bytes.
	:param key: Clave como cadena.
	:return: Resultado del XOR como bytes.
	"""
	key_bytes = key.encode()
	return bytes(data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data)))

def encode_data(data):
	"""
	Codifica los datos usando XOR y Base64.

	:param data: Cadena de texto a codificar.
	:return: Cadena codificada en Base64.
	"""
	xor_result = xor_encrypt_decrypt(data.encode(), ENCODE_KEY)
	return base64.b64encode(xor_result).decode()

def decode_data(data):
	"""
	Decodifica los datos usando Base64 y XOR.

	:param data: Cadena codificada en Base64.
	:return: Cadena de texto decodificada.
	"""
	xor_result = base64.b64decode(data.encode())
	return xor_encrypt_decrypt(xor_result, ENCODE_KEY).decode()

def detect_system_language():
	"""
	Detecta el idioma del sistema operativo.
	Devuelve el código de idioma en formato ISO 639-1 (por ejemplo, 'es', 'en').
	"""
	try:
		lang, _ = locale.getdefaultlocale()
		if lang:
			logger.log_action(f"Idioma del sistema detectado: {lang}")
			return lang[:2]  # Retorna las dos primeras letras del idioma
		logger.log_action("No se detectó idioma del sistema. Usando 'es' por defecto.")
		return 'es'  # Idioma predeterminado
	except Exception as e:
		logger.log_error(f"Error al detectar idioma del sistema: {e}")
		return 'es'

def get_translation_path():
	"""
	Obtiene la ruta base donde están los archivos de traducción.
	"""
	path = os.path.join(get_base_path(), "locales")
	logger.log_action(f"Ruta de traducción: {path}")
	return path

def get_default_language():
	"""
	Obtiene el idioma predeterminado desde la configuración o detecta el idioma del sistema.
	"""
	try:
		config_file = os.path.join(get_base_path(), "WASAPIRecording.dat")
		config = load_config(config_file)
		lang = config.get("language", detect_system_language())
		logger.log_action(f"Idioma predeterminado obtenido: {lang}")
		return lang
	except Exception as e:
		logger.log_error(f"Error al obtener idioma predeterminado: {e}")
		return detect_system_language()

def set_language_in_config(lang_code):
	"""
	Guarda el idioma seleccionado por el usuario en la configuración.
	:param lang_code: Código de idioma (ejemplo: 'es', 'en').
	"""
	try:
		config_file = os.path.join(get_base_path(), "WASAPIRecording.dat")
		config = load_config(config_file)
		config["language"] = lang_code
		save_config(config_file, config)
		logger.log_action(f"Idioma guardado en la configuración: {lang_code}")
	except Exception as e:
		logger.log_error(f"Error al guardar idioma en la configuración: {e}")

def save_config(config_file, config):
	"""
	Guarda la configuración en un archivo JSON codificado.

	:param config_file: Ruta al archivo de configuración.
	:param config: Diccionario con la configuración.
	"""
	try:
		json_data = json.dumps(config, indent=4)
		encoded_data = encode_data(json_data)
		with open(config_file, "w", encoding="utf-8") as f:
			f.write(encoded_data)
		logger.log_action(f"Configuración guardada en {config_file}")
	except Exception as e:
		logger.log_error(f"Error al guardar configuración en {config_file}: {e}")

def load_config(config_file):
	"""
	Carga la configuración desde un archivo JSON codificado.
	Si no existe o hay error, retorna un diccionario vacío.

	:param config_file: Ruta al archivo de configuración.
	:return: Diccionario con la configuración o vacío si no se pudo cargar.
	"""
	try:
		if os.path.exists(config_file):
			with open(config_file, "r", encoding="utf-8") as f:
				encoded_data = f.read()
				json_data = decode_data(encoded_data)
				logger.log_action(f"Configuración cargada desde {config_file}")
				return json.loads(json_data)
		logger.log_action(f"No se encontró el archivo de configuración: {config_file}")
		return {}
	except (json.JSONDecodeError, Exception) as e:
		logger.log_error(f"Error al cargar configuración desde {config_file}: {e}")
		return {}
