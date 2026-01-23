import socket
import threading
import sys

# --- MODIFICA L'IP QUI ---
HOST = '192.168.13.62' 
PORT = 65432
# -------------------------

def ascolta(s):
    """Thread che ascolta i messaggi dal server"""
    while True:
        try:
            data = s.recv(1024)
            if not data:
                print("\n[DISCONNESSO DAL SERVER]")
                s.close()
                sys.exit() # Chiude tutto il programma
            
            # \r cancella la riga corrente (il prompt 'Tu: ') per stampare pulito
            print(f"\r{data.decode()}\nTu: ", end="")
        except:
            break

def main():
    nickname = input("Scegli il tuo Nickname: ")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except:
        print("Errore: Impossibile connettersi al Server.")
        return

    # Handshake
    try:
        msg_iniziale = client.recv(1024).decode()
        if msg_iniziale == "NICK":
            client.sendall(nickname.encode())
    except:
        print("Errore durante l'autenticazione.")
        return
    
    # Avvio ascolto
    thread = threading.Thread(target=ascolta, args=(client,), daemon=True)
    thread.start()
    
    print("\n--- BENVENUTO NEL LABORATORIO 39 ---")
    print("Comandi:")
    print("  Scrivi testo  -> Messaggio pubblico")
    print("  /list         -> Vedi chi è online")
    print("  /join stanza  -> Cambia stanza (es. /join gaming)")
    print("  @Nome testo   -> Messaggio privato (es. @Luca ciao)")
    print("  /kick Nome    -> Espelli utente")
    print("  exit          -> Esci")
    print("------------------------------------\n")

    while True:
        try:
            msg = input("Tu: ")
            if msg.lower() == 'exit':
                break
            client.sendall(msg.encode())
        except:
            break
    
    client.close()
    print("Chiusura client...")

if __name__ == "__main__":
    main()
