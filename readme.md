# Proyecto WASAPIRecording

**WASAPIRecording** es una aplicación diseñada para grabar audio en tiempo real desde el sistema y el micrófono utilizando WASAPI (Windows Audio Session API). Ofrece características como selección de dispositivos, configuración de calidad y formato, grabación en canales separados o combinados, y una interfaz gráfica intuitiva desarrollada en wxPython.

## Requisitos
- Sistema operativo: Windows.
- Python: Versión 3.11.

## Instrucciones para configurar y ejecutar el proyecto

1. Crear un entorno virtual en Python  
   Desde la raíz del proyecto, ejecuta el siguiente comando para crear un entorno virtual:  
   python -m venv env

2. Activar el entorno virtual  
   Activa el entorno virtual con el siguiente comando:  
   .\env\Scripts\activate

3. Instalar los requisitos  
   Con el entorno virtual activado, instala las dependencias del proyecto desde el archivo requerimientos.txt:  
   pip install -r requerimientos.txt

4. Ejecutar desde el código fuente  
   Navega al directorio src y ejecuta el archivo WASAPIRecording.pyw:  
   cd src  
   python WASAPIRecording.pyw

5. Compilar con PyInstaller  
   Para generar un ejecutable con PyInstaller, utiliza el siguiente comando desde el directorio src:  
   pyinstaller WASAPIRecording.spec

6. Configuración adicional para la app compilada  
   Una vez compilada la aplicación, copia los siguientes elementos al directorio de salida de la compilación:  
   - El directorio locales (contiene los archivos de traducción).  
   - El archivo licencia.txt.

7. Generar cadenas para nuevos idiomas  
   Si deseas generar las cadenas para añadir más idiomas, ejecuta el script generar_pot.py desde la raíz del proyecto:  
   python generar_pot.py

## Notas
- Asegúrate de utilizar Python 3.11 para evitar problemas de compatibilidad.
- Antes de ejecutar o compilar, verifica que las dependencias se hayan instalado correctamente.

## ⚠️ Advertencia sobre antivirus y falsos positivos

Las versiones compiladas de este proyecto, creadas con [PyInstaller](https://pyinstaller.org/), pueden ser detectadas como falsos positivos por algunos programas antivirus. Esto ocurre debido a la forma en que PyInstaller empaqueta los archivos ejecutables, lo cual puede ser identificado erróneamente como malicioso.

### Recomendaciones:
- **Confianza en el código abierto**: Este proyecto es completamente de código abierto y puedes inspeccionar el código fuente en el [repositorio oficial de GitHub](https://github.com/hxebolax/WASAPIRecording) para asegurarte de que no contiene comportamientos maliciosos.
- **Compila tu propia versión**: Si prefieres evitar posibles problemas con tu antivirus, puedes compilar el proyecto por tu cuenta utilizando herramientas como `PyInstaller` u otros métodos de tu elección. Esto también garantiza que el ejecutable coincida con tu entorno y requisitos específicos.
- **Configura excepciones**: Si decides usar las versiones compiladas de las releases oficiales, considera agregar el ejecutable a la lista de excepciones de tu antivirus si detecta un falso positivo.
- **Verifica el origen**: Asegúrate de descargar el ejecutable únicamente desde el [repositorio oficial de GitHub](https://github.com/hxebolax/WASAPIRecording/releases).

Si encuentras problemas relacionados con esta advertencia o tienes dudas sobre las releases, no dudes en abrir un [issue](https://github.com/hxebolax/WASAPIRecording/issues).

Disfruta trabajando con el proyecto WASAPIRecording.
