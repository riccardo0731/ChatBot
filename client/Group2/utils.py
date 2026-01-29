import json
import socket

ENCODING = "utf-8"
PORT = 5000
BUFFER = 1024

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

def create_json_msg(sender_name, sender_ip, message):
    return json.dumps({
        "from": {
            "name": sender_name,
            "ip": sender_ip
        },
        "message": message
    })

def decode_json_msg(data):
    try:
        return json.loads(data.decode(ENCODING))
    except:
        return None
