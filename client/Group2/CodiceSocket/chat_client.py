import os
import sys
import socket
import threading
import utils

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))

def receive(sock):
    while 1:
        try:
            incoming = sock.recv(utils.BUFFER)
            if not incoming:
                print("\nConnessione al Server Chiusa")
                break
                
            message_data = utils.decode_json_msg(incoming)
            if message_data:
                who = message_data["from"]["name"]
                what = message_data["message"]
                print(f"\n{who}: {what}")
                print("> ", end='', flush=True)
                
        except (ConnectionResetError, OSError):
            print("\nErrore di connessione con il server")
            break
        except Exception as e:
            print(f"\nErrore: {str(e)}")
            break

def main():
    print("Chat di Gruppo")
    
    print("Inserisci i dati per connetterti al server:")
    user = input("Nome utente: ").strip()
    
    server = input("Indirizzo server (lascia vuoto per localhost): ").strip()
    server = server if server else "127.0.0.1"
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, utils.PORT))
        
        try:
            s.send(user.encode(utils.ENCODING))
        except Exception as e:
            print(f"Errore durante l'invio del nome utente: {e}")
            return
            
        print("\nConnesso! Inizia a chattare. Premi CTRL+C per uscire\n")
        
        receive_thread = threading.Thread(target=receive, args=(s,))
        receive_thread.daemon = True
        receive_thread.start()
        
        while True:
            try:
                msg = input("> ").strip()
                if not msg:
                    continue
                    
                message = utils.create_json_msg(
                    user,
                    s.getsockname()[0],
                    msg
                )
                s.send(message.encode(utils.ENCODING))
                
            except KeyboardInterrupt:
                print("\nChiusura della connessione...")
                break
                
    except ConnectionRefusedError:
        print("\nImpossibile connettersi al server.")
    except Exception as e:
        print(f"\nSi è verificato un errore: {str(e)}")
    finally:
        try:
            s.close()
        except:
            pass
        print("Disconnesso.")

if __name__ == "__main__":
    main()