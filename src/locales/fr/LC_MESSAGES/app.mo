��    e      D  �   l      �  [  �  S   �   V   A!     �!     �!     �!  	   �!     �!     �!     �!     �!     "     $"     3"     G"     W"     j"     q"     u"     �"  $   �"     �"     �"     �"     �"  ,   #     9#     K#     S#     a#     n#     v#     |#     �#     �#     �#     �#     �#  %   �#  %   �#     $     8$     S$     d$     l$  (   y$  !   �$  :   �$     �$  &   %  (   ,%     U%     f%     o%     �%  �  �%     N)     U)     ^)     g)  
   o)  9   z)  /   �)  #   �)  3   *  7   <*     t*     {*     �*     �*  L   �*  3   �*  C   +     ^+     l+  "   y+     �+     �+     �+  !   �+  �   �+  :   �,  6   �,     �,  U   �,  1   Q-  ,   �-  
   �-  
   �-     �-     �-     �-  
   �-     .     .     #.     +.  )   1.  [   [.  ,   �.  :  �.  m  0  P   �K  S   �K     2L  %   ?L     eL     vL     L     �L     �L     �L     �L     �L     �L     �L     M     -M     3M     8M  !   DM  "   fM     �M     �M     �M     �M  :   �M     
N     !N     *N     >N     NN     WN     `N     eN     mN     }N  -   �N     �N  ,   �N  !   �N  !   O  !   7O     YO     pO     yO  %   �O  %   �O  I   �O     $P  )   +P  <   UP     �P     �P     �P      �P  `  �P     XU     ^U  	   gU  	   qU     {U  ?   �U  G   �U  /   V  B   BV  B   �V     �V     �V     �V     �V  Q   �V  8   >W  K   wW     �W     �W  *   �W  )   X     ?X     EX     YX  �   yX  E    Y  �   fY     �Y  `   �Y  A   TZ  4   �Z  	   �Z  
   �Z  
   �Z     �Z     �Z     [     [     [     ;[     C[  /   H[  k   x[  9   �[                K           c          ;           b       "       8   1                 J   0          &   #       N   -   Y          >   G   5   )   _   =         <              ]   2      9   C   Z   W       4   %   F         A   R   	   /   I          V   [          ?   H   P       (   Q   ,          T   `          *          '   X       B       L                    E   @   
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
Language: fr
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: Poedit 3.5
X-Poedit-SourceCharset: UTF-8
 
1. qu'est-ce que l'enregistrement WASAPIR ?
 
WASAPIRecording est une application Windows qui vous permet d'enregistrer simultanément l'audio de votre microphone et l'audio du système (musique, appels vidéo, etc.). Vous pouvez combiner les deux dans un seul fichier ou les enregistrer séparément (un pour le microphone et un pour l'audio du système).
 
2. Exigences
 
- Windows 10 ou supérieur (avec WASAPI).
- Permissions d'exécuter l'application.
 
3. Lancer l'application
 
- Lancez le fichier ou le raccourci appelé "WASAPIRecording".
- La fenêtre principale s'ouvre avec des commandes pour le microphone, le système, les formats audio, etc.
 
4. Configurer les appareils et les paramètres
 
- Microphone : sélectionnez le microphone que vous souhaitez utiliser.
- Système (bouclage) : sélectionnez le périphérique sur votre PC qui capture tout ce qui est entendu sur le système.
- Actualiser les appareils : si vous avez connecté un nouvel appareil et qu'il n'apparaît pas, cliquez ici pour actualiser la liste.
- Qualité (Hz) : choisissez la fréquence d'échantillonnage (22050, 44100 ou 48000). Plus le chiffre est élevé, plus la qualité est grande et plus le fichier est lourd.
- Format de sortie : Vous pouvez choisir WAV, MP3, FLAC, OGG ou AIFF.
- Bitrate MP3 : ne s'affiche que si vous choisissez MP3 ; permet de régler la qualité de la compression.
- Mode d'enregistrement (mono ou stéréo) : Déterminez le nombre de canaux de votre enregistrement final.
- Activer le mixage mono :
- Si vous remarquez que votre son est séparé (par exemple, le microphone d'un côté seulement, le système de l'autre), cochez cette case pour mélanger les deux canaux et concentrer le son.
- En pratique, tous les sons sont combinés en un seul canal et reproduits à gauche et à droite, ce qui évite de donner l'impression que l'audio "penche" d'un côté.
- Enregistrer des fichiers séparés :
- Si cette case est cochée, en plus de créer un fichier "combiné", l'application enregistrera deux autres fichiers individuels : l'un provenant du microphone uniquement et l'autre du système.
 
5. Régler les volumes
 
- Volume du microphone : utilisez le curseur pour augmenter ou diminuer le gain du microphone.
- Volume du système : Augmente ou diminue le gain des sons de l'ordinateur.
 
6. Démarrer et arrêter l'enregistrement
 
- Appuyez sur Démarrer l'enregistrement (ou utilisez le raccourci global "Ctrl + Shift + F1" par défaut). L'état affichera "Enregistrement...".
- Pour arrêter, cliquez sur Arrêter l'enregistrement (ou "Ctrl + Shift + F2").
- Si vous avez choisi MP3, FLAC, OGG ou AIFF, l'application convertira le fichier final après l'enregistrement ; un message "Veuillez patienter..." apparaîtra.
- Une fois l'opération terminée, vous verrez apparaître une invite indiquant le chemin d'accès où vos fichiers ont été enregistrés.
 
7. Où sont sauvegardés les enregistrements
 
- Les enregistrements sont stockés dans un dossier appelé "recording", qui se trouve dans le dossier de l'application.
- Dans la fenêtre principale, vous pouvez ouvrir ce dossier en cliquant sur Menu > Ouvrir les enregistrements.
 
8. Options et menu
 
- Dans la fenêtre principale, il y a un bouton appelé Menu :
- A propos de... : Affiche la version de WASAPIRecording et le nom du créateur.
- Ouvrir les enregistrements : Ouvre le dossier dans lequel se trouvent les fichiers enregistrés.
- Langue : Choisissez votre langue préférée. Vous devrez redémarrer l'application pour appliquer le changement.
- Options :
- Vous trouverez ici la boîte de dialogue Options, qui comporte deux sections :
- Général : cochez la case "Minimiser dans la barre d'état système" pour masquer la fenêtre et laisser une icône dans la barre d'état lorsque vous la minimisez.
- Clavier : permet de modifier les raccourcis globaux pour démarrer et arrêter l'enregistrement. S'ils ne fonctionnent pas ou sont répétés, vous pouvez les ajuster ici.
 
9. Test audio
 
- Le bouton Test audio ouvre une boîte de dialogue permettant d'enregistrer quelques secondes d'échantillons et de les lire immédiatement.
- Cette boîte de dialogue :
- s'ouvre toujours au premier plan.
- Elle ne se ferme pas avec "X" ou Alt+F4, mais uniquement avec le bouton Fermer.
- Vous commencez par enregistrer (bouton "Stop" pour terminer l'enregistrement).
- Ensuite, vous pouvez "lire" ce que vous avez enregistré.
- Si vous avez coché la case "Enregistrer des fichiers séparés", vous pouvez choisir de ne lire que le microphone, que le système ou les deux.
- Lorsque vous fermez cette boîte de dialogue, les fichiers temporaires sont supprimés. Elle est donc idéale pour vérifier que tout sonne bien avant de procéder à l'enregistrement final.
 
10. Raccourcis clavier
 
Raccourcis globaux (par défaut, vous pouvez les modifier dans Options > Clavier) :
- Démarrer l'enregistrement : Ctrl + Shift + F1
- Arrêter l'enregistrement : Ctrl + Shift + F2
Raccourcis dans l'interface (avec la touche Alt) :
- Microphone : Alt + O
- Système (bouclage) : Alt + S
- Rafraîchir les appareils : Alt + R
- Qualité (Hz) : Alt + C
- Format de sortie : Alt + F
- Bitrate MP3 (kbps) : Alt + B
- Mode d'enregistrement : Alt + G
- Activer le mixage mono : Alt + H
- Enregistrer des fichiers séparés pour le microphone et le système : Alt + Y
- Volume du microphone : Alt + V
- Volume du système : alt + V
- Démarrer l'enregistrement : Alt + I
- Arrêt de l'enregistrement : Alt + D
- Test audio : Alt + P
- Menu : Alt + M
- Fermer (dans certains dialogues) : Alt + C
- Selon la langue, certaines lettres peuvent varier.
 
11. Minimiser dans le bac
 
- Si, dans les Options (onglet "Général"), vous avez activé l'option "Minimiser dans la barre des tâches", lorsque vous appuyez sur le bouton de minimisation de Windows, la fenêtre disparaît de la barre des tâches et une icône s'affiche près de l'horloge système.
- À partir de l'icône dans la barre des tâches, vous pouvez double-cliquer pour restaurer la fenêtre ou utiliser le menu contextuel pour afficher/fermer l'application.
 
12. Fermer l'application
 
- Lors de la fermeture de la fenêtre principale, si vous enregistrez, il vous sera demandé si vous souhaitez arrêter l'enregistrement avant de quitter l'application.
- Si le fichier est converti en MP3/FLAC/etc., l'application attendra que la conversion soit terminée.
- L'application se ferme ensuite complètement.
 
13. Derniers conseils
 
- Réglez le volume du système et du microphone dans l'application elle-même pour équilibrer vos sources audio.
- Si quelque chose ne sonne pas bien, utilisez le test audio pour vérifier et ajuster avant d'enregistrer pour de bon.
- Si l'audio est "biaisé" sur un canal (gauche ou droit), cochez la case "Activer le mixage mono" pour centrer le son.
 
bon enregistrement avec WASAPIRecording ! Si vous aimez cette application, allez dans "Menu > m'inviter à prendre un café" pour soutenir son développement.
 
Fichier microphone séparé : {mic_path}
Fichier système séparé : {sys_path} 
Fichier microphone séparé : {mic_path}
Fichier système séparé : {system_path} &Acceptation &Taux d'échantillonnage MP3 (kbps) : &Qualité (Hz) : &Annuler &fermer &Stop &Arrêter l'enregistrement &Format de sortie : activer le mixage mono &Information : &Démarrer l'enregistrement &Manuel d'utilisation : & Manuel d'utilisation &Menu &Non &Test audio &Dispositifs de rafraîchissement sélectionnez le fichier à lire : &System (loopback) : &Oui volume du microphone : volume du système : &invitez-moi à prendre un café si vous aimez mon travail Enregistrements libres Accepter À propos de &de... À propos de... Allemand Les deux Avis Annuler Annuler le test Capture Hotkey Home Arrêt des touches de raccourci de la capture Fermer Combinaison pour arrêter l'enregistrement : Pour démarrer l'enregistrement : Configuration de l'enregistrement Confirmer le changement de langue Confirmer la fermeture Arrêter Rencontres positives Dispositifs correctement mis à jour. Veille (utiliser {hk} pour démarrer) Veille. Attribuer des touches dans les options ou démarrer manuellement. Erreur Erreur de conversion du fichier : {error} Erreur lors de l'actualisation des périphériques : {error} Erreur de raccourci clavier Espagnol En attendant la combinaison... Veuillez patienter... Traitement Cette fenêtre vous permet d'effectuer un test d'enregistrement et de lecture.

1. Lorsqu'elle est ouverte, elle démarre l'enregistrement avec les mêmes paramètres que la fenêtre principale.
2. Pour mettre fin à l'enregistrement, appuyez sur "Stop". Le bouton devient alors "Play".
3. Si l'option "Enregistrer des fichiers séparés" a été activée dans la fenêtre principale, le menu déroulant s'affiche pour permettre de choisir entre la lecture du microphone uniquement, du système uniquement ou des deux (par défaut, "Les deux").
4. Le fait d'appuyer sur "Play" lance la lecture du fichier WAV de manière asynchrone. Le bouton devient "Stop" pendant la lecture. Lorsque la piste est terminée, le bouton revient à "Play".
5. Si vous appuyez sur "Close" pendant l'enregistrement, le système vous demandera si vous souhaitez annuler le test (les fichiers seront supprimés). Si vous avez déjà enregistré et/ou terminé, l'appareil se fermera simplement et effacera également les fichiers.

Vous ne pouvez pas fermer avec Alt+F4 ou avec le X dans la fenêtre, mais uniquement avec le bouton "Fermer".
 État Stéréo Français Général Enregistrement Enregistrement terminé. Fichier sauvegardé sous :
{file_path} Enregistrement... (Aucune touche de raccourci d'arrêt n'est affectée) Enregistrement... (Utilisez {hk} pour arrêter) Sauvegarde de fichiers séparés pour le microphone et le système Un enregistrement est en cours, voulez-vous l'arrêter et sortir ? Langue Informations Anglais Italien La combinaison doit comporter au moins deux modificateurs et une clé principale. La combinaison est utilisée par une autre application : L'enregistrement est toujours en cours, voulez-vous annuler le soundcheck ? Manuel de l'utilisateur Microphone&o : Minimiser au **barre d'état du système** Enregistrement et mode d'enregistrement : Singe Afficher la demande Le fichier à lire n'existe pas Vous ne pouvez pas attribuer la même combinaison au démarrage et à l'arrêt.
Veuillez en choisir une autre.
Les modifications reviendront à la valeur par défaut. Rien n'a encore été enregistré. Arrêtez d'abord l'enregistrement. Le répertoire d'enregistrement n'a pas pu être ouvert : {error} {error} {error} {error} {error} {error} {error} {error} {error} [0 Options Pour appliquer la nouvelle langue, vous devez redémarrer l'application.
voulez-vous continuer ? Veuillez patienter, la conversion au format final est en cours... Veuillez patienter, nous finalisons la conversion... Portugais Traitement Test audio Test du microphone Test du système Jouer Quitter Touche non valide détectée. Clavier Turc Enregistrement WASAPIR
Version {}
Créé par {} WASAPIR L'enregistrement est déjà en cours.

Il n'est pas possible d'avoir deux instances en même temps. invitez-moi à prendre un café si vous aimez mon travail 