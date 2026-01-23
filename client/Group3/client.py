# Import socket library
import socket as sck
import json 
import threading as thr
 
def receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            msg = json.loads(data.decode())
            print(f"\n{msg['from']}: {msg['msg']}")
        except:
            break

def send(sock, name):
    while True:
        to = input("To: ")
        text = input("Msg: ")

        msg = {
            "from": name,
            "to": to,
            "msg": text
        }
        sock.send(json.dumps(msg).encode())


# Server connection settings
HOST = "127.0.0.1"
PORT = 65432

if __name__ == "__main__":

    name = input("Username: ")

    sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.send(name.encode())

    thr.Thread(target=receive, args=(sock,), daemon=True).start()
    send(sock, name)