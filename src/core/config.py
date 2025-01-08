#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para manejar la carga y guardado de configuración en un archivo JSON.

Funciones principales:
- Codificar y decodificar datos utilizando XOR y Base64 para mayor seguridad.
- Detectar el idioma del sistema operativo y configurar el idioma predeterminado.
- Guardar y cargar configuraciones desde un archivo JSON codificado.

Incluye funcionalidades para:
- Manejar claves de codificación.
- Trabajar con archivos de configuración.
- Detectar y establecer idiomas del sistema.

Se ha añadido la opción de 'buffer_size' para que el usuario pueda elegir el tamaño de buffer 
de grabación, y soporte para las siguientes hotkeys:
 - hotkey_start
 - hotkey_stop
 - hotkey_pause
 - hotkey_cancel

Adicionalmente, se contempla 'recording_dir' para la ruta de grabaciones.
"""
import json
import os
import base64
import locale
import ctypes
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

	:return: Código de idioma en formato ISO 639-1 (por ejemplo, 'es', 'en').
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

	:return: Ruta absoluta al directorio de traducciones.
	"""
	path = os.path.join(get_base_path(), "locales")
	logger.log_action(f"Ruta de traducción: {path}")
	return path

def get_default_language():
	"""
	Obtiene el idioma predeterminado desde la configuración o detecta el idioma del sistema.

	:return: Código de idioma predeterminado.
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

import os
import ctypes

def play_beep(frequency=440, duration=1000, info=True):
	"""
	Prueba el uso de ctypes para llamar a la API de Windows y reproducir un tono,
	registrando posibles errores durante su ejecución.

	:param frequency: Frecuencia del tono en Hertz (por defecto, 440 Hz).
	:param duration: Duración del tono en milisegundos (por defecto, 1000 ms).
	:return: None
	"""
	try:
		# Validar si la plataforma es compatible
		if os.name != "nt":  # Solo funciona en Windows
			raise RuntimeError("La función ctypes.Beep solo está disponible en Windows.")

		# Validar rango de frecuencia y duración
		if not (37 <= frequency <= 32767):
			raise ValueError("La frecuencia debe estar entre 37 y 32767 Hertz.")
		if duration <= 0:
			raise ValueError("La duración debe ser mayor a 0 milisegundos.")

		# Cargar la biblioteca kernel32
		kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

		# Intentar ejecutar Beep
		if info:
			logger.log_action(f"Intentando reproducir un tono: frecuencia={frequency}Hz, duración={duration}ms")
		result = kernel32.Beep(frequency, duration)
		
		# Comprobar el resultado de la función Beep
		if result == 0:  # La función Beep devuelve 0 en caso de error
			raise ctypes.WinError(ctypes.get_last_error())

		if info:
			logger.log_action("Tono reproducido exitosamente.")
	except ValueError as ve:
		# Error en los parámetros
		logger.log_error(f"Error de validación en ctypes.Beep: {ve}")
	except RuntimeError as re:
		# Error de compatibilidad de plataforma
		logger.log_error(f"Error de plataforma en ctypes.Beep: {re}")
	except Exception as e:
		# Cualquier otro error inesperado
		logger.log_error(f"Error inesperado en ctypes.Beep: {e}")
