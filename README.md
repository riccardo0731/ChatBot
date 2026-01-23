# ChatBot
Obiettivo: sviluppare una chat multi canale, con chat privata tra utenti, da poter utilizzare su tutti i computer del laboratorio 39

per domande sulla rete: scrivere  Munzio Maurizio




import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Non serve che l'IP sia raggiungibile, serve solo a "risvegliare" l'interfaccia
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

print(f"Il tuo IP locale è: {get_local_ip()}")
