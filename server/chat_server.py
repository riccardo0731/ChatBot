import json
import socket as sck
import threading as thr

### CHAT SERVER FUNCTIONS ###

msg_standard = {
                "from": {
                	   "name": "YourName",
                         "ip":   "YourIp",
                	},

                "to":   "IpToSendMsgTo",
                "msg":  "YourMsg"
            }

# Standard Port
PORT = 65432

clients = {}
lock = thr.Lock()



def client_handle(conn, addr):

    try:
        name = conn.recv(1024).decode()

        with lock:
            clients[name] = conn
        
        print(f"{name} connected from {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break
        
            msg = json.loads(data.decode())
            dest = msg['to']

            with lock:
                if dest in clients:
                    clients[dest].send(json.dumps(msg).encode())

    finally:
        with lock:
            clients.pop(name, None)
        conn.close()
        print(f"{name} disconnected")



def check_standard_endpoint(msg: dict):
    if(msg['msg'] == '/standard'):
        return True
    else:
        return False



