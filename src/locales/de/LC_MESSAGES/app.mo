��    e      D  �   l      �  [  �  S   �   V   A!     �!     �!     �!  	   �!     �!     �!     �!     �!     "     $"     3"     G"     W"     j"     q"     u"     �"  $   �"     �"     �"     �"     �"  ,   #     9#     K#     S#     a#     n#     v#     |#     �#     �#     �#     �#     �#  %   �#  %   �#     $     8$     S$     d$     l$  (   y$  !   �$  :   �$     �$  &   %  (   ,%     U%     f%     o%     �%  �  �%     N)     U)     ^)     g)  
   o)  9   z)  /   �)  #   �)  3   *  7   <*     t*     {*     �*     �*  L   �*  3   �*  C   +     ^+     l+  "   y+     �+     �+     �+  !   �+  �   �+  :   �,  6   �,     �,  U   �,  1   Q-  ,   �-  
   �-  
   �-     �-     �-     �-  
   �-     .     .     #.     +.  )   1.  [   [.  ,   �.  :  �.  4  0  F   TK  I   �K     �K     �K     L  
   L     #L     /L     5L     GL     WL     qL     L     �L     �L     �L     �L     �L     �L  5   �L     M     /M     3M     JM  E   _M     �M     �M     �M     �M     �M     �M     �M  	   �M     N     N     )N  
   >N  %   IN  %   oN     �N  #   �N     �N     �N     �N     O  $   %O  >   JO     �O  +   �O  /   �O     �O     �O     P     !P  o  >P     �T     �T     �T  	   �T     �T  <   �T  *   U  1   DU  .   vU  ?   �U     �U     �U     �U     V  W   V  C   fV  B   �V     �V     �V     
W     *W     DW     IW  '   \W  �   �W  G   ,X  �   tX     �X  _   Y  ,   cY  1   �Y     �Y     �Y  
   �Y     �Y     �Y     Z  	   Z      Z     <Z  	   EZ  *   OZ  r   zZ  A   �Z                K           c          ;           b       "       8   1                 J   0          &   #       N   -   Y          >   G   5   )   _   =         <              ]   2      9   C   Z   W       4   %   F         A   R   	   /   I          V   [          ?   H   P       (   Q   ,          T   `          *          '   X       B       L                    E   @   
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
Language: de
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: Poedit 3.5
X-Poedit-SourceCharset: UTF-8
 
1. was ist WASAPIRecording?
 
WASAPIRecording ist eine Windows-Anwendung, mit der Sie Ihr Mikrofon-Audio und Ihr System-Audio (Musik, Videoanrufe usw.) gleichzeitig aufnehmen können. Sie können beides in einer Datei kombinieren oder getrennt speichern (eine für das Mikrofon und eine für das Systemaudio).
 
2. Anforderungen
 
- Windows 10 oder höher (mit WASAPI).
- Berechtigungen zum Ausführen der Anwendung.
 
3. Starten Sie die Anwendung
 
- Führen Sie die Datei oder die Verknüpfung mit dem Namen "WASAPIRecording" aus.
- Es öffnet sich das Hauptfenster mit Steuerelementen für Mikrofon, System, Audioformate usw.
 
4. Geräte und Parameter konfigurieren
 
- Mikrofon: Wählen Sie das Mikrofon, das Sie verwenden möchten.
- System (Loopback): Wählen Sie das Gerät auf Ihrem PC aus, das alles aufnimmt, was auf dem System erklingt.
- Geräte aktualisieren: Wenn Sie ein neues Gerät angeschlossen haben und es nicht angezeigt wird, klicken Sie hier, um die Liste zu aktualisieren.
- Qualität (Hz): Wählen Sie die Abtastrate (22050, 44100 oder 48000). Je höher die Zahl ist, desto höher ist die Qualität und desto größer ist die Datei.
- Ausgabeformat: Sie können zwischen WAV, MP3, FLAC, OGG oder AIFF wählen.
- MP3-Bitrate: Wird nur angezeigt, wenn Sie MP3 wählen; stellen Sie die Kompressionsqualität ein.
- Aufnahmemodus (Mono oder Stereo): Legen Sie fest, wie viele Kanäle Ihre endgültige Aufnahme haben soll.
- Mono-Mischung aktivieren:
- Wenn Sie feststellen, dass Ihr Ton getrennt wird (z. B. Mikrofon nur auf einer Seite, System auf der anderen), aktivieren Sie dieses Kontrollkästchen, um beide Kanäle zu mischen und den Ton zu bündeln.
- In der Praxis werden alle Töne in einem einzigen Kanal kombiniert und nach links und rechts übertragen, so dass der Eindruck vermieden wird, dass sich der Ton zu einer Seite "neigt".
- Separate Dateien speichern:
- Wenn dieses Kontrollkästchen aktiviert ist, erstellt die App nicht nur eine "kombinierte" Datei, sondern speichert auch zwei weitere Einzeldateien: eine nur vom Mikrofon und eine vom System.
 
5. Lautstärke anpassen
 
- Mikrofonlautstärke: Verwenden Sie den Schieberegler, um die Mikrofonverstärkung zu erhöhen oder zu verringern.
- Systemlautstärke: Erhöht oder verringert die Verstärkung der PC-Töne.
 
6. Aufnahme starten und stoppen
 
- Drücken Sie auf Aufnahme starten (oder verwenden Sie standardmäßig die Tastenkombination "Strg + Umschalt + F1"). Im Status wird "Aufnahme..." angezeigt.
- Um die Aufnahme zu beenden, klicken Sie auf Aufnahme stoppen (oder "Strg + Umschalt + F2").
- Wenn Sie MP3, FLAC, OGG oder AIFF gewählt haben, konvertiert die App die endgültige Datei nach der Aufnahme; es erscheint die Meldung "Bitte warten...".
- Wenn die Konvertierung abgeschlossen ist, wird eine Aufforderung mit dem Pfad angezeigt, in dem die Dateien gespeichert wurden.
 
7. Wo die Aufnahmen gespeichert werden
 
- Sie werden in einem Ordner namens "Aufnahme" gespeichert, der sich im Anwendungsordner befindet.
- Vom Hauptfenster aus können Sie diesen Ordner öffnen, indem Sie auf Menü > Aufzeichnungen öffnen klicken.
 
8. Optionen und Menü
 
- Im Hauptfenster gibt es eine Schaltfläche namens Menü:
- Über...: Zeigt die Version von WASAPIRecording und den Namen des Erstellers an.
- Aufzeichnungen öffnen: Öffnet den Ordner, in dem sich die aufgezeichneten Dateien befinden.
- Sprache: Wählen Sie Ihre bevorzugte Sprache. Sie müssen die Anwendung neu starten, um die Änderung zu übernehmen.
- Optionen:
- Hier finden Sie das Dialogfeld Optionen mit zwei Abschnitten:
- Allgemein: Aktivieren Sie das Kontrollkästchen "In die Taskleiste minimieren", um das Fenster auszublenden und ein Symbol in der Taskleiste zu hinterlassen, wenn Sie es minimieren.
- Tastatur: Hier können Sie die globalen Tastenkombinationen zum Starten und Beenden der Aufnahme ändern. Wenn sie nicht funktionieren oder sich wiederholen, können Sie sie hier anpassen.
 
9. Audio-Test
 
- Die Schaltfläche Audiotest öffnet einen Dialog, mit dem Sie einige Sekunden an Samples aufnehmen und sofort wiedergeben können.
- Dieser Dialog:
- Wird immer im Vordergrund geöffnet.
- Er wird nicht mit "X" oder Alt+F4 geschlossen, sondern nur mit der Schaltfläche "Schließen".
- Zuerst nehmen Sie auf ("Stop"-Taste zum Beenden der Aufnahme).
- Dann können Sie das Aufgenommene abspielen".
- Wenn Sie "Getrennte Dateien speichern" aktiviert haben, können Sie wählen, ob nur das Mikrofon, nur das System oder beides wiedergegeben werden soll.
- Wenn Sie diesen Dialog schließen, werden die temporären Dateien gelöscht, so dass Sie sich vor der endgültigen Aufnahme vergewissern können, dass alles gut klingt.
 
10. Tastaturkurzbefehle
 
Globale Tastenkombinationen (standardmäßig, Sie können sie unter Optionen > Tastatur ändern):
- Aufnahme starten: Strg + Umschalt + F1
- Aufnahme stoppen: Strg + Umschalttaste + F2
Tastenkombinationen innerhalb der Benutzeroberfläche (mit der Alt-Taste):
- Mikrofon: Alt + O
- System (Rückkopplung): Alt + S
- Geräte aktualisieren: Alt + R
- Qualität (Hz): Alt + C
- Ausgabeformat: Alt + F
- MP3-Bitrate (kbps): Alt + B
- Aufnahmemodus: Alt + G
- Mono-Mix aktivieren: Alt + H
- Separate Mikrofon- und Systemdateien speichern: Alt + Y
- Mikrofonlautstärke: Alt + V
- System-Lautstärke: alt + V
- Aufnahme starten: Alt + I
- Aufnahme stoppen: Alt + D
- Audiotest: Alt + P
- Menü: Alt + M
- Schließen (in einigen Dialogen): Alt + C
- Je nach Sprache können einige Buchstaben variieren.
 
11. In Ablage minimieren
 
- Wenn Sie in den Optionen (Registerkarte "Allgemein") die Option "In die Taskleiste minimieren" aktiviert haben, verschwindet das Fenster von der Taskleiste, wenn Sie die Windows-Schaltfläche zum Minimieren drücken, und ein Symbol wird in der Nähe der Systemuhr angezeigt.
- Auf das Symbol in der Taskleiste können Sie doppelklicken, um das Fenster wiederherzustellen, oder das Kontextmenü verwenden, um die Anwendung anzuzeigen oder zu schließen.
 
12. Schließen Sie die Anwendung
 
- Wenn Sie das Hauptfenster schließen, werden Sie bei einer Aufnahme gefragt, ob Sie die Aufnahme vor dem Beenden beenden möchten.
- Wenn die Datei in MP3/FLAC/etc. konvertiert wird, wartet das Programm, bis die Konvertierung abgeschlossen ist.
- Danach wird das Programm vollständig geschlossen.
 
13. Abschließende Tipps
 
- Passen Sie die System- und Mikrofonlautstärke in der App selbst an, um Ihre Audioquellen auszugleichen.
- Wenn etwas nicht richtig klingt, verwenden Sie den Audiotest, um es zu überprüfen und anzupassen, bevor Sie endgültig aufnehmen.
- Wenn der Ton auf einem Kanal (links oder rechts) "verzerrt" ist, aktivieren Sie "Mono-Mixing aktivieren", um den Ton zu zentrieren.
 
viel Spaß beim Aufnehmen mit WASAPIRecording! Wenn Ihnen diese Anwendung gefällt, gehen Sie zu "Menü > Laden Sie mich auf einen Kaffee ein", um die Entwicklung der Anwendung zu unterstützen.
 
Separate Mikrofon-Datei: {mic_path}
Getrennte Systemdatei: {sys_path} 
Separate Mikrofon-Datei: {mic_path}
Getrennte Systemdatei: {system_path} &Akzeptieren &Bitrate MP3 (kbps): &Qualität (Hz): &Abbrechen &Schließen &Halt &Aufnahme stoppen &Ausgabeformat: mono-Mischung einschalten &Information: &Aufnahme starten &Benutzerhandbuch: &Benutzerhandbuch &Menü &Nein &Audio Test &Auffrischungsgeräte wählen Sie aus, welche Datei abgespielt werden soll: &System (Loopback): &Ja &Mikrofon-Lautstärke: &System Lautstärke: &laden Sie mich zu einem Kaffee ein, wenn Ihnen meine Arbeit gefällt Offene Aufzeichnungen Akzeptieren Über &de... Über... Deutsch Beide Benachrichtigung Abbrechen Test abbrechen Capture Hotkey Home Erfassen Hotkey Stop Schließen Kombination zum Beenden der Aufnahme: Kombination zum Starten der Aufnahme: Konfiguration der Aufzeichnung Bestätigen Sie die Sprachänderung Bestätigung der Schließung Anhalten Geräte Korrekt aktualisierte Geräte. Standby (zum Starten {hk} verwenden) Standby. Tasten in den Optionen zuweisen oder manuell starten. Fehler Fehler beim Konvertieren der Datei: {error} Fehler beim Aktualisieren von Geräten: {error} Hotkey-Fehler Spanisch Warten auf die Kombination... Bitte warten... Verarbeitung In diesem Fenster können Sie eine Testaufnahme und -wiedergabe durchführen.

1. Wenn es geöffnet wird, beginnt die Aufnahme mit denselben Einstellungen wie im Hauptfenster.
2. Um die Aufnahme zu beenden, drücken Sie auf "Stopp". Die Schaltfläche ändert sich dann in "Wiedergabe".
3. Wenn die Option "Separate Dateien speichern" im Hauptfenster aktiviert wurde, wird das Dropdown-Menü angezeigt, in dem Sie wählen können, ob nur das Mikrofon, nur das System oder beides wiedergegeben werden soll (Standardeinstellung: "Beide").
4. Durch Drücken von "Play" wird die WAV-Wiedergabe asynchron gestartet. Die Schaltfläche ändert sich während der Wiedergabe in "Stop". Nach Beendigung des Titels wird sie wieder zu "Play".
5. Wenn Sie während der Aufnahme auf "Schließen" drücken, werden Sie gefragt, ob Sie den Test abbrechen möchten (die Dateien werden gelöscht). Wenn Sie bereits aufgezeichnet und/oder die Aufnahme beendet haben, wird sie einfach geschlossen und die Dateien werden ebenfalls gelöscht.

Sie können nicht mit Alt+F4 oder mit dem X im Fenster schließen, sondern nur mit der Schaltfläche "Schließen".
 Status Stereo Französisch Allgemein Aufnahme Aufnahme abgeschlossen. Datei gespeichert unter:
{file_path} Aufnahme... (Kein Stopp-Hotkey zugewiesen) Aufnahme... (Mit {hk} wird die Aufnahme gestoppt) Separate Mikrofon- und Systemdateien speichern Eine Aufzeichnung läuft. Möchten Sie sie stoppen und beenden? Sprache Informacion Englisch Italienisch Die Kombination muss mindestens zwei Modifikatoren und einen Hauptschlüssel enthalten. Die Kombination wird bereits von einer anderen Anwendung verwendet: Die Aufnahme ist noch im Gange, wollen Sie den Soundcheck absagen? Benutzerhandbuch Mikrofon&o: In den Systembereich minimieren Aufnahme & Aufnahmemodus: Affe Anwendung anzeigen Die abzuspielende Datei existiert nicht Sie können Start und Stopp nicht dieselbe Kombination zuweisen.
Bitte wählen Sie eine andere Kombination.
Die Änderungen werden auf den Standardwert zurückgesetzt. Es ist noch nichts aufgenommen worden. Stoppen Sie zuerst die Aufnahme. Aufnahmeverzeichnis konnte nicht geöffnet werden: {error} {error} {error} {error} {error} {error} {error} {error} {error} {error} [0 Optionen Um die neue Sprache anzuwenden, müssen Sie die Anwendung neu starten.
möchten Sie fortfahren? Bitte warten, Konvertierung ins Endformat... Bitte warten, Konvertierung wird abgeschlossen... Portugiesisch Verarbeitung Audio-Test Mikrofon-Test Systemprüfung Wiedergeben Verlassen Ungültiger Schlüssel entdeckt. Tastatur Türkisch WASAPIRecording
Version {}
Erstellt von {} Die WASAPIR-Aufnahmen sind bereits im Gange.

Es ist nicht möglich, zwei Instanzen gleichzeitig laufen zu lassen. laden Sie mich auf einen Kaffee ein, wenn Sie meine Arbeit mögen 