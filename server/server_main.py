import sys
import os

# sys directory to import utils
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

import socket as sck
import threading as thr
import utils
import chat_server as cht 

HOST = "0.0.0.0"

if __name__ == '__main__':
    print(f"--- Server started on {utils.get_local_ip()}:{utils.PORT} ---")
    with sck.socket(sck.AF_INET, sck.SOCK_STREAM) as s:
        s.bind((HOST, utils.PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            thr.Thread(target=cht.handle_client, args=(conn, addr), daemon=True).start()