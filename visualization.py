import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import cm
from wordcloud import WordCloud
import numpy as np
import random

class VisualizationManager:
    def __init__(self, gui):
        self.gui = gui

    def show_visualizations_menu(self):
        menu = tk.Menu(self.gui.master, tearoff=0)
        menu.add_command(label="Command History Chart", command=self.show_command_history_chart)
        menu.add_command(label="Command Word Cloud", command=self.show_command_wordcloud)
        menu.add_separator()
        menu.add_command(label="System Performance", command=self.show_system_performance)
        menu.add_separator()
        menu.add_command(label="Conversation Timeline", command=self.show_conversation_timeline)
        menu.add_command(label="Sentiment Analysis", command=self.show_sentiment_analysis)
        try:
            menu.tk_popup(self.gui.master.winfo_pointerx(), self.gui.master.winfo_pointery())
        finally:
            menu.grab_release()

    def show_command_history_chart(self):
        if not self.gui.config.action_history:
            messagebox.showinfo("Info", "No command history available yet.")
            return
        vis_window = tk.Toplevel(self.gui.master)
        vis_window.title("Command History Chart")
        vis_window.geometry("600x400")
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        command_counts = {}
        for cmd in self.gui.config.action_history:
            command_counts[cmd] = command_counts.get(cmd, 0) + 1
        commands = list(command_counts.keys())
        counts = list(command_counts.values())
        colors = cm.viridis(np.linspace(0, 1, len(commands)))
        bars = ax.bar(commands, counts, color=colors)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height, f'{int(height)}', ha='center', va='bottom')
        ax.set_title('Most Used Commands', pad=20)
        ax.set_ylabel('Frequency')
        ax.set_xlabel('Commands')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=vis_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        ttk.Button(vis_window, text="Close", command=vis_window.destroy).pack(pady=10)

    def show_command_wordcloud(self):
        if not self.gui.config.action_history:
            messagebox.showinfo("Info", "No command history available yet.")
            return
        vis_window = tk.Toplevel(self.gui.master)
        vis_window.title("Command Word Cloud")
        vis_window.geometry("600x400")
        text = ' '.join(self.gui.config.action_history)
        wordcloud = WordCloud(width=500, height=300, background_color='white', colormap='viridis').generate(text)
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Command Word Cloud', pad=20)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=vis_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        ttk.Button(vis_window, text="Close", command=vis_window.destroy).pack(pady=10)

    def show_system_performance(self):
        vis_window = tk.Toplevel(self.gui.master)
        vis_window.title("System Performance")
        vis_window.geometry("800x600")
        fig = plt.figure(figsize=(8, 6), dpi=100)
        ax1 = fig.add_subplot(221)
        cpu_usage = [random.randint(10, 80) for _ in range(10)]
        ax1.plot(cpu_usage, marker='o', color='tab:blue')
        ax1.set_title('CPU Usage (%)')
        ax1.set_ylim(0, 100)
        ax2 = fig.add_subplot(222)
        mem_usage = [random.randint(30, 90) for _ in range(10)]
        ax2.plot(mem_usage, marker='o', color='tab:orange')
        ax2.set_title('Memory Usage (%)')
        ax2.set_ylim(0, 100)
        ax3 = fig.add_subplot(223)
        commands = ['Open', 'Search', 'Time', 'File', 'Other']
        times = [random.uniform(0.1, 2.0) for _ in range(5)]
        ax3.bar(commands, times, color='tab:green')
        ax3.set_title('Average Response Times (s)')
        ax4 = fig.add_subplot(224)
        success_rate = [random.randint(70, 100) for _ in range(5)]
        ax4.bar(commands, success_rate, color='tab:red')
        ax4.set_title('Success Rate (%)')
        ax4.set_ylim(0, 100)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=vis_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        ttk.Button(vis_window, text="Close", command=vis_window.destroy).pack(pady=10)

    def show_conversation_timeline(self):
        vis_window = tk.Toplevel(self.gui.master)
        vis_window.title("Conversation Timeline")
        vis_window.geometry("800x400")
        fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
        events = ['Greeting', 'Command 1', 'Response 1', 'Command 2', 'Response 2', 'Exit']
        times = [0, 1, 2, 3, 4, 5]
        ax.plot(times, [1] * len(times), '-o', color='purple')
        for i, txt in enumerate(events):
            ax.annotate(txt, (times[i], 1), textcoords="offset points", xytext=(0, 10), ha='center')
        ax.set_title('Conversation Timeline')
        ax.set_yticks([])
        ax.set_xlabel('Time (minutes)')
        ax.grid(True, axis='x')
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=vis_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        ttk.Button(vis_window, text="Close", command=vis_window.destroy).pack(pady=10)

    def show_sentiment_analysis(self):
        vis_window = tk.Toplevel(self.gui.master)
        vis_window.title("Sentiment Analysis")
        vis_window.geometry("600x400")
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        sentiments = ['Positive', 'Neutral', 'Negative']
        counts = [65, 25, 10]
        colors = ['#4CAF50', '#FFC107', '#F44336']
        wedges, texts, autotexts = ax.pie(counts, labels=sentiments, colors=colors, autopct='%1.1f%%', startangle=90, explode=(0.1, 0, 0))
        plt.setp(autotexts, size=10, weight="bold")
        ax.set_title('Conversation Sentiment Analysis')
        canvas = FigureCanvasTkAgg(fig, master=vis_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        ttk.Button(vis_window, text="Close", command=vis_window.destroy).pack(pady=10)

    def show_file_explorer(self, directory, files):
        explorer = tk.Toplevel(self.gui.master)
        explorer.title(f"Files in {directory}")
        explorer.geometry("600x400")
        tree = ttk.Treeview(explorer)
        tree["columns"] = ("size", "type", "modified")
        tree.column("#0", width=300, minwidth=100)
        tree.column("size", width=100, minwidth=50)
        tree.column("type", width=100, minwidth=50)
        tree.column("modified", width=150, minwidth=50)
        tree.heading("#0", text="Name")
        tree.heading("size", text="Size")
        tree.heading("type", text="Type")
        tree.heading("modified", text="Modified")
        for file in files:
            path = os.path.join(directory, file)
            size = os.path.getsize(path)
            modified = datetime.fromtimestamp(os.path.getmtime(path))
            file_type = "Folder" if os.path.isdir(path) else "File"
            tree.insert("", tk.END, text=file, values=(size, file_type, modified))
        tree.pack(expand=True, fill=tk.BOTH)
        btn_frame = ttk.Frame(explorer)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Open", command=lambda: self.open_selected_file(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=explorer.destroy).pack(side=tk.RIGHT, padx=5)

    @staticmethod
    def open_selected_file(tree):
        selected = tree.focus()
        if selected:
            file_name = tree.item(selected, "text")
            try:
                os.startfile(file_name)
            except:
                messagebox.showerror("Error", f"Could not open {file_name}")

    def show_copy_animation(self, source, dest):
        progress = tk.Toplevel(self.gui.master)
        progress.title("Copying File")
        progress.geometry("300x100")
        ttk.Label(progress, text=f"Copying {source} to {dest}").pack(pady=5)
        pb = ttk.Progressbar(progress, orient="horizontal", length=200, mode="determinate")
        pb.pack(pady=10)
        pb.start(10)
        def finish_copy():
            pb.stop()
            progress.destroy()
        progress.after(2000, finish_copy)
