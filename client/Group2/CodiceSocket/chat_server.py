import threading as thr
import socket
import utils

clients = {}
lock = thr.Lock()

def broadcast(data, sender_conn=None):
    with lock:
        connections = list(clients.values())
    
    for conn in connections:
        try:
            if conn != sender_conn:
                conn.send(data)
        except (ConnectionError, OSError) as e:
            print(f"Errore nell'invio del messaggio: {e}")

def handle_client(conn, addr):
    name = None
    
    try:
        name_data = conn.recv(utils.BUFFER)
        if not name_data:
            return 
            
        name = name_data.decode(utils.ENCODING).strip()
        
        with lock:
            if name in clients:
                conn.send("ERRORE: Nome utente già in uso".encode(utils.ENCODING))
                conn.close()
                return
            clients[name] = conn
        
        print(f"{name} si è unito da {addr[0]}")
        
        welcome_msg = utils.create_json_msg(
            "SERVER",
            "0.0.0.0",
            f"👋 {name} si è unito alla chat!"
        )
        broadcast(welcome_msg.encode(utils.ENCODING), conn)
        
        while 1:
            try:
                data = conn.recv(utils.BUFFER)
                if not data:
                    break
                
                print(f"{name}: {len(data)} bytes")
                
                broadcast(data, conn)
                
            except (ConnectionResetError, socket.error) as e:
                print(f"Connessione con {name} interrotta: {e}")
                break
                
    except Exception as e:
        print(f"Errore in handle_client: {str(e)}")
        
    finally:
        if name:
            with lock:
                if name in clients:
                    del clients[name]
            
            leave_msg = utils.create_json_msg(
                "SERVER",
                "0.0.0.0",
                f"👋 {name} ha lasciato la chat"
            )
            broadcast(leave_msg.encode(utils.ENCODING))
            
            print(f"{name} si è disconnesso")
        
        try:
            conn.close()
        except:
            pass
