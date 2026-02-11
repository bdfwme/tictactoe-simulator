# tictactoe-simulator
a dynamic tictactoe simulator project for my semester coursework
Project: Blank's Tic-Tac-Toe
1. Overview

This is a web-based Tic-Tac-Toe application built with Python (Flask). It features a modern "Deep Black" minimalist interface and supports two game modes:

    Player vs. Computer: A quick match against a randomized AI.

    Remote Multiplayer (PvP): Two players can compete from different devices using a shared Room Code.

The project demonstrates the core concepts of Client-Server Architecture, REST APIs, and Asynchronous State Management.
2. Technology Stack

    Backend: Python 3, Flask (Web Framework)

    Frontend: HTML5, CSS3 (Custom Dark Theme), Vanilla JavaScript

    Deployment: Render (Cloud Hosting)

3. Key Features

    Room-Based Multiplayer: Uses unique 4-character codes (e.g., ABCD) to create private game sessions.

    Real-Time Synchronization: Both players see moves instantly without reloading the page.

    Smart Replay System: When a game ends, either player can click "PLAY AGAIN" to instantly reset the board for both users.

    Validation: The server prevents illegal moves (e.g., playing on top of another piece or playing out of turn).

4. How to Run Locally

    Install Flask:
    Bash

    pip install flask

    Start the Server:
    Bash

    python app.py

    Access the Game: Open your browser and navigate to http://127.0.0.1:5000

5. Architecture & Logic

The application follows a Polling Architecture:

    State Storage: The Python server holds a dictionary (games) that acts as a temporary database. It stores the board ["X", "", "O", ...], the current turn, and the winner.

    API Communication: The frontend sends moves via POST requests to /move.

    The Heartbeat: The browser sends a GET request to /status/<room_id> every 1 second. This ensures that when Player A moves, Player B's screen updates automatically.
