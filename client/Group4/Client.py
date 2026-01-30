import socket
import threading
import sys
import json
from datetime import datetime

# Colori e stile
Y = '\033[93m' # Server
B = '\033[94m' # Privato
C = '\033[96m' # Public
G = '\033[92m' # Success
R = '\033[91m' # Error
RESET = '\033[0m'

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    s.close()
    return ip

def ricevi_messaggi(sock):
    while True:
        try:
            raw = sock.recv(2048).decode()
            if not raw: break
            
            data = json.loads(raw)
            frm = data.get("from", {}).get("name", "?")
            msg = data.get("msg", "")
            to = data.get("to", "")
            
            # Pulizia riga input
            sys.stdout.write("\r" + " " * 60 + "\r")

            timestamp = datetime.now().strftime("%H:%M")

            if frm == "SERVER":
                print(f"{Y}🛡️  [SERVER]: {msg}{RESET}")
            elif to == "/shout" or to == "Everyone":
                print(f"{C}📢 [{timestamp}] {frm}: {msg}{RESET}")
            else:
                # Messaggio privato
                print(f"{B}🔒 [{timestamp}] {frm} (privato): {msg}{RESET}")

            # Ripristino prompt
            sys.stdout.write(f"{G}[Tu] > {RESET}")
            sys.stdout.flush()

        except (json.JSONDecodeError, OSError):
            continue

HOST = '127.0.0.1'
PORT = 65432

print(f"{C}--- CHAT CLIENT ---{RESET}")
name = input("Username: ").strip()
ip = get_local_ip()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        s.sendall(name.encode()) # Handshake semplice
    except:
        print(f"{R}Server offline.{RESET}")
        sys.exit()

    threading.Thread(target=ricevi_messaggi, args=(s,), daemon=True).start()
    
    print(f"{G}Connesso come {name}.{RESET}")
    print("Usa '@Nome Messaggio' per privati, '/list' per utenti, testo normale per tutti.\n")
    
    sys.stdout.write(f"{G}[Tu] > {RESET}")
    sys.stdout.flush()

    while True:
        try:
            inp = input()
            
            # Cancellazione estetica input raw e feedback
            sys.stdout.write("\033[F\033[K")
            print(f"{G}✓ [Tu]: {inp}{RESET}")
            sys.stdout.write(f"{G}[Tu] > {RESET}")
            sys.stdout.flush()

            if inp.lower() == "exit": break

            # LOGICA DI INVIO
            payload = {"from": {"name": name, "ip": ip}, "msg": inp}

            if inp.startswith("@"):
                # Messaggio Privato: @Nome Messaggio
                try:
                    target, content = inp.split(" ", 1)
                    payload["to"] = target[1:] # Rimuove la @
                    payload["msg"] = content
                except ValueError:
                    print(f"{R}Formato errato. Usa: @Nome Messaggio{RESET}")
                    continue
            
            elif inp.startswith("/"):
                # Comando Server (es. /list, /time)
                payload["to"] = inp.split(" ")[0]
            
            else:
                # Messaggio a tutti
                payload["to"] = "/shout"

            s.sendall(json.dumps(payload).encode())

        except KeyboardInterrupt:
            break
        except Exception:
            print(f"\n{R}Errore connessione.{RESET}")
            break
