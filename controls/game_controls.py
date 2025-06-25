import tkinter as tk

class GameControls(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.pack(pady=5)
        self.create_buttons()
    
    def create_buttons(self):
        self.btn_valider = tk.Button(self, text="Valider", 
                                   command=self.controller.check_answer)
        self.btn_hint = tk.Button(self, text="Indice", 
                                command=self.controller.show_hint)
        self.btn_show = tk.Button(self, text="Voir la traduction", 
                                command=self.controller.show_translation)
        
        self.btn_valider.pack(pady=5)
        self.btn_hint.pack(pady=5)
        self.btn_show.pack(pady=5)
    
    def update_buttons(self, flashcard_mode, answered):
        # Masquer tous les boutons d'abord
        self.btn_valider.pack_forget()
        self.btn_hint.pack_forget()
        self.btn_show.pack_forget()
        # Afficher selon le mode
        if flashcard_mode:
            self.btn_show.pack(pady=5)
        else:
            self.btn_valider.pack(pady=5)
            self.btn_hint.pack(pady=5)
            if answered:
                self.btn_valider.config(text="Mot suivant", command=self.controller.next_word)
            else:
                self.btn_valider.config(text="Valider", command=self.controller.check_answer)
            self.btn_valider.config(state=tk.NORMAL)
            self.btn_hint.config(state=tk.NORMAL)
