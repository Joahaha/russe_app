import tkinter as tk

class BaseWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style_components()
    
    def style_components(self):
        self.option_add('*Font', 'Arial 12')
        self.configure(padx=10, pady=10)
    
    def create_new_window(self, window_class):
        self.destroy()
        new_window = window_class()
        new_window.mainloop()
