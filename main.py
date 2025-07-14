import tkinter as tk
import logging
from gui import VoiceAssistantGUI

# Configure logging
logging.basicConfig(
    filename="assistant.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        gui = VoiceAssistantGUI(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"Application error: {e}")
        raise
