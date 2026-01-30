import sys
import os
import signal
import socket
import threading

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import utils
import chat_server

HOST = "0.0.0.0"
server_socket = None

def signal_handler(sig, frame):
    print("\nRicevuto segnale di chiusura. Disconnessione in corso...")
    if server_socket:
        try:
            server_socket.close()
        except:
            pass
    print("Server spento.")
    sys.exit(0)

def main():
    global server_socket
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((HOST, utils.PORT))
        except OSError as e:
            print(f"Errore: Impossibile avviare il server sulla porta {utils.PORT}")
            print(f"Dettagli: {e}")
            return 1
        
        server_socket.listen(5)  
        
        local_ip = utils.get_local_ip()
        
        print("=" * 60)
        print(f"Server Chat Avviato")
        print(f"Indirizzo: {local_ip}")
        print(f"Porta: {utils.PORT}")
        print("=" * 60)
        print("In attesa di connessioni... (premi Ctrl+C per uscire)")
        
        while 1:
            try:
                conn, addr = server_socket.accept()
                
                client_thread = threading.Thread(
                    target=chat_server.handle_client,
                    args=(conn, addr),
                    daemon=True  
                )
                
                client_thread.start()
                
                print(f"Connessione accettata da {addr[0]}:{addr[1]}")
                
            except KeyboardInterrupt:
                print("\nChiusura del server in corso...")
                break
            except Exception as e:
                print(f"Errore nella connessione: {e}")
                continue
                
    except Exception as e:
        print(f"Errore: {e}")
        return 1
    finally:
        if server_socket:
            try:
                server_socket.close()
            except:
                pass
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
