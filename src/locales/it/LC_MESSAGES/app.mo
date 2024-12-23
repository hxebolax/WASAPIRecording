��    e      D  �   l      �  [  �  S   �   V   A!     �!     �!     �!  	   �!     �!     �!     �!     �!     "     $"     3"     G"     W"     j"     q"     u"     �"  $   �"     �"     �"     �"     �"  ,   #     9#     K#     S#     a#     n#     v#     |#     �#     �#     �#     �#     �#  %   �#  %   �#     $     8$     S$     d$     l$  (   y$  !   �$  :   �$     �$  &   %  (   ,%     U%     f%     o%     �%  �  �%     N)     U)     ^)     g)  
   o)  9   z)  /   �)  #   �)  3   *  7   <*     t*     {*     �*     �*  L   �*  3   �*  C   +     ^+     l+  "   y+     �+     �+     �+  !   �+  �   �+  :   �,  6   �,     �,  U   �,  1   Q-  ,   �-  
   �-  
   �-     �-     �-     �-  
   �-     .     .     #.     +.  )   1.  [   [.  ,   �.  :  �.  �  0  M   �I  P   9J     �J     �J     �J     �J     �J     �J     �J     �J     �J     K     &K     >K     MK     [K     aK  
   eK     pK  "   �K     �K     �K     �K     �K  9   �K     %L  	   :L     DL     [L     mL     uL     ~L  	   �L     �L  #   �L  #   �L     �L  /   �L  *   $M  "   OM     rM     �M     �M     �M  %   �M  %   �M  <   	N     FN  *   MN  7   xN  !   �N     �N     �N     �N    O     "S     (S     /S     8S     AS  8   OS  T   �S  3   �S  3   T  B   ET     �T     �T     �T     �T  I   �T  7   �T  C   /U     sU     �U  -   �U  +   �U     �U     �U      V  �   %V  J   �V  �   W     �W  X   �W  1   X  .   6X  
   eX     pX  
   }X     �X     �X     �X     �X     �X     �X     �X  (   �X  e   Y  3   uY                K           c          ;           b       "       8   1                 J   0          &   #       N   -   Y          >   G   5   )   _   =         <              ]   2      9   C   Z   W       4   %   F         A   R   	   /   I          V   [          ?   H   P       (   Q   ,          T   `          *          '   X       B       L                    E   @   
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
PO-Revision-Date: 2024-12-23 15:31+0100
Last-Translator: 
Language-Team: 
Language: it
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: Poedit 3.5
X-Poedit-SourceCharset: UTF-8
 
1. che cos'è il WASAPIRecording?
 
WASAPIRecording è un'applicazione Windows che consente di registrare contemporaneamente l'audio del microfono e l'audio del sistema (musica, videochiamate, ecc.). È possibile combinare entrambi in un unico file o salvarli separatamente (uno per il microfono e uno per l'audio di sistema).
 
2. Requisiti
 
- Windows 10 o superiore (con WASAPI).
- Permessi per l'esecuzione dell'applicazione.
 
3. Avviare l'applicazione
 
- Eseguire il file o il collegamento chiamato "WASAPIRecording".
- Si aprirà la finestra principale con i controlli per il microfono, il sistema, i formati audio, ecc.
 
4. Configurazione di dispositivi e parametri
 
- Microfono: selezionare il microfono che si desidera utilizzare.
- Sistema (loopback): selezionare il dispositivo del PC che cattura tutti i suoni del sistema.
- Aggiorna dispositivi: se è stato collegato un nuovo dispositivo e non appare, fare clic qui per aggiornare l'elenco.
- Qualità (Hz): scegliere la frequenza di campionamento (22050, 44100 o 48000). Più alto è il numero, più alta è la qualità e più pesante il file.
- Formato di uscita: è possibile scegliere WAV, MP3, FLAC, OGG o AIFF.
- Bitrate MP3: viene visualizzato solo se si sceglie MP3; regola la qualità di compressione.
- Modalità di registrazione (Mono o Stereo): Decidere quanti canali avrà la registrazione finale.
- Attiva missaggio mono:
- Se si nota che l'audio viene separato (ad esempio, il microfono solo da un lato e il sistema dall'altro), selezionare questa casella per miscelare entrambi i canali e concentrare il suono.
- In pratica, tutti i suoni vengono combinati in un unico canale e replicati a sinistra e a destra, evitando la sensazione che l'audio sia "inclinato" verso un lato.
- Salva file separati:
- Se selezionata, oltre a creare un file "combinato", l'applicazione salverà altri due file individuali: uno solo dal microfono e uno dal sistema.
 
5. Regola i volumi
 
- Volume del microfono: utilizzare il cursore per aumentare o diminuire il guadagno del microfono.
- Volume del sistema: alza o abbassa il guadagno dei suoni del PC.
 
6. Avvio e interruzione della registrazione
 
- Premere Avvia registrazione (o utilizzare la scorciatoia globale "Ctrl + Shift + F1"). Lo stato mostrerà "Registrazione...".
- Per interrompere, fare clic su Interrompi registrazione (o "Ctrl + Shift + F2").
- Se si è scelto MP3, FLAC, OGG o AIFF, l'applicazione convertirà il file finale dopo la registrazione; apparirà un messaggio "Attendere prego...".
- Al termine, verrà visualizzato un messaggio con il percorso in cui sono stati salvati i file.
 
7. Dove vengono salvate le registrazioni
 
- Le registrazioni vengono salvate in una cartella denominata "recording", all'interno della cartella dell'applicazione.
- Dalla finestra principale, è possibile aprire questa cartella facendo clic su Menu > Apri registrazioni.
 
8. Opzioni e menu
 
- Nella finestra principale è presente un pulsante denominato Menu:
- Informazioni su...: visualizza la versione di WASAPIRecording e il nome del creatore.
- Apri registrazioni: Apre la cartella in cui si trovano i file registrati.
- Lingua: consente di scegliere la lingua preferita. Per applicare la modifica è necessario riavviare l'applicazione.
- Opzioni:
- Qui si trova la finestra di dialogo Opzioni, con due sezioni:
- Generale: Includere la casella di controllo "Riduci a icona nella barra delle applicazioni" per nascondere la finestra e lasciare un'icona nella barra delle applicazioni quando si riduce a icona.
- Tastiera: serve a modificare le scorciatoie globali per avviare e interrompere la registrazione. Se non funzionano o sono ripetute, è possibile modificarle qui.
 
9. Test audio
 
- Il pulsante Test audio apre una finestra di dialogo per registrare alcuni secondi di campioni e riprodurli immediatamente.
- Questa finestra di dialogo:
- Si apre sempre in primo piano.
- Non si chiude con "X" o Alt+F4, ma solo con il pulsante Chiudi.
- Prima si registra (pulsante "Stop" per terminare la registrazione).
- Poi si può "riprodurre" ciò che si è registrato.
- Se è stata selezionata l'opzione "Salva file separati", è possibile scegliere di riprodurre solo il microfono, solo il sistema o entrambi.
- Quando si chiude questa finestra di dialogo, i file temporanei vengono cancellati, quindi è perfetta per verificare che tutto suoni bene prima di effettuare la registrazione finale.
 
10. Scorciatoie da tastiera
 
Scorciatoie globali (predefinite, si possono modificare in Opzioni > Tastiera):
- Avvia registrazione: Ctrl + Maiusc + F1
- Interruzione della registrazione: Ctrl + Maiusc + F2
Scorciatoie all'interno dell'interfaccia (con il tasto Alt):
- Microfono: Alt + O
- Sistema (loopback): Alt + S
- Aggiorna dispositivi: Alt + R
- Qualità (Hz): Alt + C
- Formato di uscita: Alt + F
- Bitrate MP3 (kbps): Alt + B
- Modalità di registrazione: Alt + G
- Abilita mix mono: Alt + H
- Salva i file separati del microfono e del sistema: Alt + Y
- Volume del microfono: Alt + V
- Volume del sistema: : Alt + V
- Avvio della registrazione: Alt + I
- Interruzione della registrazione: Alt + D
- Test audio: Alt + P
- Menu: Alt + M
- Chiudi (in alcune finestre di dialogo): Alt + C
- A seconda della lingua, alcune lettere possono variare.
 
11. Riduci a icona nel vassoio
 
- Se nelle Opzioni (scheda "Generale") è stata attivata l'opzione "Riduci a icona", quando si preme il pulsante di riduzione a icona di Windows, la finestra scompare dalla barra delle applicazioni e viene visualizzata un'icona vicino all'orologio di sistema.
- Dall'icona nell'area di notifica, è possibile fare doppio clic per ripristinare la finestra o utilizzare il menu contestuale per mostrare/chiudere l'applicazione.
 
12. Chiudere l'applicazione
 
- Quando si chiude la finestra principale, se si sta registrando, viene chiesto se si desidera interrompere la registrazione prima di uscire.
- Se il file è in fase di conversione in MP3/FLAC/etc., l'applicazione attenderà il termine della conversione.
- Quindi si chiuderà completamente.
 
13. Suggerimenti finali
 
- Regolare il volume del sistema e del microfono all'interno dell'applicazione stessa per bilanciare le fonti audio.
- Se qualcosa non suona bene, usare il Test audio per controllare e regolare prima di registrare definitivamente.
- Se l'audio è "skewed" su un canale (destro o sinistro), selezionare "Enable Mono Mixing" per centrare il suono.
 
divertitevi a registrare con WASAPIRecording! Se vi piace questa applicazione, andate su "Menu > invitami per un caffè" per sostenerne lo sviluppo.
 
File del microfono separato: {mic_path}
File di sistema separato: {sys_path} 
File del microfono separato: {mic_path}
File di sistema separato: {system_path} accetta bitrate MP3 (kbps): qualità (Hz): &Annulla chiudere &Stop &Arresta la registrazione formato di uscita: abilita la miscelazione mono &Informazioni: &Avvia la registrazione manuale d'uso: manuale d'uso &Menu &No test audio dispositivi &Refresh selezionare il file da riprodurre: &Sistema (loopback): sì volume del microfono: volume del sistema: invitatemi a prendere un caffè se vi piace il mio lavoro Registrazioni aperte Accettare Informazioni su &de... A proposito di... Tedesco Entrambi Notare Annullare Annullamento del test Cattura tasti di scelta rapida Home Cattura tasto di scelta rapida Stop Chiudi Combinazione per interrompere la registrazione: Combinazione per avviare la registrazione: Configurazione della registrazione Confermare il cambio di lingua Confermare la chiusura Fermarsi Dispositivi Dispositivi correttamente aggiornati. Standby (utilizzare {hk} per avviare) Standby. Assegnare i tasti in Opzioni o avviare manualmente. Errore Errore nella conversione del file: {error} Errore durante l'aggiornamento dei dispositivi: {error} Errore dei tasti di scelta rapida Spagnolo In attesa della combinazione... Attendere prego... Elaborazione Questa finestra consente di eseguire una registrazione e una riproduzione di prova.

1. Quando viene aperta, inizia la registrazione con le stesse impostazioni della finestra principale.
2. Per terminare la registrazione, premere "Stop". Il pulsante cambia quindi in "Riproduci".
3. Se nella finestra principale è stata attivata l'opzione "Salva file separati", verrà visualizzato il menu a discesa per scegliere se riprodurre solo il microfono, solo il sistema o entrambi (impostazione predefinita "Entrambi").
4. Premendo 'Play' si avvia la riproduzione WAV in modo asincrono. Il pulsante cambia in 'Stop' durante la riproduzione. Quando la traccia è terminata, torna a 'Play'.
5. Se si preme 'Chiudi' durante la registrazione, verrà chiesto se si desidera annullare il test (i file verranno cancellati). Se la registrazione è già stata effettuata e/o terminata, si chiuderà semplicemente e si cancelleranno anche i file.

Non è possibile chiudere con Alt+F4 o con la X nella finestra, ma solo con il pulsante "Chiudi".
 Stato Stereo Francese Generico Registrazione Registrazione completata. File salvato come:
{file_path} Registrazione... (Non è stato assegnato alcun tasto di scelta rapida per l'arresto) Registrazione... (Utilizzare {hk} per interrompere) Salvate i file separati del microfono e del sistema È in corso una registrazione, si desidera interromperla e uscire? Lingua Informazioni Inglese Italiano La combinazione deve avere almeno due modificatori e un tasto principale. La combinazione è utilizzata da un'altra applicazione: La registrazione è ancora in corso, vuole annullare il soundcheck? Manuale d'uso Microfono&o: Riduci a icona nella barra delle applicazioni Registrazione e modalità di registrazione: Scimmia Mostra applicazione Il file da riprodurre non esiste Non è possibile assegnare la stessa combinazione a Start e Stop.
Scegliere una combinazione diversa.
Le modifiche verranno ripristinate come predefinite. Non è stato ancora registrato nulla. Interrompere prima la registrazione. Non è stato possibile aprire la directory di registrazione: {error} {error} {error} {error} {error} {error} {error} {error} {error} {error} {error} [0 Opzioni Per applicare la nuova lingua è necessario riavviare l'applicazione.
volete continuare? Attendere prego, conversione in formato finale... Attendere prego, finalizzare la conversione... Portoghese Elaborazione Test audio Test del microfono Test del sistema Gioco Uscire Rilevato un tasto non valido. Tastiera Turco WASAPIRecording
Versione {}
Creato da {} La registrazione di WASAPIR è già in corso.

Non è possibile avere due istanze contemporaneamente. invitatemi per un &caffè se vi piace il mio lavoro 