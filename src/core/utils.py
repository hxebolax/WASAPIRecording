#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Utilidades de Ruta

Este módulo proporciona funciones para obtener el directorio base de la aplicación, 
ya sea cuando se ejecuta como un script de Python o como un ejecutable empaquetado 
(utilizando herramientas como PyInstaller).

Funciones:
- get_base_path: Devuelve el directorio base dependiendo de si la aplicación está empaquetada 
  o en modo de desarrollo.

Características:
- Maneja el caso de aplicaciones empaquetadas con PyInstaller, devolviendo la ruta del ejecutable.
- Proporciona una ruta base consistente para cargar recursos o configuraciones.

Dependencias:
- os: Gestión de rutas y directorios.
- sys: Detección del entorno de ejecución (empaquetado o no).

"""

import os
import sys

def get_base_path():
	"""
	Obtiene el directorio base donde se encuentra el ejecutable o script.
	"""
	if getattr(sys, 'frozen', False):  # Si el script está empaquetado con PyInstaller
		return os.path.dirname(sys.executable)
	else:
		return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
