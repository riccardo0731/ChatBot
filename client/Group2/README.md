# Chat di gruppo TCP in Python

Questa è una semplice applicazione di chat di gruppo client–server sviluppata in Python utilizzando socket TCP, threading e messaggi in formato JSON.

Il progetto permette a più client di collegarsi a un server centrale e scambiarsi messaggi in tempo reale tramite terminale.

---

## Descrizione generale

Il server accetta più connessioni contemporaneamente e gestisce ogni client in un thread separato.  
I messaggi vengono inviati in broadcast a tutti gli utenti connessi, escluso il mittente.

Quando un utente entra o lascia la chat, il server invia una notifica a tutti gli altri client.

---

## Struttura del progetto

chat/  
│  
├── server/  
│ ├── server.py # Avvio del server  
│ └── chat_server.py # Gestione dei client e dei messaggi  
│  
├── client/  
│ └── client.py # Client della chat  
│  
├── utils.py # Funzioni e costanti condivise  
│  
└── README.md  


---

## Requisiti

- Python 3.8 o superiore
- Nessuna dipendenza esterna (solo librerie standard)

---

## Avvio del server

Dal terminale, posizionandosi nella cartella del progetto:

```bash
python server/server.py
Il server viene avviato sulla porta 5000 ed è in ascolto su tutte le interfacce di rete.

Avvio del client
In un altro terminale (anche su un computer diverso):

python client/client.py
All’avvio verranno richiesti:

uno username

l’indirizzo IP del server (premendo INVIO viene usato localhost)

Dopo la connessione è possibile iniziare a scrivere messaggi.

Formato dei messaggi
I messaggi scambiati tra client e server sono codificati in formato JSON.
Ogni messaggio contiene il nome del mittente, il suo indirizzo IP e il testo del messaggio.

Esempio:

{
  "from": {
    "name": "Mario",
    "ip": "192.168.1.20"
  },
  "message": "Ciao a tutti"
}
Gestione dei client
Ogni client è gestito in un thread dedicato

L’accesso alla lista dei client è protetto da un lock

I messaggi vengono inoltrati a tutti i client connessi

Chiusura dell’applicazione
Il client può essere chiuso con Ctrl + C

Il server rileva la disconnessione e notifica gli altri utenti

Possibili estensioni
Il progetto può essere esteso, ad esempio con:

comandi testuali (/quit, /list)

autenticazione degli utenti

salvataggio dello storico dei messaggi

cifratura della comunicazione

interfaccia grafica  

Licenza
Progetto a scopo didattico. Libero per studio, modifica e utilizzo.

Autori
Biestro Edoardo
Medri Riccardo
