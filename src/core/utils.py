#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
