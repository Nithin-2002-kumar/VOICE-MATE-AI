import subprocess
import os
import webbrowser
import pyautogui
import wikipedia
import speech_recognition as sr
from datetime import datetime
from tkinter import messagebox
from utils import log_action

class CommandProcessor:
    def __init__(self, gui):
        self.gui = gui
        self.intent_keywords = {
            "open browser": "open_browser",
            "open notepad": "open_notepad",
            "open file explorer": "open_file_explorer",
            "search wikipedia": "search_wikipedia",
            "open calculator": "open_calculator",
            "time": "time",
            "screenshot": "screenshot",
            "shutdown": "shutdown",
            "create a file": "create_a_file",
            "move mouse": "move_mouse",
            "click": "click",
            "scroll": "scroll",
            "type": "type",
            "exit": "exit_program",
            "delete": "delete",
            "open application": "open application",
            "close application": "close application",
            "open website": "open website",
            "close website": "close website",
            "search online": "search",
            "list files": "list_files",
            "copy file": "copy_file",
            "show visualizations": "show_visualizations",
        }

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.gui.master.after(0, self.gui.assistant_speaks, "Listening...")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                return None
        try:
            return recognizer.recognize_google(audio, language='en').lower()
        except sr.UnknownValueError:
            self.gui.master.after(0, self.gui.assistant_speaks, "I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError as e:
            self.gui.master.after(0, self.gui.assistant_speaks, f"Could not request results; check your internet connection.")
            log_action(f"Speech recognition error: {e}", "ERROR")
            return None

    def process_command(self, command):
        command = command.lower()
        intents = []
        for keyword, intent in self.intent_keywords.items():
            if keyword in command:
                intents.append(intent)
                break
        return intents

    def execute_command(self, command):
        if self.gui.expecting_name:
            self.gui.config.user_preferences['name'] = command
            self.gui.assistant_speaks(f"Hello {command}! How can I help you today?")
            self.gui.expecting_name = False
            log_action(f"Executed command: {command}")
            return

        intents = self.process_command(command)
        for intent in intents:
            try:
                if intent == "open_browser":
                    self.gui.assistant_speaks("Opening browser...")
                    subprocess.run(["start", "chrome"], shell=True)
                elif intent == "open_notepad":
                    os.system('notepad')
                    self.gui.assistant_speaks(f"Opening Notepad, {self.gui.config.user_preferences['name']}")
                elif intent == "open_file_explorer":
                    self.gui.assistant_speaks("Opening File Explorer...")
                    subprocess.run(["explorer"], shell=True)
                elif intent == "search_wikipedia":
                    self.gui.assistant_speaks(f"What do you want to search for, {self.gui.config.user_preferences['name']}?")
                    query = self.listen()
                    if query:
                        result = wikipedia.summary(query, sentences=2)
                        self.gui.assistant_speaks(f"According to Wikipedia: {result}")
                elif intent == "open_calculator":
                    os.system('calc')
                    self.gui.assistant_speaks(f"Opening Calculator, {self.gui.config.user_preferences['name']}")
                elif intent == "time":
                    now = datetime.now().strftime("%H:%M:%S")
                    self.gui.assistant_speaks(f"The current time is {now}, {self.gui.config.user_preferences['name']}")
                elif intent == "screenshot":
                    self.take_screenshot()
                elif intent == "shutdown":
                    self.gui.assistant_speaks(f"Are you sure you want to shut down, {self.gui.config.user_preferences['name']}?")
                    confirmation = self.listen()
                    if confirmation and "yes" in confirmation:
                        self.gui.assistant_speaks(f"Shutting down the computer, {self.gui.config.user_preferences['name']}")
                        subprocess.run(['shutdown', "/s", "/t", "0"], shell=True)
                    else:
                        self.gui.assistant_speaks(f"Shutdown cancelled, {self.gui.config.user_preferences['name']}")
                elif intent == "create_a_file":
                    self.gui.assistant_speaks("What should be the name of the file?")
                    filename = self.listen()
                    if filename:
                        filepath = os.path.join(os.getcwd(), f"{filename}.txt")
                        with open(filepath, "w") as file:
                            file.write("This is a new file created by your voice assistant.")
                        self.gui.assistant_speaks(f"File {filename}.txt has been created in the current directory, {self.gui.config.user_preferences['name']}")
                elif intent == "move_mouse":
                    self.gui.assistant_speaks(f"Where do you want to move the mouse, {self.gui.config.user_preferences['name']}? Please tell the coordinates.")
                    position = self.listen()
                    if position:
                        try:
                            x, y = map(int, position.split())
                            pyautogui.moveTo(x, y)
                            self.gui.assistant_speaks(f"Mouse moved to position ({x}, {y})")
                        except ValueError:
                            self.gui.assistant_speaks("Sorry, I couldn't understand the position.")
                elif intent == "click":
                    pyautogui.click()
                    self.gui.assistant_speaks(f"Mouse clicked, {self.gui.config.user_preferences['name']}.")
                elif intent == "scroll":
                    self.gui.assistant_speaks("Would you like to scroll up or down?")
                    direction = self.listen()
                    if direction and "up" in direction:
                        pyautogui.scroll(10)
                        self.gui.assistant_speaks("Scrolled up")
                    elif direction and "down" in direction:
                        pyautogui.scroll(-10)
                        self.gui.assistant_speaks("Scrolled down")
                elif intent == "type":
                    self.gui.assistant_speaks("What would you like me to type?")
                    text = self.listen()
                    if text:
                        pyautogui.write(text)
                        self.gui.assistant_speaks(f"Typed: {text}")
                elif intent == "open application":
                    self.gui.assistant_speaks("What application do you want to open?")
                    app_name = self.listen()
                    if app_name:
                        try:
                            subprocess.Popen(app_name)
                            self.gui.assistant_speaks(f"Opening {app_name}, {self.gui.config.user_preferences['name']}.")
                        except Exception as e:
                            self.gui.assistant_speaks(f"Could not open {app_name}. Please check the application name.")
                            log_action(f"Error opening application: {e}", "ERROR")
                elif intent == "close application":
                    self.gui.assistant_speaks("What application do you want to close?")
                    app_name = self.listen()
                    if app_name:
                        try:
                            os.system(f"taskkill /im {app_name}.exe")
                            self.gui.assistant_speaks(f"Closing {app_name}, {self.gui.config.user_preferences['name']}.")
                        except Exception as e:
                            self.gui.assistant_speaks(f"Could not close {app_name}. Please check the application name.")
                            log_action(f"Error closing application: {e}", "ERROR")
                elif intent == "open website":
                    self.gui.assistant_speaks("What website do you want to open?")
                    website = self.listen()
                    if website:
                        webbrowser.open(f"https://{website}")
                        self.gui.assistant_speaks(f"Opening {website}, {self.gui.config.user_preferences['name']}.")
                elif intent == "close website":
                    self.gui.assistant_speaks("Closing the browser is not supported directly. Please close it manually.")
                elif intent == "search":
                    self.gui.assistant_speaks("What do you want to search for online?")
                    query = self.listen()
                    if query:
                        webbrowser.open(f"https://www.google.com/search?q={query}")
                        self.gui.assistant_speaks(f"Searching for {query} online.")
                elif intent == "list_files":
                    self.gui.assistant_speaks("Which directory should I list files from?")
                    directory = self.listen()
                    if directory:
                        try:
                            files = os.listdir(directory)
                            if files:
                                self.gui.visualization_manager.show_file_explorer(directory, files)
                                self.gui.assistant_speaks(f"Showing files in {directory}")
                            else:
                                self.gui.assistant_speaks(f"No files found in {directory}")
                        except Exception as e:
                            self.gui.assistant_speaks(f"Could not access {directory}")
                            log_action(f"Directory error: {e}", "ERROR")
                elif intent == "copy_file":
                    self.gui.assistant_speaks("Which file should I copy?")
                    source = self.listen()
                    if source:
                        self.gui.assistant_speaks("Where should I copy it to?")
                        dest = self.listen()
                        if dest:
                            try:
                                self.gui.visualization_manager.show_copy_animation(source, dest)
                                self.gui.assistant_speaks(f"Copied {source} to {dest}")
                            except Exception as e:
                                self.gui.assistant_speaks("Failed to copy file")
                                log_action(f"Copy error: {e}", "ERROR")
                elif intent == "show_visualizations":
                    self.gui.visualization_manager.show_visualizations_menu()
                elif intent == "exit_program":
                    self.gui.assistant_speaks("Goodbye!")
                    self.gui.master.quit()
                else:
                    self.gui.assistant_speaks("I didn't understand that command. Please try again.")
            except Exception as e:
                self.gui.assistant_speaks("Something went wrong with that command.")
                log_action(f"Error executing command: {e}", "ERROR")

    def take_screenshot(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"assistant_screenshot_{timestamp}.png"
            x = self.gui.master.winfo_rootx()
            y = self.gui.master.winfo_rooty()
            width = self.gui.master.winfo_width()
            height = self.gui.master.winfo_height()
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            screenshot.save(filename)
            self.gui.assistant_speaks(f"Screenshot saved as {filename}")
        except Exception as e:
            self.gui.assistant_speaks("Failed to take screenshot")
            log_action(f"Screenshot error: {e}", "ERROR")

    def listen_and_process(self):
        command = self.listen()
        if command:
            self.gui.master.after(0, self.gui.user_says, command)
            self.gui.master.after(0, self.execute_command, command)
        self.gui.listening = False
        self.gui.master.after(0, lambda: self.gui.listen_btn.config(text="🎤 Listen"))
