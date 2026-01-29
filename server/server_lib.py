import sys
import os

# 1. Retrieve the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))
# 2. Navigate two levels up to locate the project root directory
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 3. Append the root directory to the system path to resolve shared modules
sys.path.append(root_dir)

import socket as sck
import threading as thr
import utils
import datetime

# Data structure for connected clients: { "Username": socket_object }
clients = {}
lock = thr.Lock()

def send_server_response(conn, target_user, text):
    """
    Name: send_server_response

    Parameters: 
        conn        | socket object | socket of the sender
        target_user | string        | name of the user who will receive the message
        text        | string        | message content

    Exceptions: OSError | If the socket is closed

    Description: Send a response back when an endpoint is called, signing as the server.

    """
    try:
        json_resp = utils.create_json_msg(
            sender_name = "SERVER",
            sender_ip = "0.0.0.0",
            target = target_user,
            text = text
        )
        conn.send(json_resp.encode(utils.ENCODING))
    except OSError:
        pass  # Socket may be closed

### Endpoint Management ###

def endpoint_standard(conn, requester_name, text):
    """
    Name: endpoint_standard

    Parameters: 
        conn           | socket object | socket of the sender
        requester_name | string        | name of the user who asked for the service
        text           | string        | message content

    Exceptions: None

    Description: Reply with the JSON format used during the sessions.

    """
    standard_json = utils.get_standard_json()
    send_server_response(conn, requester_name, f"JSON STD: \n {standard_json}")

def endpoint_list(conn, requester_name, text):
    """
    Name: endpoint_list

    Parameters: 
        conn           | socket object | socket of the sender
        requester_name | string        | name of the user who asked for the service
        text           | string        | message content

    Exceptions: None

    Description: Reply with the list of all active users (except the requester).

    """
    with lock:
        users = [name for name in clients if name != requester_name] # everyone but the requester
    if users:
        msg = f"Online users ({len(users)}): " + ", ".join(users)
    else:
        msg = "Your are the only active user!"
    
    send_server_response(conn, requester_name, msg)

def endpoint_time(conn, requester_name, text):
    """
    Name: endpoint_time

    Parameters: 
        conn           | socket object | socket of the sender
        requester_name | string        | name of the user who asked for the service
        text           | string        | message content

    Exceptions: None

    Description: Reply with the current time of the server.

    """
    now = datetime.datetime.now().strftime("%H:%M:%S")
    send_server_response(conn, requester_name, f"Server time: {now}")

def endpoints_help(conn, requester_name, text):
    """
    Name: endpoint_help

    Parameters: 
        conn           | socket object | socket of the sender
        requester_name | string        | name of the user who asked for the service
        text           | string        | message content

    Exceptions: None

    Description: Reply with the list of all available endpoint commands.

    """
    commands = ", ".join(COMMANDS.keys())
    send_server_response(conn, requester_name, f"Available commands: \n {commands} \n Note: Write them when asking 'to:' to receive the correct response!")

def endpoint_shout(conn, requester_name, text):
    """
    Name: endpoint_shout

    Parameters: 
        conn           | socket object | socket of the sender
        requester_name | string        | name of the user who asked for the service
        text           | string        | message content

    Exceptions: 
        Any     | if the sender ip can't be resolved
        OSError | trying to send message to broken sockets

    Description: Send a message to all active users except the sender.

    """
    # Get sender ip
    try:
        sender_ip = clients[requester_name].getpeername()[0]
    except:
        sender_ip = 'Unknown'
    
    # Create JSON package
    json_message = utils.create_json_msg(
        sender_name = requester_name,
        sender_ip = sender_ip,
        target = "Everyone",
        text = text
    )

    encoded_message = json_message.encode(utils.ENCODING)

    # Send to everyone
    with lock:
        users = [sock for name, sock in clients.items() if name != requester_name]
        count = 0
        for sock in users:
            try:
                sock.send(encoded_message)
                count += 1
            except OSError:
                pass # Ignore broken sockets
    
    # Confirm to sender
    send_server_response(conn, requester_name, f"Message sent to {count} users")



# Commands Dispatcher for endpoints
COMMANDS = {
    '/standard':  endpoint_standard,
    '/list':      endpoint_list,
    '/time':      endpoint_time,
    '/help':      endpoints_help,
    '/shout':     endpoint_shout
}

def handle_client(conn, addr):
    """
    Name: handle_client

    Parameters: 
        conn | socket object | socket of the client
        addr | string        | address of the client 

    Exceptions: 
        ConnectionResetError | Disconnection of the client
        Any                  | Error logged in the server terminal

    Description: Handle clients by receiving their messages and dispatching them between commands or routing to the correct receiver.

    """
    name = None
    try:
        # 1. Handshake: Receive name
        raw_data = conn.recv(1024).decode(utils.ENCODING)
        
        # If help message and name are sent together because of the TCP Coalescing, then we just take the name
        if '{' in raw_data:
            raw_name = raw_data.split('{')[0]
        else:
            raw_name = raw_data
            
        raw_name = raw_name.strip()
        
        # Check uniqueness
        with lock:
            if raw_name in clients:
                # If name is already existing, send error and disconnect
                print(f"[REJECTED] {raw_name} tried access from {addr[0]} (Duplicate name)")
                error_msg = "⛔ Error: Username already in! Try with another name."
                send_server_response(conn, "Guest", error_msg)
                conn.close()
                return # Exits from function, terminating the thread
            
            # If its unique, we add it
            clients[raw_name] = conn
            name = raw_name # Assign to local variable for the final step

        print(f"[NEW CONNECTION] {name} connected from {addr[0]}")

        # 2. Welcome message to new user
        with lock:
            other_users = [u for u in clients if u != name]
        
        welcome_text = f"Welcome {name}! Connection established.\nSend message to /help for a list of available commands!"
        if other_users:
            welcome_text += f"\nOnline users: {', '.join(other_users)}"
        else:
            welcome_text += "\nYou are the first connected user."
            
        send_server_response(conn, name, welcome_text)

        # Message listening loop
        while True:
            data = conn.recv(1024)
            if not data: break
            
            msg_obj = utils.decode_json_msg(data)
            if not msg_obj: continue
            
            # Server Log
            print(f"[MSG] {name} -> {msg_obj['to']}")

            dest_name = msg_obj['to']
            msg_content = msg_obj['msg']
            
            # Endpoint commands handling
            if dest_name in COMMANDS:
                COMMANDS[dest_name](conn, name, msg_content)
                continue

            # Message routing
            with lock:
                if dest_name in clients:
                    clients[dest_name].send(data)
                else:
                    send_server_response(conn, name, f"❌ Errore: Utente '{dest_name}' non trovato.")

    except ConnectionResetError:
        pass # In case of disconnection
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        # Cleanup on disconnection
        if name:
            print(f"[DISCONNECTING] {name} exited.")
            with lock:
                # Security check in case of race condition
                if name in clients and clients[name] == conn:
                    del clients[name]
        conn.close()