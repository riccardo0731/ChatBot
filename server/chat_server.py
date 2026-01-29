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
        
        print(f"[NUOVA CONNESSIONE] {name} connesso da {addr[0]}")
        
        # Message listening loop
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            # Decode using the standard
            msg_obj = utils.decode_json_msg(data)
            
            if msg_obj:
                # Server side logging
                print(f"[MSG] Da: {msg_obj['from']['name']} -> A: {msg_obj['to']}")
                
                dest_name = msg_obj['to']
                
                # Message routing
                with lock:
                    # Check for /standard endpoint
                    if dest_name == '/standard':
                        conn.send(utils.create_json_msg("SERVER", "0.0.0.0", name, utils.get_standard_json).encode(utils.ENCODING))
                    elif dest_name in clients:
                        dest_conn = clients[dest_name]
                        # Send JSON message
                        dest_conn.send(data)
                    else:
                        # Tell the sender that the user doesnt exist
                        error_msg = utils.create_json_msg("SERVER", "0.0.0.0", name, f"User {dest_name} not found.")
                        conn.send(error_msg.encode(utils.ENCODING))

    except Exception as e:
        print(f"[ERRORE] {e}")
    finally:
        # Clean when the client disconnects
        if name:
            print(f"[DISCONNESSIONE] {name} uscito.")
            with lock:
                if name in clients:
                    del clients[name]
        conn.close()