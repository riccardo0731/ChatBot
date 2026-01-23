import socket
import threading
import sys
import os

# --- CONFIGURAZIONE LABORATORIO 39 ---
HOST = '192.168.13.62'  # <--- IP DEL SERVER HARDCODED
PORT = 65432
# -------------------------------------

def ascolta_server(s):
    """Ascolta i messaggi in arrivo senza bloccare la tastiera"""
    while True:
        try:
            data = s.recv(1024)
            if not data:
                print("\n[DISCONNESSO DAL SERVER]")
                s.close()
                os._exit(0) # Chiude brutalmente il programma
            
            # \r cancella la riga corrente per stampare pulito
            print(f"\r{data.decode()}\nTu: ", end="")
        except:
            break

def main():
    # Pulizia iniziale schermo
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"--- CLIENT LAB 39 ---")
    print(f"Tentativo di connessione a {HOST}...")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except Exception as e:
        print(f"Errore: Server non trovato ({e})")
        input("Premi Invio per uscire...")
        return

    # Handshake Nickname
    try:
        msg = client.recv(1024).decode()
        if msg == "NICK":
            nick = input("Scegli il tuo Nickname: ")
            client.sendall(nick.encode())
    except:
        print("Errore connessione.")
        return

    # Avvio thread ascolto
    thread = threading.Thread(target=ascolta_server, args=(client,), daemon=True)
    thread.start()

    # Istruzioni
    print("\n--- COMANDI ---")
    print(" /list           -> Vedi chi è online")
    print(" /join stanza    -> Entra in una stanza (es. /join gaming)")
    print(" @Nome msg       -> Messaggio privato")
    print(" /shout msg      -> Annuncio a TUTTI (Globale)")
    print(" /roll           -> Tira un dado")
    print(" /afk            -> Segnala che sei assente")
    print(" /cls            -> Pulisci il tuo schermo")
    print(" /kick Nome      -> (Admin) Espelli utente")
    print(" /ban Nome       -> (Admin) Banna IP utente")
    print(" exit            -> Chiudi")
    print("---------------\n")

    # Ciclo input tastiera
    while True:
        try:
            msg = input("Tu: ")
            
            # Gestione pulizia locale
            if msg.lower() == '/cls':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Tu: ", end="")
                continue

            if msg.lower() == 'exit':
                break
                
            client.sendall(msg.encode())
            
        except KeyboardInterrupt:
            break
        except:
            break
    
    client.close()
    print("Chiusura...")

if __name__ == "__main__":
    main()
