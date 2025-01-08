#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para manejo de hotkeys globales en Windows.

Este módulo permite capturar combinaciones de teclas a nivel global utilizando un hook
de teclado de bajo nivel. Proporciona funcionalidades para definir, validar y registrar 
combinaciones de hotkeys, bloquear combinaciones específicas como Alt+F4 durante la captura, 
y guardar/cargar configuraciones de hotkeys.

Funciones principales:
- Capturar combinaciones de teclas globales.
- Validar que las combinaciones cumplan con ciertos criterios.
- Guardar y cargar hotkeys desde un archivo de configuración.
- Manejar eventos asociados a hotkeys para su registro y validación.
"""
import wx
import json
import os
import ctypes
import atexit
from ctypes import wintypes
from core.config import load_config, save_config, get_base_path, play_beep
from core.logger import Logger
from ui.widgets import mensaje

logger = Logger(log_dir=os.path.join(get_base_path(), "logs"))

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

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

# Rangos de teclas principales permitidas
# F1..F12, 0..9, A..Z excepto Ñ
ALLOWED_MAIN_KEYS = {
	"F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12",
	"0","1","2","3","4","5","6","7","8","9",
	"A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P",
	"Q","R","S","T","U","V","W","X","Y","Z"
}

VK_NAMES = {
	0xA0: "LeftShift", 0xA1: "RightShift",
	0xA2: "LeftCtrl", 0xA3: "RightCtrl",
	0xA4: "LeftAlt",  0xA5: "RightAlt",

	0x41: "A", 0x42: "B", 0x43: "C", 0x44: "D", 0x45: "E", 0x46: "F", 0x47: "G",
	0x48: "H", 0x49: "I", 0x4A: "J", 0x4B: "K", 0x4C: "L", 0x4D: "M", 0x4E: "N",
	0x4F: "O", 0x50: "P", 0x51: "Q", 0x52: "R", 0x53: "S", 0x54: "T", 0x55: "U",
	0x56: "V", 0x57: "W", 0x58: "X", 0x59: "Y", 0x5A: "Z",

	0x30: "0", 0x31: "1", 0x32: "2", 0x33: "3", 0x34: "4", 0x35: "5", 0x36: "6",
	0x37: "7", 0x38: "8", 0x39: "9",

	0x70: "F1", 0x71: "F2", 0x72: "F3", 0x73: "F4", 0x74: "F5", 0x75: "F6",
	0x76: "F7", 0x77: "F8", 0x78: "F9", 0x79: "F10", 0x7A: "F11", 0x7B: "F12",
}

def low_level_keyboard_proc(nCode, wParam, lParam):
	"""
	Procesa eventos del hook de teclado para capturar combinaciones de teclas.

	:param nCode: Código de evento recibido.
	:param wParam: Tipo de mensaje del evento (por ejemplo, WM_KEYDOWN).
	:param lParam: Información adicional del evento, incluyendo el código de la tecla.
	:return: Llama al siguiente hook en la cadena o bloquea el evento.
	"""
	global is_capturing, current_combination, teclas_presionadas, captura_completa

	if nCode == 0 and is_capturing and not captura_completa:
		keyboard = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
		key_code = keyboard.vkCode

		# Bloquear Alt+F4 mientras capturamos
		if wParam == WM_KEYDOWN:
			# Detectamos si es Alt+F4
			if (0x73 == key_code) and (0x12 in teclas_presionadas or 0xA4 in teclas_presionadas or 0xA5 in teclas_presionadas):
				# 0x73 = F4, 0x12=VK_MENU(Alt), 0xA4=LeftAlt, 0xA5=RightAlt
				logger.log_action("Se bloquea Alt+F4 durante la captura de hotkeys.")
				return 1  # Bloqueamos

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

def get_key_name(vk_code):
	"""
	Obtiene el nombre de una tecla a partir de su código virtual.

	:param vk_code: Código virtual de la tecla.
	:return: Nombre de la tecla o `None` si no es reconocida.
	"""
	special_keys = {
		0xA0: "Shift", 0xA1: "Shift",
		0xA2: "Ctrl",  0xA3: "Ctrl",
		0xA4: "Alt",   0xA5: "Alt",
	}
	if vk_code in special_keys:
		return special_keys[vk_code]
	if vk_code in VK_NAMES:
		return VK_NAMES[vk_code]
	return None

def validate_combination(combination):
	"""
	Valida que una combinación de teclas cumpla con los requisitos mínimos:
	- Al menos dos modificadores (Ctrl, Shift, Alt).
	- Una única tecla principal válida.

	:param combination: Combinación de teclas en formato cadena (por ejemplo, "Ctrl+Shift+F1").
	:return: `True` si es válida, `False` en caso contrario.
	"""
	parts = combination.split("+")
	modifiers = {"Ctrl","Shift","Alt"}
	# Contar modificadores
	mod_count = sum(1 for p in parts if p in modifiers)
	# Buscar las "partes" que no son mod
	main_keys = [p for p in parts if p not in modifiers]

	if mod_count < 2:
		return False

	if len(main_keys) != 1:
		return False

	# Validar que el main_key esté en ALLOWED_MAIN_KEYS
	if main_keys[0].upper() not in ALLOWED_MAIN_KEYS:
		return False

	return True

def process_hotkey_result(combination):
	"""
	Procesa el resultado de una combinación de teclas capturada, validándola y notificando
a la interfaz de usuario si es válida o no.

	:param combination: Combinación de teclas capturada.
	"""
	global captura_completa
	try:
		parent_dialog = wx.GetActiveWindow()
		if hasattr(parent_dialog, "on_hotkey_captured"):
			if not validate_combination(combination):
				logger.log_error("Combinación no válida.")
				wx.CallAfter(mensaje, None, _("La combinación debe tener al menos 2 modificadores (Ctrl,Shift,Alt) y 1 tecla principal válida."),
					_("Error"), style=wx.OK | wx.ICON_ERROR)
				wx.CallAfter(parent_dialog.on_hotkey_error)
				return

			modifiers, key_code = parse_hotkey(combination)
			if not can_register_hotkey(parent_dialog, modifiers, key_code):
				logger.log_error(f"La combinación está en uso: {combination}")
				wx.CallAfter(mensaje, None, _("La combinación está en uso: {}").format(combination), _("Error"),
					style=wx.OK | wx.ICON_ERROR)
				wx.CallAfter(parent_dialog.on_hotkey_error)
			else:
				logger.log_action(f"Hotkey capturada correctamente: {combination}")
				wx.CallAfter(parent_dialog.on_hotkey_captured, combination)
	except Exception as e:
		logger.log_error(f"Error al procesar la combinación: {e}")

def install_hook():
	"""
	Instala el hook de teclado global para capturar eventos de teclado de bajo nivel.
	"""
	global keyboard_hook, hook_proc
	try:
		hook_proc_type = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p)
		hook_proc = hook_proc_type(low_level_keyboard_proc)
		keyboard_hook = ctypes.windll.user32.SetWindowsHookExW(
			WH_KEYBOARD_LL,
			hook_proc,
			ctypes.windll.kernel32.GetModuleHandleW(None),
			0
		)
		if not keyboard_hook:
			raise OSError("No se pudo instalar el hook de teclado.")
		logger.log_action("Hook de teclado instalado correctamente.")
		atexit.register(uninstall_hook)
	except Exception as e:
		logger.log_error(f"Error al instalar el hook: {e}")
		uninstall_hook()

def uninstall_hook():
	"""
	Desinstala el hook de teclado global y libera los recursos asociados.
	"""
	global keyboard_hook
	if keyboard_hook:
		ctypes.windll.user32.UnhookWindowsHookEx(keyboard_hook)
		logger.log_action("Hook de teclado desinstalado.")
		keyboard_hook = None

def start_capturing():
	"""
	Inicia la captura de combinaciones de teclas y configura el hook de teclado global.
	"""
	global is_capturing, current_combination, teclas_presionadas, captura_completa
	current_combination = []
	teclas_presionadas.clear()
	captura_completa = False
	is_capturing = True
	install_hook()
	play_beep(1000, 200)
	logger.log_action("Inicio de captura de hotkeys.")

def stop_capturing():
	"""
	Finaliza la captura de combinaciones de teclas y desinstala el hook de teclado global.
	"""
	global is_capturing
	is_capturing = False
	uninstall_hook()
	play_beep(500, 200)
	logger.log_action("Captura de hotkeys finalizada.")

def parse_hotkey(hotkey):
	"""
	Convierte una combinación de teclas en modificadores y un código de tecla.

	:param hotkey: Combinación de teclas en formato cadena.
	:return: Tupla con modificadores (como bandera) y el código de tecla.
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
	Verifica si una combinación de hotkey puede ser registrada.

	:param window: Ventana wxPython donde se intenta registrar la hotkey.
	:param modifiers: Modificadores (Ctrl, Alt, Shift) en formato de bandera.
	:param key_code: Código de la tecla principal.
	:return: `True` si la hotkey puede ser registrada, `False` en caso contrario.
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
	Carga las hotkeys desde el archivo de configuración. Si no existen, se crean con valores predeterminados.

	:return: Diccionario con las hotkeys cargadas.
	"""
	config_file = os.path.join(get_base_path(), "WASAPIRecording.dat")
	cfg = load_config(config_file)

	if "hotkey_start" not in cfg:
		cfg["hotkey_start"] = "Ctrl+Shift+F1"
	if "hotkey_stop" not in cfg:
		cfg["hotkey_stop"] = "Ctrl+Shift+F2"
	if "hotkey_pause" not in cfg:
		cfg["hotkey_pause"] = "Ctrl+Shift+F3"
	if "hotkey_cancel" not in cfg:
		cfg["hotkey_cancel"] = "Ctrl+Shift+F4"

	logger.log_action("Hotkeys cargadas desde la configuración.")
	return cfg

def save_hotkeys_to_config(start, stop, pause, cancel):
	"""
	Guarda las hotkeys proporcionadas en el archivo de configuración.

	:param start: Combinación de teclas para iniciar.
	:param stop: Combinación de teclas para detener.
	:param pause: Combinación de teclas para pausar.
	:param cancel: Combinación de teclas para cancelar.
	"""
	config_file = os.path.join(get_base_path(), "WASAPIRecording.dat")
	cfg = load_config(config_file)

	cfg["hotkey_start"] = start
	cfg["hotkey_stop"] = stop
	cfg["hotkey_pause"] = pause
	cfg["hotkey_cancel"] = cancel

	save_config(config_file, cfg)
	logger.log_action("Hotkeys guardadas en la configuración.")
