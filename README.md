# Real-Time AI Chat Desktop GUI Application

## Project Introduction

This project is a desktop application that enables real-time chatting with an AI powered by Microsoft's DialoGPT-medium model. The application features a user-friendly graphical interface built with PyQt6, allowing users to input messages and receive AI-generated responses instantly. The AI model runs in a Docker container, ensuring easy deployment and dependency management across different platforms. The application is designed to be responsive, leveraging QThread for asynchronous processing to keep the UI smooth during AI response generation.

## Technologies Used

- **Python 3.10**: The core programming language for the application logic.
- **PyQt6**: A Python library for creating the graphical user interface (GUI), providing a chat window with input fields, a send button, and a conversation history display.
- **Microsoft DialoGPT-medium**: A conversational AI model from Hugging Face's Transformers library, used for generating human-like responses.
- **Hugging Face Transformers**: Provides the framework to load and interact with the DialoGPT model.
- **PyTorch**: The backend for running the DialoGPT model, handling tensor computations for AI inference.
- **QThread**: A PyQt6 component for asynchronous processing, ensuring the GUI remains responsive while the AI generates responses.

## Installation Instructions

### Prerequisites

Before setting up the project, ensure the following are installed on your system:

- **Docker Desktop**: Required to build and run the Docker container. Download and install from [Docker's official website](https://www.docker.com/products/docker-desktop/).
- **Python 3.10 or higher**: Download from [Python's official website](https://www.python.org/downloads/).
- **Git**: For cloning the repository (optional). Download from [Git's official website](https://git-scm.com/downloads/).

### Step-by-Step Installation

1. **Clone the Repository** (or download the project files):
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create and Activate a Virtual Environment:**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python Dependencies: Install the required packages using requirements.txtr**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application: Execute the GUI script**:
   
   ```bash
   python gui.py
   ```

### Usage

1. Upon running `main.py`, a GUI window will appear with:
   - A text area displaying the conversation history.
   - An input field for typing messages.
   - A "Send" button to submit messages.
2. Type a message in the input field and press "Send" or hit Enter.
3. The AI will respond, and the conversation will be displayed in the text area.
4. Close the window to terminate the application and the Docker container.
