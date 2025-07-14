import tkinter.ttk as ttk

class Config:
    def __init__(self):
        self.bg_color = "#f0f8ff"
        self.text_bg = "#ffffff"
        self.user_color = "#4169e1"
        self.assistant_color = "#2e8b57"
        self.error_color = "#ff4500"
        
        self.user_preferences = {
            'name': 'User',
            'speech_rate': 150,
            'preferred_language': 'en',
            'spaCy_model': 'en_core_web_sm',
            'theme': 'light'
        }
        
        self.action_history = []
        self.redo_stack = []
        
        self.text_tags = {
            'user': {'foreground': self.user_color, 'font': ('Helvetica', 10, 'bold')},
            'assistant': {'foreground': self.assistant_color, 'font': ('Helvetica', 10, 'bold')},
            'error': {'foreground': self.error_color},
            'system': {'foreground': '#888888'},
            'command': {'foreground': '#8a2be2'}
        }

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background=self.bg_color)
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10), padding=5)
        self.style.configure('TEntry', font=('Helvetica', 10), padding=5)

    def change_theme(self, theme):
        self.user_preferences['theme'] = theme
        if theme == 'dark':
            self.bg_color = "#2d2d2d"
            self.text_bg = "#1e1e1e"
            self.user_color = "#569cd6"
            self.assistant_color = "#4ec9b0"
        else:
            self.bg_color = "#f0f8ff"
            self.text_bg = "#ffffff"
            self.user_color = "#4169e1"
            self.assistant_color = "#2e8b57"
        self.text_tags['user']['foreground'] = self.user_color
        self.text_tags['assistant']['foreground'] = self.assistant_color
