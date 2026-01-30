import socket
import threading
import sys
import json
from datetime import datetime

# --- CONFIGURAZIONE COLORI E STILE ---
class Style:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def timestamp():
    return datetime.now().strftime("%H:%M")

def ricevi_messaggi(sock):
    while True:
        try:
            # Ricezione dati grezzi
            raw_data = sock.recv(2048).decode()
            if not raw_data:
                break
            
            # Tentativo di parsing JSON
            try:
                data = json.loads(raw_data)
                
                # Estrazione dati sicura
                mittente_info = data.get("from", {})
                if isinstance(mittente_info, dict):
                    mittente = mittente_info.get("name", "Sconosciuto")
                else:
                    mittente = str(mittente_info) # Fallback 
                
                messaggio = data.get("msg", "")
                destinatario = data.get("to", "")

                # --- FORMATTAZIONE ESTETICA ---
                
          
                sys.stdout.write("\r" + " " * 50 + "\r")

              
                if mittente == "SERVER":
                   
                    print(f"{Style.YELLOW}  [SERVER] {messaggio}{Style.RESET}")
                
                elif mittente == name:
                   
                    print(f"{Style.GREEN}✓  [Tu]: {messaggio}{Style.RESET}")
                    
                else:
                  
                    if destinatario == "Everyone" or destinatario == "/shout":

                        print(f"{Style.CYAN} [{timestamp()}] {Style.BOLD}{mittente}{Style.RESET}: {messaggio}")
                    else:
                
                        print(f"{Style.BLUE} [{timestamp()}] {Style.BOLD}{mittente}{Style.RESET} (privato): {messaggio}")

               
                sys.stdout.write(f"{Style.GREEN}[Tu] > {Style.RESET}")
                sys.stdout.flush()

            except json.JSONDecodeError:
               
                print(f"\r{Style.RED}  RAW: {raw_data}{Style.RESET}")
                sys.stdout.write(f"{Style.GREEN}[Tu] > {Style.RESET}")
                sys.stdout.flush()

        except Exception as e:
            print(f"\n{Style.RED} Connessione persa ({e}).{Style.RESET}")
            break

# --- PARAMETRI DI CONNESSIONE ---
HOST = '127.0.0.1'
PORT = 65432

# TITOLO DI BENVENUTO
name = input("Inserisci il tuo nome utente: ").strip()
ip = get_local_ip()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        print(f" Connessione al server {HOST}:{PORT}...")
        s.connect((HOST, PORT))
        

        s.sendall(name.encode()) 
        print(f"{Style.GREEN} Connesso! Sei online come '{name}'.{Style.RESET}")
        print(f"{Style.YELLOW} Suggerimento: Scrivi /help per i comandi.{Style.RESET}\n")

    except ConnectionRefusedError:
        print(f"{Style.RED} Errore: Il server sembra spento.{Style.RESET}")
        sys.exit()


    t = threading.Thread(target=ricevi_messaggi, args=(s,), daemon=True)
    t.start()

    sys.stdout.write(f"{Style.GREEN}[Tu] > {Style.RESET}")
    sys.stdout.flush()

    while True:
        try:
            # Input utente
            testo = input()
            
           
            sys.stdout.write("\033[F\033[K") 
            
           
            print(f"{Style.GREEN}✓  [Tu]: {testo}{Style.RESET}")
            
            sys.stdout.write(f"{Style.GREEN}[Tu] > {Style.RESET}")
            sys.stdout.flush()

            if testo.lower() == "exit":
                break
            
            # --- INTELLIGENZA COMANDI ---
            # Se inizia con '/', usiamo quello come "to". 
            # Esempio: "/help" diventa to="/help". 
            # Altrimenti default è "/shout".
            
            if testo.startswith('/'):
                destinazione = testo.split(" ")[0]
                contenuto = testo 
            else:
                destinazione = "/shout"
                contenuto = testo

            payload = {
                "from": {"name": name, "ip": ip},
                "to": destinazione,
                "msg": contenuto
            }
            
            s.sendall(json.dumps(payload).encode())

        except (ConnectionAbortedError, ConnectionResetError):
            print(f"\n{Style.RED} Disconnesso dal server.{Style.RESET}")
            break
        except KeyboardInterrupt:
            print("\n")
            break

    s.close()
    print(f"{Style.HEADER} Alla prossima!{Style.RESET}")

