import json
import socket

# Standard Configuration
PORT = 65432
# Using UTF-8 to even support emoji and special characters
ENCODING = 'utf-8' 

def get_local_ip():
    """ Find Local Machine IP Address """
    try:
        # Get effective IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def create_json_msg(sender_name, sender_ip, target, text):
    """
    Create dictionary folllowing the standard:
    {
      "from": { "name": "...", "ip": "..." },
      "to": "...",
      "msg": "..."
    }
    """
    return json.dumps({
        "from": {
            "name": sender_name,
            "ip": sender_ip
        },
        "to": target,
        "msg": text
    })

def decode_json_msg(bytes_data):
    """Transform the received bytes into a Python dictionary"""
    try:
        return json.loads(bytes_data.decode(ENCODING))
    except json.JSONDecodeError:
        return None
    
def get_standard_json():
    """Return the standard JSON as a string(for debugging)"""
    return """
    {
      "from": { "name": "...", "ip": "..." },
      "to": "...",
      "msg": "..."
    }
    """