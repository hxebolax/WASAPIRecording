#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Diálogo de Actualización (UpdateDialog)

Este módulo implementa un diálogo de actualización para aplicaciones que utiliza 
GitHub como fuente para las versiones más recientes. Proporciona una interfaz gráfica 
(wxPython) que permite comprobar, descargar y aplicar actualizaciones de manera interactiva.

Clases:
- UpdateDialog: Clase principal que gestiona el diálogo de actualización, comprobaciones, 
  descargas y aplicación de nuevas versiones.

Características:
- Bloqueo de cierre forzado (X, Alt+F4).
- Verificación de actualizaciones en GitHub utilizando la API REST.
- Descarga de actualizaciones con indicador de progreso.
- Extracción automática de archivos ZIP y generación de un script BAT para aplicar los cambios.
- Reinicio automático de la aplicación después de la instalación.

Dependencias:
- wxPython: Para la interfaz gráfica.
- urllib.request: Para realizar solicitudes HTTP.
- zipfile: Para manejar archivos ZIP.
- shutil: Para operaciones de archivo y directorio.
- threading: Para manejar procesos en segundo plano.
- subprocess: Para ejecutar scripts de instalación.
- core.logger: Sistema de registro para acciones y errores.
- core.utils: Función `get_base_path` para obtener rutas dinámicas.

Excepciones gestionadas:
- Manejo de errores de red (conexión, SSL, tiempo de espera).
- Problemas relacionados con archivos y permisos.
- Errores de lógica del programa, como datos faltantes o inconsistentes.

Uso:
Este diálogo puede integrarse en una aplicación existente para proporcionar una funcionalidad 
de actualización automática basada en versiones almacenadas en un repositorio de GitHub.

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
from core.utils import get_base_path  # Asegúrate de tener esta función en core.utils

# Inicialización del logger
logger = Logger(log_dir=os.path.join(get_base_path(), "logs"))

class UpdateDialog(wx.Dialog):
	def __init__(self, parent, repo_owner, repo_name, current_version):
		super().__init__(parent, title=_("Actualización"), size=(500, 300), style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)
		logger.log_action("UpdateDialog: Inicializando el diálogo de actualización.")

		# Bloqueamos la X, Alt+F4, etc.
		self.SetWindowStyleFlag(
			self.GetWindowStyleFlag()
			& ~wx.CLOSE_BOX
			& ~wx.MAXIMIZE_BOX
			& ~wx.MINIMIZE_BOX
			& ~wx.SYSTEM_MENU
		)
		# Evitar Alt+F4
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
		logger.log_action("UpdateDialog: Configurado para bloquear cierre con la X y Alt+F4.")

		self.repo_owner = repo_owner
		self.repo_name = repo_name
		self.current_version = current_version
		self.cancelled = False
		self.download_thread = None

		# Etiqueta para identificar el cuadro de texto
		info_label = wx.StaticText(self, label=_("&Información:"))
		self.message_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_NONE)
		self.progress_bar = wx.Gauge(self, range=100, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
		self.progress_bar.Hide()

		self.cancel_button = wx.Button(self, label=_("Cancelar"))
		self.install_button = wx.Button(self, label=_("Instalar"))
		self.install_button.Hide()

		self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
		self.install_button.Bind(wx.EVT_BUTTON, self.on_install)

		# Sizer para los botones en horizontal con separación
		button_sizer = wx.BoxSizer(wx.HORIZONTAL)
		button_sizer.Add(self.install_button, flag=wx.ALL, border=5)
		button_sizer.AddSpacer(10)  # Separación entre botones
		button_sizer.Add(self.cancel_button, flag=wx.ALL, border=5)

		# Diseño principal
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(info_label, flag=wx.ALL | wx.EXPAND, border=10)  # Etiqueta
		sizer.Add(self.message_text, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
		sizer.Add(self.progress_bar, flag=wx.ALL | wx.EXPAND, border=10)
		sizer.Add(button_sizer, flag=wx.ALIGN_CENTER_HORIZONTAL)  # Botones en horizontal

		self.SetSizer(sizer)

		# Iniciar comprobación de actualizaciones
		threading.Thread(target=self.check_update, daemon=True).start()
		logger.log_action("UpdateDialog: Hilo para comprobar actualizaciones iniciado.")

	def on_key_down(self, event):
		key_code = event.GetKeyCode()
		# Si se presiona F4 con Alt, ignoramos
		if key_code == wx.WXK_F4 and event.AltDown():
			logger.log_action("UpdateDialog: Intento de cierre con Alt+F4 ignorado.")
			return
		event.Skip()

	def append_message(self, message):
		"""Añade un mensaje al cuadro de texto."""
		self.message_text.Clear()
		self.message_text.AppendText(f"\n{message}\n")
		self.message_text.SetInsertionPoint(0)
		logger.log_action(f"UpdateDialog: Mensaje añadido al cuadro de texto: {message}")

	def check_update(self):
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
		message = _("Se encontró una nueva versión: {0}. ¿Desea instalarla?").format(new_version)
		self.append_message(message)
		self.install_button.Show()
		self.Layout()
		logger.log_action("UpdateDialog: Prompt de actualización mostrado al usuario.")

	def show_no_update(self):
		self.append_message(_("No hay actualizaciones disponibles. Su aplicación está actualizada."))
		self.cancel_button.SetLabel(_("Cerrar"))
		logger.log_action("UpdateDialog: Mensaje de no actualización mostrado al usuario.")

	def show_error(self, error):
		import socket
		import ssl
		import urllib.error

		# Errores de red
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

		# Errores relacionados con archivos
		elif isinstance(error, FileNotFoundError):
			error_message = _("No se encontró el archivo necesario para completar la operación.")
		elif isinstance(error, IsADirectoryError):
			error_message = _("Se esperaba un archivo, pero se encontró un directorio.")
		elif isinstance(error, PermissionError):
			error_message = _("Permiso denegado. Ejecute la aplicación con los permisos adecuados.")
		elif isinstance(error, shutil.Error):
			error_message = _("Error al copiar o mover archivos. Verifique los permisos y el espacio disponible.")

		# Errores relacionados con la lógica del programa
		elif isinstance(error, ValueError):
			error_message = _("Se produjo un error en los datos proporcionados. Verifique la información ingresada.")
		elif isinstance(error, KeyError):
			error_message = _("Falta un elemento requerido en los datos. Verifique el formato de la información.")
		elif isinstance(error, IndexError):
			error_message = _("Se intentó acceder a un elemento fuera del rango permitido. Revise la configuración interna.")

		# Errores específicos de conexiones y protocolos
		elif isinstance(error, ConnectionError):
			error_message = _("No se pudo establecer una conexión. Verifique su conexión a Internet.")
		elif isinstance(error, TimeoutError):
			error_message = _("La operación tardó demasiado tiempo en completarse. Inténtelo más tarde.")
		elif isinstance(error, BrokenPipeError):
			error_message = _("Se perdió la conexión con el servidor. Intente reconectarse.")

		# Otros errores generales
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
		self.append_message(_("Descargando la actualización, esto puede tardar unos momentos..."))
		self.progress_bar.Show()
		self.install_button.Hide()
		self.Layout()
		logger.log_action("UpdateDialog: Iniciando descarga de la actualización.")

		self.download_thread = threading.Thread(target=self.download_update, daemon=True)
		self.download_thread.start()
		logger.log_action("UpdateDialog: Hilo de descarga iniciado.")

	def download_update(self):
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
		try:
			self.append_message(_("Extrayendo la actualización..."))
			logger.log_action(f"UpdateDialog: Extrayendo archivo ZIP: {zip_path}")
			temp_dir = os.path.join(os.getcwd(), "temp-install")
			with zipfile.ZipFile(zip_path, "r") as zip_ref:
				subfolder = "WASAPIRecording/"
				for file_name in zip_ref.namelist():
					if file_name.startswith(subfolder):
						target_path = os.path.join(temp_dir, file_name[len(subfolder):])
						if not os.path.basename(target_path):  # Si es una carpeta
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
		try:
			self.append_message(_("Reiniciando la aplicación..."))
			logger.log_action(f"UpdateDialog: Reiniciando la aplicación ejecutando {bat_path}")
			# Ejecutar el archivo .bat en segundo plano sin mostrar consola
			subprocess.Popen(
				[bat_path],
				shell=True,
				creationflags=subprocess.CREATE_NO_WINDOW
			)
			# Cerrar la aplicación principal
			self.Close()
			wx.GetApp().Exit()
			logger.log_action("UpdateDialog: Aplicación cerrada para reinicio.")
		except Exception as e:
			wx.CallAfter(self.show_error, e)
			logger.log_error(f"UpdateDialog: Error al reiniciar la aplicación: {e}")

	def on_cancel(self, event):
		self.cancelled = True
		logger.log_action("UpdateDialog: Usuario canceló la actualización.")
		self.Close()

	def close_dialog(self, message):
		self.append_message(message)
		self.cancel_button.SetLabel(_("Cerrar"))
		self.progress_bar.Hide()
		self.Layout()
		logger.log_action("UpdateDialog: Diálogo cerrado con mensaje: " + message)
