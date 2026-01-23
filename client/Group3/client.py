import sys
import os

# sys import to find utils
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(root_dir)

import socket as sck
import threading as thr
import utils 

def receive_messages(sock):
    """Listen for incoming messages."""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[!] Disconnected from server.")
                break
            
            msg = utils.decode_json_msg(data)
            if msg:
                # Pretty print msg
                sender = msg['from']['name']
                text = msg['msg']
                print(f"\n >>> {sender}: {text}")
                print("To: ", end="", flush=True)
        except Exception as e:
            print(f"\n[!] Receive Error: {e}")
            break
    sys.exit()

def start_client():
    my_ip = utils.get_local_ip()
    
    # Connection
    server_host = input("Insert Server IP (press send for localhost): ").strip() or "127.0.0.1"
    my_name = input("Your Username: ").strip()

    sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    
    try:
        sock.connect((server_host, utils.PORT))
    except ConnectionRefusedError:
        print("[!] Impossible to connect to server. Check connectivity.")
        return

    # 1. Send name for registration
    sock.send(my_name.encode(utils.ENCODING))

    # Start Receiver Thread
    thr.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    print(f"--- Connected as {my_name} ({my_ip}) ---")
    print("Message format -> Receiver, send, message.")

    # Sending Loop
    try:
        while True:
            to_user = input("To: ")
            text = input("Msg: ")

            # Utility function to create the json
            json_packet = utils.create_json_msg(my_name, my_ip, to_user, text)
            
            sock.send(json_packet.encode(utils.ENCODING))
            
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        sock.close()

if __name__ == "__main__":
    start_client()