import tkinter as tk

class ModeControls(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.label = tk.Label(self, text="Mode :")
        self.btn_quiz = tk.Button(self, text="Quiz", 
                                command=self.controller.set_mode_quiz)
        self.btn_flash = tk.Button(self, text="Flashcard", 
                                 command=self.controller.set_mode_flashcard)
        self.pack_components()
    
    def pack_components(self):
        self.label.pack(side=tk.LEFT, padx=(15, 0))
        self.btn_quiz.pack(side=tk.LEFT, padx=2)
        self.btn_flash.pack(side=tk.LEFT, padx=2)
