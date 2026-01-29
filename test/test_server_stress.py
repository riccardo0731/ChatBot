### !!! COMPLETELY AI GENERATED CODE !!! ###

import sys
import os
import socket
import threading
import time
import random

# --- AUTOMATIC IMPORT FIX (Ensures utils.py is found) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Attempt to locate utils in current dir, parent, or grand-parent dir
paths_to_check = [current_dir, os.path.join(current_dir, '..'), os.path.join(current_dir, '..', '..')]

found_utils = False
for p in paths_to_check:
    sys.path.append(p)
    try:
        import utils
        found_utils = True
        break
    except ImportError:
        sys.path.remove(p)

if not found_utils:
    print("❌ CRITICAL ERROR: Unable to locate 'utils.py'. Please place this script in the project root.")
    sys.exit(1)
# --------------------------------------------------------

# TEST CONFIGURATION
SERVER_HOST = "127.0.0.1"
SERVER_PORT = utils.PORT
NUM_BOTS = 50          # Number of concurrent simulated clients
DELAY_BETWEEN_MSGS = 0.5
TEST_DURATION = 10     # Duration of the stress test in seconds

# Terminal Colors for visual feedback
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def log(type, msg):
    """Helper function for formatted logging."""
    if type == "OK":
        print(f"{Colors.OKGREEN}[SUCCESS]{Colors.ENDC} {msg}")
    elif type == "ERR":
        print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {msg}")
    elif type == "INFO":
        print(f"{Colors.OKBLUE}[INFO]{Colors.ENDC} {msg}")

# --- TEST 1: SINGLE BOT BEHAVIOR (User Simulation) ---
def bot_behavior(bot_id):
    """
    Name: bot_behavior

    Parameters:
        bot_id | int | Unique identifier for the simulated bot

    Description: 
        Simulates a client lifecycle: connects, performs handshake, 
        sends random messages for a duration, and disconnects.
    """
    name = f"Bot_{bot_id}"
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5) # Set timeout in case server hangs
        sock.connect((SERVER_HOST, SERVER_PORT))
        
        # 1. Handshake Phase
        sock.send(name.encode(utils.ENCODING))
        
        # Receive Welcome Message
        try:
            welcome = sock.recv(4096) 
            if b"Welcome" in welcome or b"Benvenuto" in welcome:
                # Handshake successful
                pass
            else:
                log("ERR", f"{name} handshake failed or server rejected connection.")
                return
        except socket.timeout:
            log("ERR", f"{name} timed out waiting for welcome message.")
            return

        # 2. Messaging Loop Phase
        start_time = time.time()
        while time.time() - start_time < TEST_DURATION:
            # Select random target: a specific command, a user, or everyone
            target = random.choice(["/time", "/list", "Bot_1", "Everyone", "/shout"])
            msg_text = f"Stress test message from {name}"
            
            # Construct standard JSON packet
            json_pkt = utils.create_json_msg(name, "127.0.0.1", target, msg_text)
            sock.send(json_pkt.encode(utils.ENCODING))
            
            # Read potential response to prevent TCP buffer congestion
            try:
                sock.recv(1024)
            except socket.timeout:
                pass
            
            # Randomized sleep to simulate human behavior variance
            time.sleep(random.uniform(0.1, 1.0))

    except Exception as e:
        log("ERR", f"{name} encountered an error: {e}")
    finally:
        sock.close()

# --- TEST 2: UNIQUENESS CHECK (Security Test) ---
def test_duplicate_name():
    """
    Name: test_duplicate_name

    Description: 
        Connects two clients with the same username to verify 
        that the server correctly rejects the duplicate.
    """
    print(f"\n{Colors.HEADER}--- SECURITY TEST: DUPLICATE USERNAME REJECTION ---{Colors.ENDC}")
    
    # Client A (The Original User)
    sock_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_a.connect((SERVER_HOST, SERVER_PORT))
    sock_a.send(b"TestUser_Unique")
    time.sleep(0.5) # Allow server to process registration

    # Client B (The Impostor)
    sock_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_b.connect((SERVER_HOST, SERVER_PORT))
    sock_b.send(b"TestUser_Unique") # Sending the same name

    try:
        # Client B should receive an error message and be disconnected
        data = sock_b.recv(1024).decode(utils.ENCODING)
        
        # Check for keywords defined in server response
        if "Error" in data or "ERRORE" in data or "⛔" in data:
            log("OK", "The server correctly rejected the duplicate username.")
        else:
            log("ERR", f"The server accepted the duplicate! Response: {data}")
    except Exception as e:
        log("ERR", f"Error during duplicate test: {e}")
    finally:
        sock_a.close()
        sock_b.close()

# --- MAIN RUNNER ---
if __name__ == "__main__":
    print(f"{Colors.HEADER}--- STARTING SERVER STRESS TEST SUITE ---{Colors.ENDC}")
    print(f"Target: {SERVER_HOST}:{SERVER_PORT}")
    
    # Preliminary Server Health Check
    try:
        s = socket.socket()
        s.connect((SERVER_HOST, SERVER_PORT))
        s.close()
        log("OK", "Server is reachable. initializing tests...")
    except:
        log("ERR", "SERVER OFFLINE! Please start 'server_main.py' in a separate terminal first.")
        sys.exit()

    # Execute Security Test
    test_duplicate_name()

    # Execute Stress Test
    print(f"\n{Colors.HEADER}--- STRESS TEST: DEPLOYING {NUM_BOTS} BOTS ---{Colors.ENDC}")
    threads = []
    
    for i in range(NUM_BOTS):
        t = threading.Thread(target=bot_behavior, args=(i,))
        threads.append(t)
        t.start()
        # Small delay to prevent unrealistic simultaneous connection spikes
        time.sleep(0.05) 

    print(f"Waiting for {TEST_DURATION} seconds of load testing...")
    
    # Wait for all threads to complete
    for t in threads:
        t.join()

    print(f"\n{Colors.HEADER}--- TEST SUITE COMPLETED ---{Colors.ENDC}")
    print("Check the SERVER terminal to verify stability or crashes.")