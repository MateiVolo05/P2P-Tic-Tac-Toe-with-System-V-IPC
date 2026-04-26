# P2P Tic-Tac-Toe with System-V IPC
## Decentralized Peer-to-Peer Gaming via Unix Message Queues

## 📌 Project Overview
This project is a Peer-to-Peer (P2P) implementation of the classic Tic-Tac-Toe game, designed to run as two independent processes communicating via **System-V Message Queues**. The application demonstrates advanced Inter-Process Communication (IPC) techniques, multi-threaded GUI synchronization, and persistent data management.

## ⚙️ Key Technical Features
* **Decentralized P2P Communication:** Uses `sysv_ipc` for real-time synchronization of moves between players without requiring a central server.
* **Multi-threaded Architecture:** Implements a dedicated `CommunicationManager` thread (based on `QThread`) to handle asynchronous message reception, ensuring a responsive and lag-free UI.
* **Persistent Game History:** Integrates an **SQLite** database to track player statistics, scores, and timestamps for every matchup.
* **Dynamic Role Assignment:** Automatically determines player roles (X or 0) and turns through an initial handshake protocol over the message queue.
* **Win/Draw Detection:** Real-time evaluation of board states to determine game outcomes and update the persistent score history.

## 📊 System Design
The project follows a structured engineering approach, featuring:
* **UML Class Diagram:** Defines the interaction between the application logic (`MainWindow`), the communication layer, and the database manager.
* **E-R Diagram:** Illustrates the relational database schema used for storing player profiles and game results.

## 🛠 Tools & Technologies
* **Language:** Python 3
* **GUI Framework:** PyQt5
* **IPC Mechanism:** System-V Message Queues (`sysv_ipc`)
* **Database:** SQLite3
* [cite_start]**OS:** Linux (required for System-V IPC support) [cite: 136]

## 🚀 How to Run
1. Ensure you are on a Linux-based system.
2. Install dependencies: `pip install PyQt5 sysv_ipc`
3. Launch the first instance: `python main.py` (Enter your name and wait for an opponent).
4. Launch the second instance: `python main.py` (Enter a different name to connect).
