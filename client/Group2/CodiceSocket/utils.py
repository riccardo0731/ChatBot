import json
import socket

ENCODING = 'utf-8'  
PORT = 5000         
BUFFER = 1024

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return socket.gethostbyname(socket.gethostname())

def create_json_msg(sender_name, sender_ip, message):
    msg_dict = {
        'from': {
            'name': sender_name,
            'ip': sender_ip
        },
        'message': message
    }
    return json.dumps(msg_dict)

def decode_json_msg(data):
    if not data:
        return None
        
    try:
        return json.loads(data.decode(ENCODING))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return None
