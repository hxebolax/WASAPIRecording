#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para manejar la captura y validación de hotkeys, así como su registro global.
"""

import wx
import json
import os
import ctypes
import winsound
import atexit
from ctypes import wintypes
from core.config import load_config, save_config, get_base_path
from ui.widgets import mensaje

# Constantes de hook y eventos de teclado
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

# Variables globales del hook
keyboard_hook = None
hook_proc = None
is_capturing = False
current_combination = []
teclas_presionadas = set()
captura_completa = False

user32 = ctypes.windll.user32

class KBDLLHOOKSTRUCT(ctypes.Structure):
	_fields_ = [
		("vkCode", wintypes.DWORD),
		("scanCode", wintypes.DWORD),
		("flags", wintypes.DWORD),
		("time", wintypes.DWORD),
		("dwExtraInfo", wintypes.ULONG),
	]

def _(text):
	return text

# Mapa reducido de teclas virtuales compatibles con wx.RegisterHotKey
VK_NAMES = {
	# Modificadores
	0xA0: "LeftShift", 0xA1: "RightShift",
	0xA2: "LeftCtrl", 0xA3: "RightCtrl",
	0xA4: "LeftAlt", 0xA5: "RightAlt",

	# Letras estándar (A-Z)
	0x41: "A", 0x42: "B", 0x43: "C", 0x44: "D", 0x45: "E", 0x46: "F", 0x47: "G",
	0x48: "H", 0x49: "I", 0x4A: "J", 0x4B: "K", 0x4C: "L", 0x4D: "M", 0x4E: "N",
	0x4F: "O", 0x50: "P", 0x51: "Q", 0x52: "R", 0x53: "S", 0x54: "T", 0x55: "U",
	0x56: "V", 0x57: "W", 0x58: "X", 0x59: "Y", 0x5A: "Z",

	# Números estándar (0-9)
	0x30: "0", 0x31: "1", 0x32: "2", 0x33: "3", 0x34: "4", 0x35: "5", 0x36: "6",
	0x37: "7", 0x38: "8", 0x39: "9",

	# Teclas de función
	0x70: "F1", 0x71: "F2", 0x72: "F3", 0x73: "F4", 0x74: "F5", 0x75: "F6",
	0x76: "F7", 0x77: "F8", 0x78: "F9", 0x79: "F10", 0x7A: "F11", 0x7B: "F12",
}

def get_key_name(vk_code):
	"""
	Convierte el código de tecla a nombre comprensible.
	"""
	special_keys = {
		0xA0: "Shift", 0xA1: "Shift",
		0xA2: "Ctrl", 0xA3: "Ctrl",
		0xA4: "Alt", 0xA5: "Alt",
	}

	if vk_code in special_keys:
		return special_keys[vk_code]
	if vk_code in VK_NAMES:
		return VK_NAMES[vk_code]
	return None

def low_level_keyboard_proc(nCode, wParam, lParam):
	"""
	Callback del hook de teclado global.
	"""
	global is_capturing, current_combination, teclas_presionadas, captura_completa

	if nCode == 0 and is_capturing and not captura_completa:
		keyboard = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
		key_code = keyboard.vkCode

		if wParam == WM_KEYDOWN and key_code not in teclas_presionadas:
			teclas_presionadas.add(key_code)
			key_name = get_key_name(key_code)
			if key_name:
				if key_name not in current_combination:
					current_combination.append(key_name)
		elif wParam == WM_KEYUP:
			teclas_presionadas.discard(key_code)
			if not teclas_presionadas:
				captura_completa = True
				stop_capturing()
				process_hotkey_result("+".join(current_combination))
		return 1
	return ctypes.windll.user32.CallNextHookEx(keyboard_hook, nCode, wParam, lParam)

def validate_combination(combination):
	"""
	Valida que la combinación tenga al menos 2 modificadores y 1 tecla principal.
	"""
	combination_list = combination.split("+")
	if any("VK_" in key for key in combination_list):
		wx.CallAfter(mensaje, None, _("Tecla inválida detectada."), _("Error"), style=wx.OK | wx.ICON_ERROR)
		return False

	modifiers = {"Ctrl", "Shift", "Alt"}
	modifier_count = sum(1 for key in combination_list if key in modifiers)
	main_key_count = sum(1 for key in combination_list if key not in modifiers)

	return modifier_count >= 2 and main_key_count == 1

def process_hotkey_result(combination):
	"""
	Procesa el resultado de la combinación capturada.
	"""
	global captura_completa
	try:
		parent_dialog = wx.GetActiveWindow()
		if hasattr(parent_dialog, "on_hotkey_captured"):
			if not validate_combination(combination):
				wx.CallAfter(
					mensaje,
					None,
					_("La combinación debe tener al menos dos modificadores y una tecla principal."),
					_("Error"),
					style=wx.OK | wx.ICON_ERROR,
				)
				wx.CallAfter(parent_dialog.on_hotkey_error)
				return

			modifiers, key_code = parse_hotkey(combination)
			if not can_register_hotkey(parent_dialog, modifiers, key_code):
				wx.CallAfter(
					mensaje,
					None,
					_("La combinación está en uso por otra aplicación: ") + combination,
					_("Error"),
					style=wx.OK | wx.ICON_ERROR,
				)
				wx.CallAfter(parent_dialog.on_hotkey_error)
			else:
				wx.CallAfter(parent_dialog.on_hotkey_captured, combination)
	except Exception as e:
		print(f"Error al procesar la combinación: {e}")

def install_hook():
	global keyboard_hook, hook_proc
	try:
		hook_proc_type = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p)
		hook_proc = hook_proc_type(low_level_keyboard_proc)
		keyboard_hook = ctypes.windll.user32.SetWindowsHookExW(
			WH_KEYBOARD_LL,
			hook_proc,
			ctypes.windll.kernel32.GetModuleHandleW(None),
			0,
		)
		if not keyboard_hook:
			raise OSError("No se pudo instalar el hook de teclado.")
		atexit.register(uninstall_hook)
	except Exception as e:
		print(f"Error al instalar el hook: {e}")
		uninstall_hook()

def uninstall_hook():
	global keyboard_hook
	if keyboard_hook:
		ctypes.windll.user32.UnhookWindowsHookEx(keyboard_hook)
		keyboard_hook = None

def start_capturing():
	global is_capturing, current_combination, teclas_presionadas, captura_completa
	current_combination = []
	teclas_presionadas.clear()
	captura_completa = False
	is_capturing = True
	install_hook()
	winsound.Beep(1000, 200)

def stop_capturing():
	global is_capturing
	is_capturing = False
	uninstall_hook()
	winsound.Beep(500, 200)

def parse_hotkey(hotkey):
	"""
	Convierte la combinación en modificadores y código de tecla.
	"""
	modifiers = 0
	if "Ctrl" in hotkey:
		modifiers |= wx.MOD_CONTROL
	if "Alt" in hotkey:
		modifiers |= wx.MOD_ALT
	if "Shift" in hotkey:
		modifiers |= wx.MOD_SHIFT

	key = hotkey.split("+")[-1].upper()
	key_code = getattr(wx, f"WXK_{key}", None)
	if key_code is None:
		key_code = ord(key) if len(key) == 1 else 0
	return modifiers, key_code

def can_register_hotkey(window, modifiers, key_code):
	"""
	Comprueba si la combinación se puede registrar.
	"""
	temp_id = wx.NewIdRef()
	try:
		if window.RegisterHotKey(temp_id, modifiers, key_code):
			window.UnregisterHotKey(temp_id)
			return True
		return False
	except Exception:
		return False

def load_hotkeys_from_config():
	"""
	Carga las hotkeys desde WASAPIRecording.dat
	Si no existen, las crea por defecto. (Ctrl+Shift+F1 / Ctrl+Shift+F2)
	No valida ni registra aquí; esa parte se hace en interface.py
	"""
	config_file = os.path.join(get_base_path(), "WASAPIRecording.dat")
	cfg = load_config(config_file)
	if "hotkey_start" not in cfg:
		cfg["hotkey_start"] = "Ctrl+Shift+F1"
	if "hotkey_stop" not in cfg:
		cfg["hotkey_stop"] = "Ctrl+Shift+F2"
	return cfg

def save_hotkeys_to_config(hotkey_start, hotkey_stop):
	"""
	Guarda las hotkeys en WASAPIRecording.dat
	"""
	config_file = os.path.join(get_base_path(), "WASAPIRecording.dat")
	cfg = load_config(config_file)
	cfg["hotkey_start"] = hotkey_start
	cfg["hotkey_stop"] = hotkey_stop
	save_config(config_file, cfg)
