# Distributed Systems & IoT - Class Chat Project

![Server Capacity](https://img.shields.io/badge/Server_Capacity-%3E_6000_Clients-brightgreen?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge)

## 1. Project Overview
Welcome to the official repository for the **Distributed Class Chat System**. This project implements a centralized Client-Server architecture designed to facilitate real-time messaging between multiple independent client implementations.

The system is built on raw TCP/IP sockets using a multithreaded architecture, capable of handling high-concurrency scenarios without relying on external asynchronous frameworks.

## 2. Architecture & File Structure
The project relies on a strict directory hierarchy to manage shared dependencies. The `utils.py` file acts as the core protocol definition.

```text
PROJECT_ROOT/
├── utils.py                 # [CORE] Shared JSON protocol & Network utilities
├── test_breaking_point.py   # [TEST] Ramp-up load testing script
├── test_server_stress.py    # [TEST] Bot simulation suite
├── server/                  # Central Server Module
│   ├── server_main.py       # Server Entry Point
│   └── chat_server.py       # Connection Handling & Command Dispatcher
└── client/                  # Student Implementations
    └── Group3/              # Reference CLI Client (Group 3)
```

## 3. The Protocol (Strict JSON Standard)
Interoperability is the primary goal. Regardless of the programming language, **ALL** TCP messages must adhere to the following JSON schema:

```json
{
  "from": {
    "name": "SenderUsername",
    "ip": "SenderIPAddress"
  },
  "to": "RecipientUsername", // or Command (e.g., "/list")
  "msg": "Content of the message"
}
```

## 4. Server Endpoints & Commands
The server implements a **Command Dispatcher** pattern. Users can interact with the server logic by addressing messages to specific endpoints instead of other users.

| Endpoint | Description | Usage Example |
| :--- | :--- | :--- |
| **`/list`** | Retrieves the list of currently connected users. | `To: /list` |
| **`/time`** | Returns the current server time. | `To: /time` |
| **`/shout`** | Broadcasts a message to **ALL** connected clients. | `To: /shout` |
| **`/help`** | Displays the list of available commands. | `To: /help` |
| **`/standard`** | Returns the raw JSON protocol structure (Debug). | `To: /standard` |

> **Note:** The server enforces **Username Uniqueness**. If a client attempts to connect with a name already in use, the connection is rejected immediately.

## 5. Testing & Performance
This repository includes professional-grade stress testing tools to verify server stability under load.

### Load Capacity
Through rigorous testing using the `test_breaking_point.py` ramp-up script, the server has been certified to handle **over 6,000 concurrent connections** on standard consumer hardware without crashing or significant latency.

### How to Run Tests
1.  **Start the Server**:
    ```bash
    python server/server_main.py
    ```
2.  **Run the Stress Test** (Simulates 50 bots chatting):
    ```bash
    python test_server_stress.py
    ```
3.  **Run the Load Test** (Infinite ramp-up until failure):
    ```bash
    python test_breaking_point.py
    ```

## 6. Contribution Guidelines
* **Do not modify `utils.py`**: This file represents the immutable contract between groups.
* **Pull Requests**: Changes to the Server logic require approval from Team Leads.

---
*Distributed Systems Course - Academic Year 2025/2026*
*With AI tutoring.*