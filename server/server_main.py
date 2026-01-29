import sys
import os

# 1. Retrieve the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))
# 2. Navigate one level up to locate the project root directory
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 3. Append the root directory to the system path to resolve shared modules
sys.path.append(parent_dir)

import socket as sck
import threading as thr
import utils
import server.server_lib as cht 

HOST = "0.0.0.0"

if __name__ == '__main__':
    print(f"--- Server started on {utils.get_local_ip()}:{utils.PORT} ---")
    with sck.socket(sck.AF_INET, sck.SOCK_STREAM) as s:
        s.bind((HOST, utils.PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            thr.Thread(target=cht.handle_client, args=(conn, addr), daemon=True).start()