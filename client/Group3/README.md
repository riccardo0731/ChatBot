# Distributed Chat Client - Group 3

## 1. Overview
This software component represents the client-side implementation assigned to **Group 3**.. It is a Command Line Interface (CLI) application developed in Python, designed to communicate with a central server using a strict JSON-based protocol over TCP/IP sockets.

## 2. System Requirements
To successfully execute this client, the following environments and dependencies are required:

* **Python 3.x** (Tested on Python 3.8 and newer).
* **Network Connectivity**: Active LAN connection or localhost loopback (`127.0.0.1`) for local testing.
* **Shared Library**: The `utils.py` file must be present in the project root directory.

## 3. Directory Structure & Dependencies
The application relies on a relative path resolution mechanism to import shared protocol definitions. The file hierarchy must be preserved exactly as follows to ensure the application can locate the `utils` module:

```text
PROJECT_ROOT/
├── utils.py             # [CRITICAL] Shared protocol and utility functions
├── server/              # Server-side components
└── client/
    └── Group3/          # Group 3 working directory
        ├── client.py    # Main application entry point
        └── README.md    # This documentation file
```

> **Warning:** The `client.py` script includes a system path modification (`sys.path.append`) to automatically locate `utils.py` in the project root (`../../utils.py`). Moving the script independently or altering the folder structure will result in an `ImportError`.

## 4. Installation and Execution

### Step 1: Navigation
Open a terminal window (Command Prompt, PowerShell, or Bash) and navigate specifically to the Group 3 directory:

```bash
cd client/Group3
```

### Step 2: Execution
Run the client application using the Python interpreter:

```bash
python client.py
```
*(Note: On some UNIX-based systems or macOS, you may need to use `python3 client.py` if Python 2 is still the system default).*

## 5. Usage Guide

Upon execution, the application initializes an interactive session. Follow these steps:

1.  **Server Configuration**:
    * Enter the IPv4 address of the central server.
    * *Tip*: Press `ENTER` without typing to default to `127.0.0.1` (Localhost).

2.  **User Registration**:
    * Enter a unique **Username** when prompted. This identifier will be used for message routing.

3.  **Messaging Loop**:
    The interface operates on a transactional basis for each message:
    * `To:` Specify the recipient's username (case-sensitive).
    * `Msg:` Enter the text payload you wish to send.

### Protocol Compliance
The client automatically encapsulates user input into the required strict JSON schema before transmission:

```json
{
  "from": {
    "name": "YourUsername",
    "ip": "YourLocalIP"
  },
  "to": "RecipientUsername",
  "msg": "Payload Text"
}
```

## 6. Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'utils'`
* **Cause:** The Python interpreter cannot locate the shared utility library.
* **Solution:** Verify that `utils.py` exists in the project root (two levels up) and that you are executing the command from within the `client/Group3/` directory, not from the root.

### Issue: `ConnectionRefusedError`
* **Cause:** The client cannot establish a TCP handshake with the target host.
* **Solution:**
    1.  Ensure the **Server** application (`server_main.py`) is currently running.
    2.  Verify that the IP address provided during the setup phase is correct.
    3.  Check for firewall rules blocking port `65432`.

