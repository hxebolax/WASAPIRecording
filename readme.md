# Proyecto WASAPIRecording

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

Disfruta trabajando con el proyecto WASAPIRecording.
