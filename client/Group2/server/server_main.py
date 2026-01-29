import sys
import os

current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.abspath(os.path.join(current, ".."))
sys.path.append(parent)

import socket
import threading
import utils
import chat_server

HOST = "0.0.0.0"

if __name__ == "__main__":
    print(f"SERVER CHAT DI GRUPPO → {utils.get_local_ip()}:{utils.PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, utils.PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            threading.Thread(
                target=chat_server.handle_client,
                args=(conn, addr),
                daemon=True
            ).start()
