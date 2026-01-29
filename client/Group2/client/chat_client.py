import sys
import os

current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.abspath(os.path.join(current, ".."))
sys.path.append(parent)

import socket
import threading
import utils

def receive(sock):
    while True:
        try:
            data = sock.recv(utils.BUFFER)
            if not data:
                print("\n[SERVER DISCONNESSO]")
                break

            msg = utils.decode_json_msg(data)
            if msg:
                sender = msg["from"]["name"]
                text = msg["message"]
                print(f"\n{sender}: {text}")
                print("> ", end="", flush=True)
        except:
            break

def main():
    print("=== CHAT DI GRUPPO ===")

    username = input("Username: ").strip()
    server_ip = input("IP server (invio = localhost): ").strip()
    if not server_ip:
        server_ip = "127.0.0.1"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_ip, utils.PORT))

            # handshake
            sock.send(username.encode(utils.ENCODING))

            print("\nConnesso! Scrivi il messaggio e premi INVIO.\n")

            threading.Thread(
                target=receive,
                args=(sock,),
                daemon=True
            ).start()

            while True:
                text = input("> ").strip()
                if not text:
                    continue

                json_msg = utils.create_json_msg(
                    username,
                    sock.getsockname()[0],
                    text
                )

                sock.send(json_msg.encode(utils.ENCODING))

    except KeyboardInterrupt:
        print("\nUscita dalla chat.")
    except Exception as e:
        print("Errore:", e)

if __name__ == "__main__":
    main()
