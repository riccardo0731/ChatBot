# Distributed Chat System - Class Chat Project

## 1. Project Overview
Welcome to the official repository for the **Distributed Class Chat System**. This project implements a centralized Client-Server architecture designed to facilitate real-time messaging between multiple independent client implementations.

The repository is structured as a **Monorepo**, hosting the central Server logic alongside five distinct Client implementations (Groups 1 through 5), all operating under a unified communication protocol.

## 2. Architecture & File Structure
The project relies on a strict directory hierarchy to manage shared dependencies. The `utils.py` file acts as the core protocol definition and must be accessible to all components.

```text
PROJECT_ROOT/
├── utils.py             # [CORE] Shared JSON protocol & Network utilities (by Group 3)
├── server/              # Central Server Module (by Group 3)
│   ├── server_main.py   # Server Entry Point
│   └── chat_server.py   # Connection Handling Logic
├── client/              # Student Implementations
│   ├── Group1/          # Client implementation by Group 1
│   ├── Group2/          # Client implementation by Group 2
│   ├── Group3/          # Client implementation by Group 3 
│   ├── Group4/          # Client implementation by Group 4
│   └── Group5/          # Client implementation by Group 5
└── README.md            # General Documentation
```

## 3. The Protocol (Strict JSON Standard)
Interoperability is the primary goal of this project. Regardless of the programming language or interface used by the client groups, **ALL** TCP messages must adhere to the following JSON schema.

### Message Format
Every payload sent to the server must be a serialized JSON object:

```json
{
  "from": {
    "name": "SenderUsername",
    "ip": "SenderIPAddress"
  },
  "to": "RecipientUsername",
  "msg": "Content of the message"
}
```

> **Developer Note:** To ensure compliance, it is highly recommended to import and utilize the `create_json_msg` and `decode_json_msg` functions provided in the `utils.py` shared library.

## 4. Quick Start Guide

To run the system locally, follow this strict execution order to avoid connection errors.

### Step 1: Launch the Server
The server acts as the central router and must be active before any client attempts to connect.

```bash
# From the project root
cd server
python server_main.py
```
*Expected Output: `Server listening on 0.0.0.0:65432...`*

### Step 2: Launch a Client (e.g., Group 3)
Open a **new terminal window/tab**, leaving the server running in the first one.

```bash
# From the project root
cd client/Group3
python client.py
```

## 5. Documentation & Wiki

Detailed technical specifications are available in the repository Wiki or the specific documentation folders:

* **[Server Specifications](wiki/Server-Specs)**: Detailed routing logic and error handling.
* **[Group 3 Client Docs](client/Group3/README.md)**: Specific usage guide for the Group 3 CLI implementation.

## 6. Contribution Guidelines
* **Do not modify `utils.py`**: This file represents the immutable contract between groups.
* **Do not commit personal configurations**: Ensure `.gitignore` is properly set up.
* **Pull Requests**: Changes to the Server logic require approval from all Team Leads.
