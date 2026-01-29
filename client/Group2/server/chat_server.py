import threading as thr
import utils

clients = {}
lock = thr.Lock()

def broadcast(data, sender_conn):
    with lock:
        for conn in clients.values():
            if conn != sender_conn:
                conn.send(data)

def handle_client(conn, addr):
    name = None
    try:
        data = conn.recv(utils.BUFFER)
        if not data:
            return

        name = data.decode(utils.ENCODING).strip()

        with lock:
            clients[name] = conn

        print(f"[CONNESSO] {name} ({addr[0]})")

        join_msg = utils.create_json_msg(
            "SERVER",
            "0.0.0.0",
            f"{name} è entrato nella chat"
        )
        broadcast(join_msg.encode(utils.ENCODING), conn)

        while True:
            data = conn.recv(utils.BUFFER)
            if not data:
                break

            print(f"[MSG] {name}")
            broadcast(data, conn)

    except Exception as e:
        print(f"[ERRORE] {e}")

    finally:
        if name:
            with lock:
                clients.pop(name, None)

            leave_msg = utils.create_json_msg(
                "SERVER",
                "0.0.0.0",
                f"{name} ha lasciato la chat"
            )
            broadcast(leave_msg.encode(utils.ENCODING), conn)

            print(f"[DISCONNESSO] {name}")
        conn.close()
