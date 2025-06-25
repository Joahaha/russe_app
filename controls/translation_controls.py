import tkinter as tk

class TranslationControls(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.label = tk.Label(self, text="Sens :")
        self.btn_russe_fr = tk.Button(self, text="Russe → Français", 
                                    command=self.controller.set_russe_fr)
        self.btn_fr_russe = tk.Button(self, text="Français → Russe", 
                                    command=self.controller.set_fr_russe)
        
        self.pack_components()
    
    def pack_components(self):
        self.label.pack(side=tk.LEFT)
        self.btn_russe_fr.pack(side=tk.LEFT, padx=2)
        self.btn_fr_russe.pack(side=tk.LEFT, padx=2)
