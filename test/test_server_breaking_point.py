### !!! COMPLETELY AI GENERATED CODE !!! ###

import sys
import os
import socket
import threading
import time
import random

# --- AUTOMATIC IMPORT RESOLUTION ---
# Ensures the script can locate 'utils.py' regardless of directory placement
current_dir = os.path.dirname(os.path.abspath(__file__))
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
# -----------------------------------

# TEST CONFIGURATION
SERVER_HOST = "127.0.0.1"
SERVER_PORT = utils.PORT
BATCH_SIZE = 50          # Number of clients added per cycle
BATCH_INTERVAL = 2       # Seconds between batches

# Global State Tracking
active_connections = 0
error_count = 0
stop_signal = False

def persistent_client(client_id):
    """
    Name: persistent_client

    Description: 
        Simulates a client that connects and maintains the connection indefinitely 
        by sending periodic heartbeat messages. This tests the server's capacity 
        to hold open sockets.
    """
    global active_connections, error_count, stop_signal
    
    name = f"LoadTester_{client_id}"
    sock = None
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5) # Strict timeout to detect server lag
        sock.connect((SERVER_HOST, SERVER_PORT))
        
        # 1. Handshake
        sock.send(name.encode(utils.ENCODING))
        
        # 2. Wait for Server Acknowledgement
        sock.recv(1024)
        
        # Connection established successfully
        active_connections += 1
        
        # 3. Keep-Alive Loop
        while not stop_signal:
            # Send a heartbeat every few seconds to prevent idle timeout
            time.sleep(3) 
            try:
                # Use a lightweight payload to minimize CPU usage, focusing test on RAM/Sockets
                msg = utils.create_json_msg(name, "0.0.0.0", "Everyone", "Heartbeat signal")
                sock.send(msg.encode(utils.ENCODING))
                
                # Optional: Read response to clear buffer
                sock.setblocking(False)
                try:
                    sock.recv(1024)
                except BlockingIOError:
                    pass
                sock.setblocking(True)

            except Exception:
                # If sending fails, the server likely severed the connection
                break 

    except Exception:
        error_count += 1
    finally:
        if sock:
            sock.close()
        # We do not decrement active_connections immediately to preserve the peak value for logging

def execute_load_test():
    """
    Name: execute_load_test

    Description:
        Orchestrates the ramp-up stress test. It spawns batches of threads 
        until the server fails or the user interrupts the process.
    """
    global stop_signal
    print(f"🚀 INITIALIZING BREAKING POINT TEST ON {SERVER_HOST}:{SERVER_PORT}")
    print(f"Strategy: Adding {BATCH_SIZE} clients every {BATCH_INTERVAL} seconds.")
    print("Press CTRL+C to stop the test manually.\n")
    
    total_spawned = 0
    batch_index = 0
    
    try:
        while True:
            batch_index += 1
            print(f"--- Batch {batch_index} ---")
            print(f"📊 Active Connections: {active_connections} | Total Errors: {error_count}")
            
            # Fail-safe: If errors spike, the server is collapsing
            if error_count > 50:
                print("\n⚠️ CRITICAL WARNING: High error rate detected. Server stability compromised.")
                print("Stopping test to prevent system freeze.")
                break

            # Spawn a new batch of clients
            for _ in range(BATCH_SIZE):
                total_spawned += 1
                t = threading.Thread(target=persistent_client, args=(total_spawned,))
                t.daemon = True # Threads will terminate when main script ends
                t.start()
            
            # Pause to allow server to stabilize before next batch
            time.sleep(BATCH_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user.")
    
    # Signal all threads to stop
    stop_signal = True
    
    # Final Report
    print(f"\n{'-'*30}")
    print(f"📈 FINAL PERFORMANCE REPORT")
    print(f"{'-'*30}")
    print(f"🏆 Peak Stable Connections: {active_connections}")
    print(f"💀 Failed Connections:      {error_count}")
    print(f"👥 Total Attempts:          {total_spawned}")
    print(f"{'-'*30}")

if __name__ == "__main__":
    execute_load_test()