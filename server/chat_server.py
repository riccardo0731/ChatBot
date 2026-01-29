import socket as sck
import threading as thr
import utils

# Data structure for connected clients: { "Username": socket_object }
clients = {}
lock = thr.Lock()

def broadcast(msg_dict, sender_socket):
    """Optional: Send to everyone"""
    pass 

def handle_client(conn, addr):
    """Handle single client connection."""
    name = None
    try:
        # 1. First Handshake: receive username
        name = conn.recv(1024).decode(utils.ENCODING).strip()
        
        with lock:
            clients[name] = conn
        
        print(f"[NEW CONNECTION] {name} connected from {addr[0]}")
        
        # Message listening loop
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            # Decode using the standard
            msg_obj = utils.decode_json_msg(data)
            
            if msg_obj:
                # Server side logging
                print(f"[MSG] From: {msg_obj['from']['name']} -> To: {msg_obj['to']}")
                
                dest_name = msg_obj['to']
                
                # Message routing
                with lock:
                    if dest_name in clients:
                        dest_conn = clients[dest_name]
                        # Send JSON message
                        dest_conn.send(data)
                    else:
                        # Tell the sender that the user doesnt exist
                        error_msg = utils.create_json_msg("SERVER", "0.0.0.0", name, f"User {dest_name} not found.")
                        conn.send(error_msg.encode(utils.ENCODING))

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        # Clean when the client disconnects
        if name:
            print(f"[DISCONNECTING] {name} exited.")
            with lock:
                if name in clients:
                    del clients[name]
        conn.close()