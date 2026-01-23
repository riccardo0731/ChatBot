### Imports ###
# Import Socket for communication
import socket as sck
# Import threading for multiple client handling
import threading as thr
# Import json for data handling
import json
# Import server functions
import chat_server as cht

# Server Socket Settings

HOST = "127.0.0.1"
PORT = 65432

# Socket Opening

if __name__ == '__main__':

    with sck.socket(family = sck.AF_INET, type= sck.SOCK_STREAM) as s:

        s.bind( (HOST, PORT) )

        s.listen()

        print(f"Server listening on {HOST}:{PORT}...")

        while True:

            conn, addr = s.accept()

            t = thr.Thread(target=cht.client_handle, args=(conn, addr))
            t.start()