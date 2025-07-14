VoiceMate
VoiceMate is a Python-based voice assistant application with a graphical user interface (GUI) that allows users to execute commands via voice or text input. It supports various functionalities such as opening applications, searching Wikipedia, taking screenshots, and visualizing command history and system performance.
Project Structure
voice_assistant/
├── main.py
├── gui.py
├── commands.py
├── visualizations.py
├── config.py
├── utils.py
├── requirements.txt
└── README.md


main.py: Entry point for the application.
gui.py: Manages the GUI and core application logic.
commands.py: Handles command processing and execution.
visualizations.py: Manages visualization-related functionality (e.g., charts, word clouds).
config.py: Stores configuration and styling settings.
utils.py: Contains utility functions like logging.
requirements.txt: Lists required Python dependencies.

Features

Voice and text-based command input
Supports commands like opening applications, web browsing, file management, and system control
Visualizations for command history, word clouds, system performance, and sentiment analysis
Light and dark theme support
Text-to-speech feedback
Screenshot capture
File explorer visualization

Prerequisites

Python 3.7+
A working microphone for voice commands
Windows operating system (some commands like notepad and calc are Windows-specific)
Internet connection for Wikipedia and online search functionality

Installation

Clone or download the project to your local machine.
Navigate to the project directory:cd voice_assistant


Create a virtual environment (optional but recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install the required dependencies:pip install -r requirements.txt


Install the spaCy language model:python -m spacy download en_core_web_sm


Ensure you have the necessary system dependencies:
For Windows, ensure sapi5 is available for text-to-speech (pyttsx3).



Usage

Run the application:python main.py


The GUI will launch, and the assistant will prompt for your name via voice or text input.
Use the microphone button (🎤 Listen) to enable voice commands or type commands in the text entry field.
Example commands:
"Open browser"
"Search Wikipedia for Python"
"Take a screenshot"
"Show visualizations"
"What time is it?"


Access visualizations via the "📊 Visualizations" button to view command history, word clouds, and more.
Adjust settings (theme, voice speed) via the "⚙️ Settings" button.

Available Commands

System Commands: Open browser, notepad, calculator, file explorer
Web Commands: Search online, open website, search Wikipedia
File Operations: Create file, list files, copy file
System Control: Shutdown, restart, lock computer
Mouse/Keyboard: Move mouse, click, scroll, type
Visualizations: Show command history, word cloud, system performance, conversation timeline, sentiment analysis
Application Control: Open/close applications
Utility: Take screenshot, exit program

Notes

Some commands (e.g., shutdown, file operations) require appropriate system permissions.
The visualizations (e.g., system performance, sentiment analysis) use simulated data for demonstration.
Voice recognition requires a stable internet connection for Google Speech Recognition.
The application is optimized for Windows due to specific system commands; modifications may be needed for other operating systems.

Troubleshooting

Microphone issues: Ensure your microphone is properly configured and not muted.
spaCy model not found: Run python -m spacy download en_core_web_sm to install the language model.
TTS errors: Verify that sapi5 is available on your Windows system.
Command not recognized: Check the command syntax or try rephrasing; see the intent_keywords in commands.py for supported commands.

Contributing
Contributions are welcome! Please fork the repository, make changes, and submit a pull request. Ensure your code follows the project's structure and includes appropriate documentation.
License
This project is licensed under the MIT License.
