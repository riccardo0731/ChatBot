import socket
import threading
import sys



def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Non serve che l'IP sia raggiungibile, serve solo a "risvegliare" l'interfaccia
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

HOST = '127.0.0.1'
PORT = 65432
name = "ricky"
ip = get_local_ip()

def ricevi_messaggi(sock):
    while True:
        try:
            messaggio = sock.recv(1024).decode()
            if not messaggio:
                break
            print(messaggio)
        except:
            print("\033[91mConnessione persa con il server.\033[0m")
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    s.connect((HOST, PORT))
    
    threading.Thread(target=ricevi_messaggi, args=(s,), daemon=True).start()

    while True:
        try:
            input = input()
            messaggio =  f"""
{{
  "from": {{ "name": "{name}", "ip": "{ip}" }},
  "msg": "{input}"
}}
"""
            if messaggio.lower() == "exit":
                print("\033[93mDisconnessione...\033[0m")
                s.close()
                sys.exit()
            s.sendall(messaggio.encode())
        except KeyboardInterrupt:
            print("\n\033[93mChiusura forzata...\033[0m")
            s.close()

            sys.exit()
