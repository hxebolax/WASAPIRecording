#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de Diálogo de Actualización (UpdateDialog)

Este módulo implementa un diálogo que permite comprobar y descargar actualizaciones
almacenadas en un repositorio de GitHub, para luego instalarlas de forma automatizada.
"""

import wx
import os
import sys
import zipfile
import threading
import urllib.request
import shutil
import subprocess
from core.logger import Logger
from core.utils import get_base_path

logger = Logger(log_dir=os.path.join(get_base_path(), "logs"))

class UpdateDialog(wx.Dialog):
	"""
	Diálogo para gestionar la verificación y aplicación de actualizaciones
	basadas en GitHub. Permite:
	- Bloquear el cierre forzado (X, Alt+F4).
	- Comprobar la última versión disponible.
	- Descargar e instalar la actualización con un script BAT.
	"""
	def __init__(self, parent, repo_owner, repo_name, current_version):
		"""
		Constructor del UpdateDialog.

		:param parent: Ventana padre (puede ser None).
		:param repo_owner: Usuario u organización dueña del repositorio GitHub.
		:param repo_name: Nombre del repositorio en GitHub.
		:param current_version: Versión actual de la aplicación.
		"""
		super().__init__(parent, title=_("Actualización"), size=(500, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)
		logger.log_action("UpdateDialog: Inicializando el diálogo de actualización.")

		self.SetWindowStyleFlag(
			self.GetWindowStyleFlag()
			& ~wx.CLOSE_BOX
			& ~wx.MAXIMIZE_BOX
			& ~wx.MINIMIZE_BOX
			& ~wx.SYSTEM_MENU
		)
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
		logger.log_action("UpdateDialog: Configurado para bloquear cierre con la X y Alt+F4.")

		self.repo_owner = repo_owner
		self.repo_name = repo_name
		self.current_version = current_version
		self.cancelled = False
		self.download_thread = None

		info_label = wx.StaticText(self, label=_("&Información:"))
		self.message_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE)
		self.progress_bar = wx.Gauge(self, range=100, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
		self.progress_bar.Hide()

		self.cancel_button = wx.Button(self, label=_("Cancelar"))
		self.install_button = wx.Button(self, label=_("Instalar"))
		self.install_button.Hide()

		self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
		self.install_button.Bind(wx.EVT_BUTTON, self.on_install)

		button_sizer = wx.BoxSizer(wx.HORIZONTAL)
		button_sizer.Add(self.install_button, flag=wx.ALL, border=5)
		button_sizer.AddSpacer(10)
		button_sizer.Add(self.cancel_button, flag=wx.ALL, border=5)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(info_label, flag=wx.ALL | wx.EXPAND, border=10)
		sizer.Add(self.message_text, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
		sizer.Add(self.progress_bar, flag=wx.ALL | wx.EXPAND, border=10)
		sizer.Add(button_sizer, flag=wx.ALIGN_CENTER_HORIZONTAL)

		self.SetSizer(sizer)

		threading.Thread(target=self.check_update, daemon=True).start()
		logger.log_action("UpdateDialog: Hilo para comprobar actualizaciones iniciado.")

	def on_key_down(self, event):
		"""
		Bloquea Alt+F4 dentro del diálogo.

		:param event: Evento de teclado.
		"""
		key_code = event.GetKeyCode()
		if key_code == wx.WXK_F4 and event.AltDown():
			logger.log_action("UpdateDialog: Intento de cierre con Alt+F4 ignorado.")
			return
		event.Skip()

	def append_message(self, message):
		"""
		Agrega un texto al cuadro de información y lo sitúa al inicio.

		:param message: Cadena de texto a mostrar.
		"""
		self.message_text.Clear()
		self.message_text.AppendText(f"\n{message}\n")
		self.message_text.SetInsertionPoint(0)
		logger.log_action(f"UpdateDialog: Mensaje añadido al cuadro de texto: {message}")

	def check_update(self):
		"""
		Verifica si existe una versión más reciente en GitHub consultando la API.
		Si la hay, ofrece instalarla; si no, indica que está actualizado.
		"""
		api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
		try:
			response = urllib.request.urlopen(api_url)
			data = response.read().decode("utf-8")
			import json
			release_info = json.loads(data)

			new_version = release_info["tag_name"]
			logger.log_action(f"UpdateDialog: Versión actual: {self.current_version}, Nueva versión encontrada: {new_version}")
			if new_version > self.current_version:
				asset = next((a for a in release_info["assets"] if a["name"].endswith(".zip")), None)
				if asset:
					self.download_url = asset["browser_download_url"]
					self.asset_name = asset["name"]
					wx.CallAfter(self.show_update_prompt, new_version)
					logger.log_action("UpdateDialog: Nueva versión encontrada y prompt de actualización mostrado.")
				else:
					wx.CallAfter(self.show_no_update)
					logger.log_action("UpdateDialog: Nueva versión encontrada pero sin asset .zip disponible.")
			else:
				wx.CallAfter(self.show_no_update)
				logger.log_action("UpdateDialog: No hay actualizaciones disponibles.")
		except Exception as e:
			wx.CallAfter(self.show_error, e)
			logger.log_error(f"UpdateDialog: Error al comprobar actualizaciones: {e}")

	def show_update_prompt(self, new_version):
		"""
		Muestra al usuario la opción de instalar la nueva versión encontrada.

		:param new_version: Versión más reciente.
		"""
		message = _("Se encontró una nueva versión: {0}. ¿Desea instalarla?").format(new_version)
		self.append_message(message)
		self.install_button.Show()
		self.Layout()
		logger.log_action("UpdateDialog: Prompt de actualización mostrado al usuario.")

	def show_no_update(self):
		"""
		Indica al usuario que su aplicación ya está actualizada.
		"""
		self.append_message(_("No hay actualizaciones disponibles. Su aplicación está actualizada."))
		self.cancel_button.SetLabel(_("Cerrar"))
		logger.log_action("UpdateDialog: Mensaje de no actualización mostrado al usuario.")

	def show_error(self, error):
		"""
		Muestra un error según su tipo (red, archivos, permisos, etc.).

		:param error: Excepción capturada.
		"""
		import socket
		import ssl
		import urllib.error

		if isinstance(error, urllib.error.URLError):
			if isinstance(error.reason, socket.gaierror):
				error_message = _("No se pudo conectar al servidor. Verifique su conexión a Internet.")
			elif isinstance(error.reason, ssl.SSLError):
				error_message = _("Error en la conexión segura (SSL). Por favor, revise la configuración de seguridad de su red.")
			elif isinstance(error.reason, TimeoutError):
				error_message = _("La conexión tardó demasiado tiempo. Intente nuevamente más tarde.")
			else:
				error_message = _("Error de red desconocido: {0}").format(str(error.reason))
				self.append_message(error_message)
				self.cancel_button.SetLabel(_("Cerrar"))
				logger.log_error(f"UpdateDialog: Error de red desconocido: {error.reason}")
				return
		elif isinstance(error, FileNotFoundError):
			error_message = _("No se encontró el archivo necesario para completar la operación.")
		elif isinstance(error, IsADirectoryError):
			error_message = _("Se esperaba un archivo, pero se encontró un directorio.")
		elif isinstance(error, PermissionError):
			error_message = _("Permiso denegado. Ejecute la aplicación con los permisos adecuados.")
		elif isinstance(error, shutil.Error):
			error_message = _("Error al copiar o mover archivos. Verifique los permisos y el espacio disponible.")
		elif isinstance(error, ValueError):
			error_message = _("Se produjo un error en los datos proporcionados. Verifique la información ingresada.")
		elif isinstance(error, KeyError):
			error_message = _("Falta un elemento requerido en los datos. Verifique el formato de la información.")
		elif isinstance(error, IndexError):
			error_message = _("Se intentó acceder a un elemento fuera del rango permitido. Revise la configuración interna.")
		elif isinstance(error, ConnectionError):
			error_message = _("No se pudo establecer una conexión. Verifique su conexión a Internet.")
		elif isinstance(error, TimeoutError):
			error_message = _("La operación tardó demasiado tiempo en completarse. Inténtelo más tarde.")
		elif isinstance(error, BrokenPipeError):
			error_message = _("Se perdió la conexión con el servidor. Intente reconectarse.")
		else:
			error_message = _("Ocurrió un error inesperado: {0}").format(str(error))
			self.append_message(error_message)
			self.cancel_button.SetLabel(_("Cerrar"))
			logger.log_error(f"UpdateDialog: Error inesperado: {error}")
			return

		self.append_message(error_message + "\n{}".format(error))
		self.cancel_button.SetLabel(_("Cerrar"))
		logger.log_error(f"UpdateDialog: {error_message}")

	def on_install(self, event):
		"""
		Comienza la descarga de la actualización y muestra la barra de progreso.

		:param event: Evento de botón "Instalar".
		"""
		self.append_message(_("Descargando la actualización, esto puede tardar unos momentos..."))
		self.progress_bar.Show()
		self.install_button.Hide()
		self.Layout()
		logger.log_action("UpdateDialog: Iniciando descarga de la actualización.")

		self.download_thread = threading.Thread(target=self.download_update, daemon=True)
		self.download_thread.start()
		logger.log_action("UpdateDialog: Hilo de descarga iniciado.")

	def download_update(self):
		"""
		Descarga el archivo ZIP de la nueva versión y, si no se cancela,
		llama a extract_update() para continuar.
		"""
		try:
			dest_path = os.path.join(os.getcwd(), self.asset_name)
			with urllib.request.urlopen(self.download_url) as response, open(dest_path, "wb") as out_file:
				total_length = int(response.info()["Content-Length"])
				downloaded = 0
				block_size = 8192

				while not self.cancelled:
					buffer = response.read(block_size)
					if not buffer:
						break
					out_file.write(buffer)
					downloaded += len(buffer)
					progress = int(downloaded / total_length * 100)
					wx.CallAfter(self.progress_bar.SetValue, progress)

			if self.cancelled:
				os.remove(dest_path)
				wx.CallAfter(self.close_dialog, _("Descarga cancelada."))
				logger.log_action("UpdateDialog: Descarga cancelada por el usuario.")
			else:
				wx.CallAfter(self.extract_update, dest_path)
				logger.log_action(f"UpdateDialog: Descarga completada y archivo guardado en {dest_path}.")
		except Exception as e:
			wx.CallAfter(self.show_error, e)
			logger.log_error(f"UpdateDialog: Error durante la descarga: {e}")

	def extract_update(self, zip_path):
		"""
		Extrae el ZIP descargado a una carpeta temporal e inicia la creación del script BAT.

		:param zip_path: Ruta del archivo ZIP.
		"""
		try:
			self.append_message(_("Extrayendo la actualización..."))
			logger.log_action(f"UpdateDialog: Extrayendo archivo ZIP: {zip_path}")
			temp_dir = os.path.join(os.getcwd(), "temp-install")
			with zipfile.ZipFile(zip_path, "r") as zip_ref:
				subfolder = "WASAPIRecording/"
				for file_name in zip_ref.namelist():
					if file_name.startswith(subfolder):
						target_path = os.path.join(temp_dir, file_name[len(subfolder):])
						if not os.path.basename(target_path):
							os.makedirs(target_path, exist_ok=True)
						else:
							with open(target_path, "wb") as f:
								f.write(zip_ref.read(file_name))

			self.create_bat(temp_dir)
			os.remove(zip_path)
			logger.log_action(f"UpdateDialog: Archivo ZIP {zip_path} eliminado después de extracción.")
		except Exception as e:
			wx.CallAfter(self.show_error, e)
			logger.log_error(f"UpdateDialog: Error durante la extracción: {e}")

	def create_bat(self, temp_dir):
		"""
		Crea un archivo BAT para copiar los archivos extraídos y reiniciar la aplicación.

		:param temp_dir: Directorio temporal donde se extrajeron los archivos.
		"""
		try:
			self.append_message(_("Creando el archivo de instalación automática..."))
			logger.log_action(f"UpdateDialog: Creando archivo BAT en {temp_dir}")
			bat_path = os.path.join(os.getcwd(), "update.bat")
			main_executable = "WASAPIRecording.exe"

			with open(bat_path, "w") as bat_file:
				bat_file.write(f"""
@echo off
:: Cerrar la aplicación principal
taskkill /f /im "{main_executable}"

:: Copiar los archivos de la actualización
xcopy "{temp_dir}\\*" "{os.getcwd()}" /e /y

:: Eliminar los archivos temporales
rmdir /s /q "{temp_dir}"

:: Reiniciar la aplicación actualizada
start "" "{main_executable}"

:: Eliminar este archivo .bat
del "%~f0"
""")

			self.append_message(_("Archivo de actualización creado. La aplicación se reiniciará."))
			self.cancel_button.SetLabel(_("Reiniciar ahora"))
			self.cancel_button.Bind(wx.EVT_BUTTON, lambda evt: self.restart_app(bat_path))
			self.progress_bar.Hide()
			self.Layout()
			logger.log_action("UpdateDialog: Archivo BAT creado y botón 'Reiniciar ahora' configurado.")
		except Exception as e:
			wx.CallAfter(self.show_error, e)
			logger.log_error(f"UpdateDialog: Error al crear el archivo BAT: {e}")

	def restart_app(self, bat_path):
		"""
		Ejecuta el archivo BAT para aplicar la actualización y reiniciar la aplicación.

		:param bat_path: Ruta del archivo BAT generado.
		"""
		try:
			self.append_message(_("Reiniciando la aplicación..."))
			logger.log_action(f"UpdateDialog: Reiniciando la aplicación ejecutando {bat_path}")
			subprocess.Popen(
				[bat_path],
				shell=True,
				creationflags=subprocess.CREATE_NO_WINDOW
			)
			self.Close()
			wx.GetApp().Exit()
			logger.log_action("UpdateDialog: Aplicación cerrada para reinicio.")
		except Exception as e:
			wx.CallAfter(self.show_error, e)
			logger.log_error(f"UpdateDialog: Error al reiniciar la aplicación: {e}")

	def on_cancel(self, event):
		"""
		Maneja el botón "Cancelar". Si hay una descarga en proceso, se marca como cancelada.

		:param event: Evento de botón Cancelar.
		"""
		self.cancelled = True
		logger.log_action("UpdateDialog: Usuario canceló la actualización.")
		self.Close()

	def close_dialog(self, message):
		"""
		Cambia el texto del diálogo al mensaje dado y finaliza la operación.

		:param message: Mensaje a mostrar antes de cerrar.
		"""
		self.append_message(message)
		self.cancel_button.SetLabel(_("Cerrar"))
		self.progress_bar.Hide()
		self.Layout()
		logger.log_action("UpdateDialog: Diálogo cerrado con mensaje: " + message)
