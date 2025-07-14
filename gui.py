import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import threading
import pyttsx3
import spacy
from commands import CommandProcessor
from visualizations import VisualizationManager
from config import Config
from utils import log_action

class VoiceAssistantGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice Assistant")
        self.master.geometry("1000x700")

        self.config = Config()
        self.command_processor = CommandProcessor(self)
        self.visualization_manager = VisualizationManager(self)

        # Initialize GUI components
        self.command_entry = None
        self.text_area = None
        self.listen_btn = None
        self.status_icon = None
        self.status_var = tk.StringVar()
        self.progress_bar = None
        self.theme_var = tk.StringVar()

        # Initialize text-to-speech
        self.engine = self._init_tts_engine()

        # Initialize NLP
        try:
            self.nlp = spacy.load(self.config.user_preferences['spaCy_model'])
        except OSError:
            logging.error("spaCy model not found. Please install it.")
            self.nlp = None

        # State variables
        self.listening = False
        self.expecting_name = True
        self.animation_frames = ["👂", "🗣", "💭", "⌛"]
        self.current_frame = 0

        self.create_widgets()
        self.assistant_speaks("What is your name?")
        threading.Thread(target=self.listen_for_name, daemon=True).start()
        self.animate_assistant()

    def _init_tts_engine(self):
        try:
            engine = pyttsx3.init('sapi5')
            engine.setProperty("rate", self.config.user_preferences['speech_rate'])
            engine.setProperty("volume", 0.9)
            return engine
        except Exception as e:
            logging.error(f"Failed to initialize TTS engine: {e}")
            return None

    def animate_assistant(self):
        if self.listening:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.status_icon.config(text=self.animation_frames[self.current_frame])
        self.master.after(500, self.animate_assistant)

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.master)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        main_frame.config(style='TFrame')

        # Header frame
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 10))

        # Assistant icon and title
        ttk.Label(header_frame, text="🤖", font=('Helvetica', 24)).pack(side='left', padx=(0, 10))
        ttk.Label(header_frame, text="Voice Assistant", font=('Helvetica', 16, 'bold')).pack(side='left', expand=True)
        ttk.Button(header_frame, text="📊 Visualizations", command=self.visualization_manager.show_visualizations_menu
                  ).pack(side='right', padx=(5, 0))

        # Text area
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(expand=True, fill='both')

        self.text_area = scrolledtext.ScrolledText(
            text_frame, wrap=tk.WORD, state='disabled', bg=self.config.text_bg,
            font=('Helvetica', 10), padx=10, pady=10
        )
        self.text_area.pack(expand=True, fill='both')
        for tag, props in self.config.text_tags.items():
            self.text_area.tag_config(tag, **props)

        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill='x', pady=(5, 0))

        self.command_entry = ttk.Entry(input_frame, font=('Helvetica', 10), style='TEntry')
        self.command_entry.pack(side='left', expand=True, fill='x', padx=(0, 5))
        self.command_entry.insert(0, "Type your command here or click the microphone...")
        self.command_entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.command_entry.bind("<FocusOut>", lambda e: self.restore_placeholder())
        self.command_entry.bind("<Return>", lambda e: self.process_text_command())

        # Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(side='left')

        self.listen_btn = ttk.Button(btn_frame, text="🎤 Listen", command=self.toggle_listening, style='TButton')
        self.listen_btn.pack(side='left', padx=(0, 5))

        ttk.Button(btn_frame, text="⚙️ Settings", command=self.show_settings, style='TButton').pack(side='left', padx=(0, 5))
        ttk.Button(btn_frame, text="📷 Screenshot", command=self.command_processor.take_screenshot, style='TButton').pack(side='left', padx=(0, 5))
        ttk.Button(btn_frame, text="❌ Exit", command=self.master.quit, style='TButton').pack(side='left')

        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill='x')

        self.status_icon = ttk.Label(status_frame, text="💤", font=('Helvetica', 12))
        self.status_icon.pack(side='left', padx=(0, 5))
        self.status_var.set("Ready")
        ttk.Label(status_frame, textvariable=self.status_var, font=('Helvetica', 9), style='TLabel').pack(side='left', expand=True, fill='x')
        self.progress_bar = ttk.Progressbar(status_frame, orient='horizontal', mode='determinate', length=100)
        self.progress_bar.pack(side='right', fill='x', expand=True)
        self.progress_bar.pack_forget()

    def clear_placeholder(self):
        if self.command_entry.get() == "Type your command here or click the microphone...":
            self.command_entry.delete(0, tk.END)
            self.command_entry.config(foreground='black')

    def restore_placeholder(self):
        if not self.command_entry.get():
            self.command_entry.insert(0, "Type your command here or click the microphone...")
            self.command_entry.config(foreground='grey')

    def toggle_listening(self):
        if not self.listening:
            self.listening = True
            self.listen_btn.config(text="🔴 Listening...")
            self.status_var.set("Listening...")
            self.progress_bar.pack(side='right', fill='x', expand=True)
            self.progress_bar.start(10)
            threading.Thread(target=self.command_processor.listen_and_process, daemon=True).start()
        else:
            self.listening = False
            self.listen_btn.config(text="🎤 Listen")
            self.status_var.set("Ready")
            self.progress_bar.stop()
            self.progress_bar.pack_forget()

    def show_settings(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("400x300")

        ttk.Label(settings_window, text="Assistant Settings", font=('Helvetica', 12, 'bold')).pack(pady=10)

        theme_frame = ttk.Frame(settings_window)
        theme_frame.pack(pady=10)
        ttk.Label(theme_frame, text="Theme:").pack(side='left', padx=5)
        self.theme_var.set(self.config.user_preferences['theme'])
        ttk.Radiobutton(theme_frame, text="Light", variable=self.theme_var, value='light', command=self.change_theme).pack(side='left', padx=5)
        ttk.Radiobutton(theme_frame, text="Dark", variable=self.theme_var, value='dark', command=self.change_theme).pack(side='left', padx=5)

        voice_frame = ttk.Frame(settings_window)
        voice_frame.pack(pady=10)
        ttk.Label(voice_frame, text="Voice Speed:").pack(side='left', padx=5)
        speed_var = tk.IntVar(value=self.config.user_preferences['speech_rate'])
        ttk.Scale(voice_frame, from_=100, to=200, variable=speed_var, command=lambda v: self.change_voice_speed(int(float(v)))).pack(side='left', padx=5)

        ttk.Button(settings_window, text="Close", command=settings_window.destroy).pack(pady=20)

    def change_theme(self):
        theme = self.theme_var.get()
        self.config.change_theme(theme)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background=self.config.bg_color)
        self.style.configure('TFrame', background=self.config.bg_color)
        self.style.configure('TLabel', background=self.config.bg_color)
        self.text_area.config(bg=self.config.text_bg)
        self.master.config(bg=self.config.bg_color)

    def change_voice_speed(self, speed):
        self.config.user_preferences['speech_rate'] = speed
        if self.engine:
            self.engine.setProperty('rate', speed)

    def assistant_speaks(self, text):
        if not text:
            return
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, f"Assistant: {text}\n", 'assistant')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                logging.error(f"Error in text-to-speech: {e}")
                self.text_area.configure(state='normal')
                self.text_area.insert(tk.END, f"Error: Could not speak text\n", 'error')
                self.text_area.configure(state='disabled')

    def user_says(self, text):
        if not text:
            return
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, f"You: {text}\n", 'user')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)
        self.config.action_history.append(text)

    def process_text_command(self):
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        if command and command != "Type your command here or click the microphone...":
            self.user_says(command)
            self.command_processor.execute_command(command)

    def listen_for_name(self):
        command = self.command_processor.listen()
        if command:
            self.config.user_preferences['name'] = command
            self.assistant_speaks(f"Hello {command}! How can I help you today?")
            self.expecting_name = False
