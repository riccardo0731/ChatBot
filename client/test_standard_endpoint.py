# Import socket library
import socket as sck
import json 

# Server connection settings
HOST = "127.0.0.1"
PORT = 65432
NAME = "Pippo"

# Socket creation
with sck.socket(family = sck.AF_INET, type = sck.SOCK_STREAM) as s:

    # Connection to server
    s.connect( (HOST, PORT) )

    # Get the string to encode from the user
    msg = str(input("Insert string to encode:"))

    json_msg = {
            "from": {
                "name": NAME,
                "ip":  "127.0.0.1"
            },
            "to": "127.0.0.1",
            "msg": msg
        }


    # Send the transformation request
    s.send(json.dumps(json_msg).encode())

    # Received the transformed string
    data = s.recv(1024)

    # Print out the result
    print(f"{json.loads(data.decode())}")