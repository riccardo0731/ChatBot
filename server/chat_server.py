import json

### CHAT SERVER FUNCTIONS ###

msg_standard = {
                "from": {
                	   "name": "YourName",
                         "ip":   "YourIp",
                	},

                "to":   "IpToSendMsgTo",
                "msg":  "YourMsg"
            }


def client_handle(conn, addr):

    with conn:
        print(f"Received message from {addr}")

        msg = conn.recv(1024)
        if not msg:
            return

        actual_msg = json.loads(msg.decode())
        
        print(f"Received JSON: {actual_msg}")

        if check_standard_endpoint(actual_msg):
            conn.send(json.dumps(msg_standard).encode())

def check_standard_endpoint(msg: dict):
    if(msg['msg'] == '/standard'):
        return True
    else:
        return False


