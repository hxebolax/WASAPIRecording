��    e      D  �   l      �  [  �  S   �   V   A!     �!     �!     �!  	   �!     �!     �!     �!     �!     "     $"     3"     G"     W"     j"     q"     u"     �"  $   �"     �"     �"     �"     �"  ,   #     9#     K#     S#     a#     n#     v#     |#     �#     �#     �#     �#     �#  %   �#  %   �#     $     8$     S$     d$     l$  (   y$  !   �$  :   �$     �$  &   %  (   ,%     U%     f%     o%     �%  �  �%     N)     U)     ^)     g)  
   o)  9   z)  /   �)  #   �)  3   *  7   <*     t*     {*     �*     �*  L   �*  3   �*  C   +     ^+     l+  "   y+     �+     �+     �+  !   �+  �   �+  :   �,  6   �,     �,  U   �,  1   Q-  ,   �-  
   �-  
   �-     �-     �-     �-  
   �-     .     .     #.     +.  )   1.  [   [.  ,   �.  :  �.    0  F   <F  I   �F     �F     �F     �F     �F     G     G     G     G     .G     FG     TG     eG     uG     �G     �G     �G     �G     �G     �G     �G     �G     �G  +    H     ,H     <H     CH     PH     YH     `H     eH     mH     tH     �H     �H     �H     �H     �H     �H      I     I     (I     -I     5I     PI  2   lI     �I     �I  &   �I     �I     �I     J     J  j  6J     �M     �M     �M     �M  	   �M  /   �M  )   �M     !N  *   AN  <   lN     �N     �N     �N     �N  @   �N  1   O  F   AO     �O     �O     �O     �O     �O     �O  $   �O  �   P  4   �P  ,   �P     �P  W   �P  *   JQ  %   uQ  
   �Q  
   �Q  
   �Q     �Q     �Q     �Q     �Q     �Q     �Q     R  (   	R  _   2R  *   �R                K           c          ;           b       "       8   1                 J   0          &   #       N   -   Y          >   G   5   )   _   =         <              ]   2      9   C   Z   W       4   %   F         A   R   	   /   I          V   [          ?   H   P       (   Q   ,          T   `          *          '   X       B       L                    E   @   
   M   3       \       6   :   O          a       .   e   $       d       !          U   D   +      ^                    7   S              
1. ¿Qué es WASAPIRecording?
 
WASAPIRecording es una aplicación para Windows que te permite grabar el audio de tu micrófono y el audio del sistema (música, videollamadas, etc.) de forma simultánea. Puedes combinar ambos en un solo archivo o guardarlos por separado (uno para el micrófono y otro para el sonido del sistema).
 
2. Requisitos
 
• Windows 10 o superior (con WASAPI).
• Permisos para ejecutar la aplicación.
 
3. Iniciar la Aplicación
 
• Ejecuta el archivo o acceso directo llamado "WASAPIRecording".
• Se abrirá la ventana principal con controles para micrófono, sistema, formatos de audio, etc.
 
4. Configurar Dispositivos y Parámetros
 
• Micrófono: Selecciona el micrófono que quieres usar.
• Sistema (loopback): Selecciona el dispositivo de tu PC que captura todo lo que suena en el sistema.
• Refrescar Dispositivos: Si conectaste algo nuevo y no aparece, haz clic aquí para actualizar la lista.
• Calidad (Hz): Elige la frecuencia de muestreo (22050, 44100 o 48000). A mayor número, más calidad y más peso del archivo.
• Formato de Salida: Puedes elegir WAV, MP3, FLAC, OGG o AIFF.
• Bitrate MP3: Se mostrará solo si eliges MP3; ajusta la calidad de compresión.
• Modo de grabación (Mono o Estéreo): Decide cuántos canales tendrá tu grabación final.
• Habilitar Mezcla Monoaural:
• Si notas que tu audio está siendo separado (por ejemplo, micrófono a un solo lado, sistema al otro), activa esta casilla para mezclar ambos canales y centrar el sonido.
• En la práctica, todos los sonidos se combinan en un solo canal y se replica al izquierdo y derecho, evitando la sensación de que el audio “esté inclinado” a un lado.
• Guardar archivos separados:
• Si lo marcas, además de crear un archivo “combinado”, la app guardará otros dos archivos individuales: uno solo del micrófono y otro del sistema.
 
5. Ajustar Volúmenes
 
• Volumen del Micrófono: Usa el deslizador para subir o bajar la ganancia del micro.
• Volumen del Sistema: Sube o baja la ganancia de los sonidos del PC.
 
6. Iniciar y Detener la Grabación
 
• Pulsa Iniciar Grabación (o usa el atajo global “Ctrl + Shift + F1” por defecto). El estado mostrará “Grabando…”.
• Para detener, haz clic en Detener Grabación (o “Ctrl + Shift + F2”).
• Si elegiste MP3, FLAC, OGG o AIFF, la app convertirá el archivo final tras la grabación; aparecerá un mensaje de “Por favor espere…”.
• Cuando acabe, verás un aviso con la ruta donde se guardaron tus archivos.
 
7. Dónde se Guardan las Grabaciones
 
• Se almacenan en una carpeta llamada “recording”, que está dentro de la carpeta de la aplicación.
• Desde la ventana principal, puedes abrir esa carpeta haciendo clic en Menú > Abrir Grabaciones.
 
8. Opciones y Menú
 
• En la ventana principal, hay un botón llamado Menú:
• Acerca de…: Muestra la versión de WASAPIRecording y el nombre del creador.
• Abrir Grabaciones: Abre la carpeta donde están los archivos grabados.
• Idioma: Elige el idioma que prefieras. Deberás reiniciar la app para aplicar el cambio.
• Opciones:
• Aquí encontrarás el diálogo de Opciones, con dos apartados:
• General: Incluye la casilla “Minimizar a la bandeja del sistema” para ocultar la ventana y dejar un ícono en la bandeja cuando minimizas.
• Teclado: Sirve para cambiar los atajos globales de iniciar y detener la grabación. Si no te funcionan o están repetidos, aquí puedes ajustarlos.
 
9. Prueba de Audio
 
• El botón Prueba de Audio abre un diálogo para grabar unos segundos de muestra y reproducirlos inmediatamente.
• Este diálogo:
• Se abre siempre en primer plano.
• No se cierra con la “X” ni con Alt+F4; solo con el botón Cerrar.
• Primero grabas (botón “Detener” para terminar la grabación).
• Luego puedes “Reproducir” lo que grabaste.
• Si tienes “Guardar archivos separados” marcado, podrás elegir reproducir solo el micrófono, solo el sistema o ambos.
• Al cerrar este diálogo, los archivos temporales se borran, así que es perfecto para confirmar que todo suena bien antes de hacer una grabación definitiva.
 
10. Atajos de Teclado
 
Atajos Globales (por defecto, puedes cambiarlos en Opciones > Teclado):
• Iniciar Grabación: Ctrl + Shift + F1
• Detener Grabación: Ctrl + Shift + F2
Atajos dentro de la interfaz (con la tecla Alt):
• Micrófono: Alt + O
• Sistema (loopback): Alt + S
• Refrescar Dispositivos: Alt + R
• Calidad (Hz): Alt + C
• Formato de salida: Alt + F
• Bitrate MP3 (kbps): Alt + B
• Modo de grabación: Alt + G
• Habilitar Mezcla Monoaural: Alt + H
• Guardar archivos separados de micrófono y sistema: Alt + Y
• Volumen del Micrófono: Alt + V
• Volumen del Sistema: : Alt + V
• Iniciar Grabación: Alt + I
• Detener Grabación: Alt + D
• Prueba de Audio: Alt + P
• Menú: Alt + M
• Cerrar (en algunos diálogos): Alt + C
• Dependiendo del idioma, algunas letras pueden variar.
 
11. Minimizar a la Bandeja
 
• Si en las Opciones (pestaña “General”) has activado “Minimizar a la bandeja”, al pulsar el botón de minimizar de Windows, la ventana desaparece de la barra de tareas y se muestra un ícono cerca del reloj del sistema.
• Desde el ícono en la bandeja, puedes hacer doble clic para restaurar la ventana o usar el menú contextual para mostrarla/cerrar la aplicación.
 
12. Cerrar la Aplicación
 
• Al cerrar la ventana principal, si se está grabando, te preguntará si deseas detener la grabación antes de salir.
• Si se está convirtiendo el archivo a MP3/FLAC/etc., esperará a que termine la conversión.
• Luego se cerrará por completo.
 
13. Consejos Finales
 
• Ajusta el volumen del sistema y micrófono dentro de la propia app para equilibrar tus fuentes de audio.
• Si algo no se oye bien, usa la Prueba de Audio para verificar y ajustar antes de grabar definitivamente.
• Si el audio se oye “inclinado” a un canal (izquierdo o derecho), marca “Habilitar Mezcla Monoaural” para centrar el sonido.
 
¡Disfruta grabando con WASAPIRecording! Si te gusta esta app, pasa por “Menú > invítame a un café” para apoyar su desarrollo.
 
Archivo separado de micrófono: {mic_path}
Archivo separado de sistema: {sys_path} 
Archivo separado de micrófono: {mic_path}
Archivo separado de sistema: {system_path} &Aceptar &Bitrate MP3 (kbps): &Calidad (Hz): &Cancelar &Cerrar &Detener &Detener Grabación &Formato de salida: &Habilitar Mezcla Monoaural &Información: &Iniciar Grabación &Manual de Uso: &Manual de usuario &Menú &No &Prueba de Audio &Refrescar Dispositivos &Selecciona qué archivo reproducir: &Sistema (loopback): &Sí &Volumen del Micrófono: &Volumen del Sistema: &invítame a un café si te gusta mi trabajo Abrir Grabaciones Aceptar Acerca &de... Acerca de... Alemán Ambos Aviso Cancelar Cancelar Prueba Capturar Hotkey Inicio Capturar Hotkey Parar Cerrar Combinación para Detener Grabación: Combinación para Iniciar Grabación: Configuración de Grabación Confirmar cambio de idioma Confirmar cierre Detener Dispositivos Dispositivos actualizados correctamente. En espera (Usa {hk} para iniciar) En espera. Asigna teclas en Opciones o inicia manualmente. Error Error al convertir el archivo: {error} Error al refrescar dispositivos: {error} Error de Hotkeys Español Esperando combinación... Espere por favor... Procesando Esta ventana permite realizar una prueba de grabación y reproducción.

1. Al abrirse, inicia la grabación con los mismos ajustes que la ventana principal.
2. Para finalizar la grabación, pulsa 'Detener'. Entonces, el botón cambiará a 'Reproducir'.
3. Si estaba activada la opción de 'Guardar archivos separados' en la ventana principal, se mostrará el menú desplegable para elegir si reproducir sólo micrófono, solo sistema o ambos (por defecto 'Ambos').
4. Al pulsar 'Reproducir', se inicia la reproducción del WAV de forma asíncrona. El botón cambia a 'Detener' durante la reproducción. Al terminar la pista, volverá a 'Reproducir'.
5. Si pulsas 'Cerrar' mientras graba, te preguntará si deseas cancelar la prueba (se borrarán los archivos). Si ya grabaste y/o terminaste, simplemente cerrará y también borrará los archivos.

No puedes cerrar con Alt+F4 ni con la X de la ventana; solo con el botón 'Cerrar'.
 Estado Estéreo Francés General Grabación Grabación completada. Archivo guardado como:
{file_path} Grabando... (No hay hotkey de detener asignada) Grabando... (Usa {hk} para detener) Guardar archivos separados de micrófono &y sistema Hay una grabación en curso. ¿Desea detenerla y salir? Idioma Información Inglés Italiano La combinación debe tener al menos dos modificadores y una tecla principal. La combinación está en uso por otra aplicación:  La grabación sigue en curso. ¿Desea cancelar la prueba de sonido? Manual de Uso Micrófon&o: Minimizar a la bandeja del sistema Modo de &grabación: Mono Mostrar aplicación No existe el archivo a reproducir No puede asignar la misma combinación a Iniciar y Detener.
Por favor, elija una diferente.
Se revertirán los cambios a los que tenia por defecto. No se ha grabado nada aún. Primero detenga la grabación. No se pudo abrir el directorio de grabaciones: {error} Opciones Para aplicar el nuevo idioma se necesita reiniciar la aplicación.
¿Desea continuar? Por favor espere, convirtiendo a formato final... Por favor espere, finalizando conversión... Portugués Procesando Prueba de Audio Prueba micrófono Prueba sistema Reproducir Salir Tecla inválida detectada. Teclado Turco WASAPIRecording
Versión {}
Creado por {} WASAPIRecording ya se encuentra en ejecución.

No se pueden tener dos instancias a la vez. invítame a un &café si te gusta mi trabajo Project-Id-Version: WASAPIRecording 1.0
Report-Msgid-Bugs-To: tu_email@ejemplo.com
PO-Revision-Date: 2024-12-23 15:29+0100
Last-Translator: 
Language-Team: 
Language: en
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: Poedit 3.5
X-Poedit-SourceCharset: UTF-8
 
1. what is WASAPIRecording?
 
WASAPIRecording is a Windows application that allows you to record your microphone audio and system audio (music, video calls, etc.) simultaneously. You can combine both in a single file or save them separately (one for the microphone and one for the system audio).
 
2. Requirements
 
- Windows 10 or higher (with WASAPI).
- Permissions to run the application.
 
3. Start the Application
 
- Run the file or shortcut named "WASAPIRecording".
- The main window will open with controls for microphone, system, audio formats, etc.
 
4. Configure Devices and Parameters
 
- Microphone: Select the microphone you want to use.
- System (loopback): Select the device on your PC that captures everything that sounds on the system.
- Refresh Devices: If you connected something new and it does not appear, click here to refresh the list.
- Quality (Hz): Choose the sample rate (22050, 44100 or 48000). The higher the number, the higher the quality and the heavier the file.
- Output Format: You can choose WAV, MP3, FLAC, OGG or AIFF.
- MP3 Bitrate: Will be displayed only if you choose MP3; adjust the compression quality.
- Recording Mode (Mono or Stereo): Decide how many channels your final recording will have.
- Enable Mono Mix:
- If you notice that your audio is being separated (e.g. microphone on one side only, system on the other), check this box to mix both channels and center the sound.
- In practice, all sounds are combined into a single channel and replicated to the left and right, avoiding the feeling that the audio is "leaning" to one side.
- Saving separate files:
- If checked, in addition to creating a "combined" file, the app will save two other individual files: one from the microphone only and one from the system.
 
5. Adjust Volumes
 
- Microphone Volume: Use the slider to raise or lower the mic gain.
- System Volume: Raises or lowers the gain of the PC sounds.
 
6. Start and Stop Recording
 
- Press Start Recording (or use the global shortcut "Ctrl + Shift + F1" by default). The status will show "Recording...".
- To stop, click Stop Recording (or "Ctrl + Shift + F2").
- If you chose MP3, FLAC, OGG or AIFF, the app will convert the final file after recording; a "Please wait..." message will appear.
- When finished, you will see a prompt with the path where your files were saved.
 
7. Where Recordings are Saved
 
- They are stored in a folder called "recording", which is inside the application folder.
- From the main window, you can open that folder by clicking Menu > Open Recordings.
 
8. Options and Menu
 
- In the main window, there is a button called Menu:
- About...: Displays the version of WASAPIRecording and the name of the creator.
- Open Recordings: Opens the folder where the recorded files are located.
- Language: Choose the language of your choice. You will need to restart the app to apply the change.
- Options:
- Here you will find the Options dialog, with two sections:
- General: Include the checkbox "Minimize to system tray" to hide the window and leave an icon in the tray when you minimize.
- Keyboard: It is used to change the global shortcuts to start and stop recording. If they do not work or are repeated, you can adjust them here.
 
9. Audio Test
 
- The Audio Test button opens a dialog to record a few seconds of sample and play them back immediately.
- This dialog:
- It is always opened in the foreground.
- It is not closed with "X" or Alt+F4; only with the Close button.
- First you record ("Stop" button to end recording).
- Then you can "Playback" what you recorded.
- If you have "Save separate files" checked, you can choose to play back only the microphone, only the system or both.
- When you close this dialog, the temporary files are deleted, so it's perfect for confirming that everything sounds good before making a final recording.
 
10. Keyboard Shortcuts
 
Global Shortcuts (by default, you can change them in Options > Keyboard):
- Start Recording: Ctrl + Shift + F1
- Stop Recording: Ctrl + Shift + F2
Shortcuts inside the interface (with the Alt key):
- Microphone: Alt + O
- System (loopback): Alt + S
- Refresh Devices: Alt + R
- Quality (Hz): Alt + C
- Output format: Alt + F
- Bitrate MP3 (kbps): Alt + B
- Record Mode: Alt + G
- Enable Mono Mixing: Alt + H
- Save separate microphone and system files: Alt + Y
- Microphone Volume: Alt + V
- System Volume: system Volume: Alt + V
- Start Recording: Alt + I
- Stop Recording: Alt + D
- Audio Test: Alt + P
- Menu: Alt + M
- Close (in some dialogs): Alt + C
- Depending on the language, some letters may vary.
 
11. Minimize to Tray
 
- If in the Options ("General" tab) you have activated "Minimize to tray", when you press the Windows minimize button, the window disappears from the taskbar and an icon is displayed near the system clock.
- From the icon in the tray, you can double-click to restore the window or use the context menu to show/close the application.
 
12. Close the Application
 
- When closing the main window, if recording, you will be asked if you want to stop recording before exiting.
- If the file is being converted to MP3/FLAC/etc., it will wait for the conversion to finish.
- Then it will close completely.
 
13. Final Tips
 
- Adjust the system and microphone volume within the app itself to balance your audio sources.
- If something doesn't sound right, use the Audio Test to check and adjust before recording for good.
- If the audio is "skewed" to one channel (left or right), check "Enable Mono Mixing" to center the sound.
 
enjoy recording with WASAPIRecording! If you like this app, stop by "Menu > invite me to a coffee" to support its development.
 
Microphone separate file: {mic_path}
System separate file: {sys_path} 
Separate microphone file: {mic_path}
System separate file: {system_path} &Accept &Bitrate MP3 (kbps): &Quality (Hz): &Cancel &Close &Stop Stop Recor&ding Output &format: Enable Monaural Mi&xing &Information: Start Record&ing &User's Manual: &User Manual &Menu &No &Audio Test &Refresh Devices select which file to play: &System(loopback): &Yes Microphone &Volume: System &Volume: &invite me for a coffee if you like my work Open Recordings Accept About &de... About... German Both Warning Cancel Cancel Test Capture Hotkey Home Capture Hotkey Stop Close Combination to Stop Recording: Combination to Start Recording: Recording Settings Confirm language change Confirm closure Stop Devices Correctly updated devices. Standby (Use {hk} to start) Standby. Assign keys in Options or start manually. Error Error converting file: {error} Error when refreshing devices: {error} Hotkeys error Spanish Waiting for combination... Please wait... Processing This window allows you to perform a recording and playback test.

1. When opened, it starts recording with the same settings as the main window.
2. To end the recording, press 'Stop'. Then, the button will change to 'Play'.
3. If the 'Save separate files' option was enabled in the main window, the drop-down menu will be displayed to choose whether to play microphone only, system only or both (default 'Both').
4. Pressing 'Play' starts the WAV playback asynchronously. The button changes to 'Stop' during playback. When the track is finished, it will return to 'Play'.
5. If you press 'Close' while recording, you will be asked if you want to cancel the test (the files will be deleted). If you have already recorded and/or finished, it will simply close and also delete the files.

You cannot close with Alt+F4 or with the X in the window; only with the 'Close' button.
 State Stereo French General Recording Recording completed. File saved as:
{file_path} Recording... (No stop hotkey is assigned) Recording... (Use {hk} to stop) Save separate microphone and s&ystem files A recording is in progress, do you want to stop it and exit? Language Information English Italian The combination must have at least two modifiers and a main key. The combination is in use by another application: Recording is still in progress, do you want to cancel the sound check? User's Manual Micr&ophone: Minimize to system tray recordin&g mode: Mono Show application The file to be played does not exist You cannot assign the same combination to Start and Stop.
Please choose a different one.
The changes will revert to the default. Nothing has been recorded yet. Stop recording first. Could not open recordings directory: {error} Options To apply the new language you need to restart the application.
do you want to continue? Please wait, converting to final format... Please wait, finalizing conversion... Portuguese Processing Audio Test Microphone test System test Play Exit Invalid key detected. Keyboard Turkish WASAPIRecording
Version {}
Created by {} WASAPIRecording is already running.

It is not possible to have two instances at the same time. invite me to a &coffee if you like my work 