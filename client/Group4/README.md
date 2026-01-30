# Authors

- Navoni
- Dilecce
- Khabir
- Solitro
- Brambilla


TCP Chat Client
Client Python per chat room TCP basata su socket, multithreading e messaggistica JSON. Include interfaccia a riga di comando colorata.

Requisiti
Python 3.x

Librerie standard (nessuna installazione pip necessaria): socket, threading, sys, json, datetime.

Configurazione
Di default il client si connette a 127.0.0.1:65432. Per modificare l'indirizzo del server, editare le variabili nel file sorgente:

Python
HOST = '127.0.0.1'
PORT = 65432
Avvio
Eseguire il script da terminale:

Bash
python client.py
Utilizzo
All'avvio, inserire il nome utente desiderato.

Digitare un messaggio e premere Invio per scrivere nella chat pubblica.

Digitare exit o premere Ctrl+C per chiudere la connessione.

Funzionalità e Comandi
Il client gestisce automaticamente l'input:

Messaggi Pubblici: Qualsiasi testo digitato viene inviato a tutti gli utenti connessi (canale /shout).

Comandi Server: Le stringhe che iniziano con / (es. /list, /help) vengono inviate come comandi diretti al server.

Interfaccia: Pulizia automatica della riga di input e feedback visivo colorato per mittente, server e messaggi privati.
