# SENEM-AI LLM Server

This repository contains the backend server for the [SENEM-AI project](https://github.com/vipenti/SENEM_Metaverse). It provides the logic for managing the smart students and facilitates communication between the Unity-based main project and the LLM (Large Language Model).

---

## How Does It Work?
The server manages the interaction between the virtual students on the SENEM-AI platform and the LLM. It capture the teacher's speech and transcribe it to generate a student's answer. More specifically, the main components are the following:

1. **student.py**: This defines the behavior and personality traits of the simulated students. It includes personality, intelligence, interest, and happiness parameters that influence the students' interactions during a lecture. Using a starting prompt and input from the professor's speech, it generates responses by interacting with an LLM endpoint.

2. **server.py**: The server's core, built with Flask. It handles communication between Unity and the backend. It receives the speaker's audio data and the student's personality traits, and it provides endpoints for generating text-based and audio-based responses using asynchronous tasks. 

3. **tasks.py**: Manages the asynchronous logic using Celery and Redis to handle multiple student interactions. It processes audio input by transcribing it with Whisper, generates text responses by leveraging the Student class, and optionally converts these responses into audio using Silero TTS.

---

## Prerequisites

Before running the project, ensure the following prerequisites are met:

1. **Python 3.9**: Required for the server and AI backend.
2. **Dependencies**: Install all dependencies listed in `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```
3. **WSL (Optional)**: If running the server on Windows, Windows Subsystem for Linux (WSL) may be required to run Redis. Install it with:
   ```bash
   wsl --install
   ```
4. **Large Language Model (LLM)**: Any LLM capable of handling POST requests can be used. We recommend using [LLM Studio](https://https://lmstudio.ai/) to host a model locally or on a server.

---

## Setup and Startup Instructions

Follow these steps to set up and start the server:

1. **(Windows Only)**: Open a new shell in the project directory and launch WSL by running:
   ```bash
   wsl
   ```
   *Skip this step if you are not using Windows.*

2. **Start Redis**:
   In the same shell, start the Redis server as an administrator:
   ```bash
   sudo service redis-server start
   ```

3. **Start Celery Worker**:
   Open another shell and run the following command to start the Celery worker:
   ```bash
   celery -A tasks worker -l info -P gevent
   ```

4. **Configure the LLM URL**:
   Open the `student.py` file and set the `LLM_url` variable to the URL of your running LLM instance. For example:
   ```python
   LLM_URL = "http://localhost:5000/endpoint"
   ```

5. **Start the Server**:
   Run the `server.py` script to start the server:
   ```bash
   python server.py
   ```

Your server is now up and running!

---

 



