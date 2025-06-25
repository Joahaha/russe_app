import tkinter as tk

class MainContent(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.pack(pady=15)
        self.create_components()
    
    def create_components(self):
        self.label_word = tk.Label(self, font=("Arial", 16, "bold"))
        self.entry = tk.Entry(self, font=("Arial", 14))
        self.label_score = tk.Label(self, text="Score : 0/0")
        self.label_result = tk.Label(self, font=("Arial", 12))
        
        self.label_word.pack(pady=15)
        self.entry.pack(pady=5)
        self.label_score.pack(pady=10)
        self.label_result.pack(pady=5)
    
    def show_result(self, text, color):
        self.label_result.config(text=text, fg=color)
