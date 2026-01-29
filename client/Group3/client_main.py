import sys
import os

# 1. Retrieve the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))
# 2. Navigate two levels up to locate the project root directory
root_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
# 3. Append the root directory to the system path to resolve shared modules
sys.path.append(root_dir)

import socket as sck
import threading as thr
import utils 
import client_lib 

def start_client():
    my_ip = utils.get_local_ip()
    
    # Initial configuration and user setup
    print(f"--- Client Group 3 ---")
    server_host = input("Insert Server IP (press enter for localhost): ").strip() or "127.0.0.1"
    my_name = input("Your Username: ").strip()

    sock = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    
    try:
        # Establish connection to the server
        sock.connect((server_host, utils.PORT))
    except ConnectionRefusedError:
        print("[!] Impossible to connect to server. Check connectivity.")
        return

    # 1. Send username for registration (Handshake Protocol)
    sock.send(my_name.encode(utils.ENCODING))

    # 2. Start the receiving thread using the library function
    # Note: Referencing client_lib.receive_messages
    receiver_thread = thr.Thread(
        target=client_lib.receive_messages, 
        args=(sock,), 
        daemon=True
    )
    receiver_thread.start()

    print(f"--- Connected as {my_name} ({my_ip}) ---")
    print("Message format -> Receiver, enter, message.")

    # Get commands list from server to show at the start to the user
    to_user = "/help"
    text = "x"
    json_packet = utils.create_json_msg(my_name, my_ip, to_user, text)
    sock.send(json_packet.encode(utils.ENCODING))


    # 3. Sending Loop (Executes in the main thread)
    try:
        while True:
            to_user = input("To: ")
            text = input("Msg: ")

            # Utilize the utility function to construct a valid JSON packet
            json_packet = utils.create_json_msg(my_name, my_ip, to_user, text)
            
            sock.send(json_packet.encode(utils.ENCODING))
            
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Ensure the socket is properly closed upon termination
        sock.close()


if __name__ == "__main__":
    start_client()