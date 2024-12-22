import os
import subprocess

def generar_archivo_pot(directorio_fuente, archivo_pot_salida):
	"""
	Genera un archivo mensajes.pot a partir de los archivos fuente en el directorio especificado.

	:param directorio_fuente: Ruta del directorio donde se encuentra el código fuente.
	:param archivo_pot_salida: Ruta del archivo .pot de salida.
	"""
	try:
		# Verificar que xgettext está disponible
		if subprocess.call(['xgettext', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
			raise RuntimeError("xgettext no está instalado. Asegúrate de que gettext esté instalado en tu sistema.")

		# Buscar archivos Python en el directorio fuente
		archivos_fuente = []
		for root, _, files in os.walk(directorio_fuente):
			for file in files:
				if file.endswith('.py'):  # Solo incluir archivos Python
					archivos_fuente.append(os.path.join(root, file))

		if not archivos_fuente:
			raise RuntimeError("No se encontraron archivos Python en el directorio especificado.")

		# Construir el comando para xgettext
		comando = [
			'xgettext',
			'--from-code=UTF-8',  # Codificación del código fuente
			'--language=Python',  # Lenguaje del código fuente
			'--output', archivo_pot_salida,  # Archivo de salida
			'--keyword=_',  # Buscar cadenas marcadas con _
			'--default-domain=mensajes',  # Nombre del dominio
			'--no-wrap',  # No ajustar líneas en el archivo POT
			'--add-comments=TRANSLATORS:',  # Agregar comentarios para traductores
			f'--msgid-bugs-address=tu_email@ejemplo.com',  # Dirección de contacto
			f'--package-name=WASAPIRecording',
			f'--package-version=1.0'
		] + archivos_fuente  # Agregar todos los archivos fuente al comando

		# Ejecutar el comando
		subprocess.run(comando, check=True)
		print(f"Archivo POT generado con éxito: {archivo_pot_salida}")

	except RuntimeError as e:
		print(f"Error: {e}")
	except Exception as e:
		print(f"Ocurrió un error inesperado: {e}")

if __name__ == '__main__':
	directorio_fuente = './src'  # Cambia esto al directorio de tu código fuente
	archivo_pot_salida = './locales/mensajes.pot'  # Cambia esto a la ubicación deseada para app.pot
	os.makedirs(os.path.dirname(archivo_pot_salida), exist_ok=True)
	generar_archivo_pot(directorio_fuente, archivo_pot_salida)
