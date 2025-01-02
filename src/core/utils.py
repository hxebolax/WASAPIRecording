#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Utilidades de Ruta

Este módulo proporciona funciones para gestionar rutas en la aplicación, permitiendo 
identificar el directorio base desde el cual se ejecuta la aplicación. Es útil tanto 
en modo de desarrollo como en aplicaciones empaquetadas con herramientas como PyInstaller.

Funciones:
- `get_base_path`: Obtiene el directorio base de la aplicación.
- `limpiar_directorio_logs`: Limpia un directorio de logs eliminando todos sus archivos.

Características:
- Maneja el caso de aplicaciones empaquetadas con PyInstaller, devolviendo la ruta del ejecutable.
- Proporciona una forma consistente de trabajar con rutas para cargar o eliminar recursos.
- Crea directorios automáticamente si no existen.

Dependencias:
- `os`: Gestión de rutas y directorios.
- `sys`: Detección del entorno de ejecución (empaquetado o desarrollo).
- `shutil`: Manipulación de directorios y eliminación de contenido.
"""
import os
import sys
import shutil

def get_base_path():
	"""
	Obtiene el directorio base donde se encuentra el ejecutable o el script.

	Si la aplicación está empaquetada (con PyInstaller, por ejemplo), retorna la ruta
	del ejecutable. En caso contrario, retorna la ruta del directorio del script en 
	modo de desarrollo.

	:return: Cadena con la ruta del directorio base.
	"""
	if getattr(sys, 'frozen', False):  # Si el script está empaquetado con PyInstaller
		return os.path.dirname(sys.executable)
	else:
		return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def limpiar_directorio_logs(directorio):
	"""
	Elimina todos los archivos y subdirectorios en el directorio especificado.

	Si el directorio no existe, lo crea automáticamente.

	:param directorio: Ruta al directorio que contiene los archivos de log.
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
