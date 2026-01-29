import sys
import socket
import utils

"""
    Name: receive_messages

    Parameters: 
        sock | socket object | socket of the client

    Exceptions: 
        Any | Error logged in the server terminal

    Description: Function for the receiver thread, listens for incoming messages from the server and prints them on the screen.

"""
def receive_messages(sock):
    """
    Listens for incoming messages from the server and prints them to the standard output.
    This function is intended to be executed in a separate thread to avoid blocking the main execution.
    
    Args:
        sock (socket.socket): The active socket connection to the server.
    """
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[!] Disconnected from server.")
                break
            
            # Decode the received data using the shared utility module
            msg = utils.decode_json_msg(data)
            
            if msg:
                # Format and display the message content
                sender = msg['from']['name']
                text = msg['msg']
                print(f"\n >>> {sender}: {text}")
                
                # Restore the user input prompt to maintain UI consistency
                print("To: ", end="", flush=True)
                
        except Exception as e:
            print(f"\n[!] Receive Error: {e}")
            break
    
    # If the connection loop terminates (e.g., server downtime), exit the application
    sys.exit()