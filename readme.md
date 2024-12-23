# Proyecto WASAPIRecording

## Índice / Table of Contents

- [Español](#español)
- [English](#english)

---

## Español

**WASAPIRecording** es una aplicación diseñada para grabar audio en tiempo real desde el sistema y el micrófono utilizando WASAPI (Windows Audio Session API). Ofrece características como selección de dispositivos, configuración de calidad y formato, grabación en canales separados o combinados, y una interfaz gráfica intuitiva desarrollada en wxPython.

### Requisitos
- Sistema operativo: Windows 10 / 11.
- Python: Versión 3.11.

### Instrucciones para configurar y ejecutar el proyecto

1. **Crear un entorno virtual en Python**  
   Desde la raíz del proyecto, ejecuta el siguiente comando para crear un entorno virtual:  
   ```bash
   python -m venv env
   ```

2. **Activar el entorno virtual**  
   Activa el entorno virtual con el siguiente comando:  
   ```bash
   .\env\Scripts\activate
   ```

3. **Instalar los requisitos**  
   Con el entorno virtual activado, instala las dependencias del proyecto desde el archivo `requerimientos.txt`:  
   ```bash
   pip install -r requerimientos.txt
   ```

4. **Ejecutar desde el código fuente**  
   Navega al directorio `src` y ejecuta el archivo `WASAPIRecording.pyw`:  
   ```bash
   cd src
   python WASAPIRecording.pyw
   ```

5. **Compilar con PyInstaller**  
   Para generar un ejecutable con PyInstaller, utiliza el siguiente comando desde el directorio `src`:  
   ```bash
   pyinstaller WASAPIRecording.spec
   ```

6. **Configuración adicional para la app compilada**  
   Una vez compilada la aplicación, copia los siguientes elementos al directorio de salida de la compilación:  
   - El directorio `locales` (contiene los archivos de traducción).  
   - El archivo `licencia.txt` que se encuentra en la raíz del proyecto en el directorio `documentos`.

7. **Generar cadenas para nuevos idiomas**  
   Si deseas generar las cadenas para añadir más idiomas, ejecuta el script `generar_pot.py` desde la raíz del proyecto:  
   ```bash
   python generar_pot.py
   ```

### Notas
- Asegúrate de utilizar Python 3.11 para evitar problemas de compatibilidad.
- Antes de ejecutar o compilar, verifica que las dependencias se hayan instalado correctamente.

### 🌍 Colabora añadiendo nuevos idiomas

En cada release de este proyecto, se incluye un archivo `.pot` que contiene todas las cadenas de texto utilizadas en la aplicación. Este archivo es la base para traducir la aplicación a otros idiomas.

#### Instrucciones para colaborar:
1. Descarga el archivo `mensajes.pot` desde la sección de releases.
2. Utiliza una herramienta como Poedit o cualquier editor compatible con archivos `.po`.
3. Carga el archivo `.pot` y selecciona el idioma que deseas traducir.
4. Traduce las cadenas de texto y guarda el archivo como `app.po`.
5. Compila el archivo a formato `.mo`. Esto se puede hacer con herramientas como `msgfmt` o desde Poedit.

   **Ejemplo de compilación con `msgfmt` en terminal:**
   ```bash
   msgfmt -o app.mo app.po
   ```
6. Crea una estructura de carpetas para tu idioma. Por ejemplo, para francés:
   ```
   src/locales/fr/LC_MESSAGES/
   ```
7. Coloca los archivos `app.po` y `app.mo` en la carpeta correspondiente.

#### Contacto
Si tienes traducciones completas o necesitas ayuda, puedes hacerme llegar tus archivos traducidos por los siguientes medios:

- **GitHub**: Abre un [issue](https://github.com/hxebolax/WASAPIRecording/issues) en este repositorio.
- **Mastodon**: [@HXeBoLaX](https://comunidad.nvda.es/@HXeBoLaX).

Gracias por tu colaboración en hacer este proyecto accesible a más idiomas y culturas. 🌐

### ⚠️ Advertencia sobre antivirus y falsos positivos

Las versiones compiladas de este proyecto, creadas con [PyInstaller](https://pyinstaller.org/), pueden ser detectadas como falsos positivos por algunos programas antivirus. Esto ocurre debido a la forma en que PyInstaller empaqueta los archivos ejecutables, lo cual puede ser identificado erróneamente como malicioso.

#### Recomendaciones:
- **Confianza en el código abierto**: Este proyecto es completamente de código abierto y puedes inspeccionar el código fuente en el [repositorio oficial de GitHub](https://github.com/hxebolax/WASAPIRecording) para asegurarte de que no contiene comportamientos maliciosos.
- **Compila tu propia versión**: Si prefieres evitar posibles problemas con tu antivirus, puedes compilar el proyecto por tu cuenta utilizando herramientas como `PyInstaller` u otros métodos de tu elección. Esto también garantiza que el ejecutable coincida con tu entorno y requisitos específicos.
- **Configura excepciones**: Si decides usar las versiones compiladas de las releases oficiales, considera agregar el ejecutable a la lista de excepciones de tu antivirus si detecta un falso positivo.
- **Verifica el origen**: Asegúrate de descargar el ejecutable únicamente desde el [repositorio oficial de GitHub](https://github.com/hxebolax/WASAPIRecording/releases).

Si encuentras problemas relacionados con esta advertencia o tienes dudas sobre las releases, no dudes en abrir un [issue](https://github.com/hxebolax/WASAPIRecording/issues).

### ☕ Invítame a un café

Si este proyecto te ha resultado útil o simplemente quieres apoyar mi trabajo, puedes invitarme a un café. ¡Tu apoyo es muy apreciado! ❤️

[![Invítame a un café](https://img.shields.io/badge/Invítame_a_un_café-PayPal-blue?logo=paypal)](https://www.paypal.com/paypalme/hjbcdonaciones)

Disfruta trabajando con el proyecto WASAPIRecording.

---

## English

**WASAPIRecording** is an application designed to record audio in real-time from the system and microphone using WASAPI (Windows Audio Session API). It offers features such as device selection, quality and format configuration, recording in separate or combined channels, and an intuitive graphical interface developed in wxPython.

### Requirements
- Operating System: Windows 10 / 11.
- Python: Version 3.11.

### Instructions to Set Up and Run the Project

1. **Create a Python Virtual Environment**  
   From the root of the project, execute the following command to create a virtual environment:  
   ```bash
   python -m venv env
   ```

2. **Activate the Virtual Environment**  
   Activate the virtual environment with the following command:  
   ```bash
   .\env\Scripts\activate
   ```

3. **Install Requirements**  
   With the virtual environment activated, install the project dependencies from the `requerimientos.txt` file:  
   ```bash
   pip install -r requerimientos.txt
   ```

4. **Run from Source Code**  
   Navigate to the `src` directory and run the `WASAPIRecording.pyw` file:  
   ```bash
   cd src
   python WASAPIRecording.pyw
   ```

5. **Compile with PyInstaller**  
   To generate an executable with PyInstaller, use the following command from the `src` directory:  
   ```bash
   pyinstaller WASAPIRecording.spec
   ```

6. **Additional Configuration for the Compiled App**  
   Once the application is compiled, copy the following items to the compilation output directory:  
   - The `locales` directory (contains the translation files).  
   - The `licencia.txt` file located in the root of the project in the `documentos` directory.

7. **Generate Strings for New Languages**  
   If you wish to generate strings to add more languages, run the `generar_pot.py` script from the root of the project:  
   ```bash
   python generar_pot.py
   ```

### Notes
- Ensure you use Python 3.11 to avoid compatibility issues.
- Before running or compiling, verify that the dependencies have been installed correctly.

### 🌍 Collaborate by Adding New Languages

Each release of this project includes a `.pot` file that contains all the text strings used in the application. This file is the basis for translating the application into other languages.

#### Instructions to Collaborate:
1. Download the `mensajes.pot` file from the releases section.
2. Use a tool like Poedit or any editor compatible with `.po` files.
3. Load the `.pot` file and select the language you wish to translate.
4. Translate the text strings and save the file as `app.po`.
5. Compile the file to `.mo` format. This can be done with tools like `msgfmt` or from Poedit.

   **Example of compilation with `msgfmt` in terminal:**
   ```bash
   msgfmt -o app.mo app.po
   ```
6. Create a folder structure for your language. For example, for French:
   ```
   src/locales/fr/LC_MESSAGES/
   ```
7. Place the `app.po` and `app.mo` files in the corresponding folder.

#### Contact
If you have complete translations or need assistance, you can send me your translated files through the following means:

- **GitHub**: Open an [issue](https://github.com/hxebolax/WASAPIRecording/issues) in this repository.
- **Mastodon**: [@HXeBoLaX](https://comunidad.nvda.es/@HXeBoLaX).

Thank you for your collaboration in making this project accessible to more languages and cultures. 🌐

### ⚠️ Warning About Antivirus and False Positives

The compiled versions of this project, created with [PyInstaller](https://pyinstaller.org/), may be detected as false positives by some antivirus programs. This happens due to the way PyInstaller packages executable files, which can be mistakenly identified as malicious.

#### Recommendations:
- **Trust in Open Source**: This project is completely open source, and you can inspect the source code in the [official GitHub repository](https://github.com/hxebolax/WASAPIRecording) to ensure it does not contain malicious behaviors.
- **Compile Your Own Version**: If you prefer to avoid potential issues with your antivirus, you can compile the project yourself using tools like `PyInstaller` or other methods of your choice. This also ensures that the executable matches your specific environment and requirements.
- **Configure Exceptions**: If you decide to use the compiled versions from the official releases, consider adding the executable to your antivirus's exception list if it detects a false positive.
- **Verify the Source**: Ensure you download the executable only from the [official GitHub repository](https://github.com/hxebolax/WASAPIRecording/releases).

If you encounter issues related to this warning or have questions about the releases, feel free to open an [issue](https://github.com/hxebolax/WASAPIRecording/issues).

### ☕ Buy Me a Coffee

If this project has been useful to you or you simply want to support my work, you can buy me a coffee. Your support is greatly appreciated! ❤️

[![Buy Me a Coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-PayPal-blue?logo=paypal)](https://www.paypal.com/paypalme/hjbcdonaciones)

Enjoy working with the WASAPIRecording project.