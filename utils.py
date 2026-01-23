import json
import socket

# Configurazione Standard
PORT = 65432
# Usiamo UTF-8 per supportare emoji e caratteri speciali 😎
ENCODING = 'utf-8' 

def get_local_ip():
    """Trova l'indirizzo IP della macchina locale."""
    try:
        # Trucchetto per trovare l'IP effettivo usato per uscire verso internet
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def create_json_msg(sender_name, sender_ip, target, text):
    """
    Crea il dizionario secondo il tuo standard rigoroso:
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
    """Trasforma i byte ricevuti in dizionario Python."""
    try:
        return json.loads(bytes_data.decode(ENCODING))
    except json.JSONDecodeError:
        return None