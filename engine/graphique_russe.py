import tkinter as tk
from tkinter import messagebox
from engine.get_word_pair import get_word_pair
from random import shuffle

class TraductionGame:
    def __init__(self, master):
        self.master = master
        master.title("Jeu de traduction russe ↔ français")

        self.score = 0
        self.total = 0
        self.inverse = False
        self.flashcard_mode = False
        self.current_pair = None
        self.answered = False

        self.frame_top = tk.Frame(master)
        self.frame_top.pack(pady=5)

        self.label_choix = tk.Label(self.frame_top, text="Sens :")
        self.label_choix.pack(side=tk.LEFT)

        self.btn_russe_fr = tk.Button(self.frame_top, text="Russe → Français", command=self.set_russe_fr)
        self.btn_russe_fr.pack(side=tk.LEFT, padx=2)

        self.btn_fr_russe = tk.Button(self.frame_top, text="Français → Russe", command=self.set_fr_russe)
        self.btn_fr_russe.pack(side=tk.LEFT, padx=2)

        self.label_mode = tk.Label(self.frame_top, text="Mode :")
        self.label_mode.pack(side=tk.LEFT, padx=(15,0))

        self.btn_mode_quiz = tk.Button(self.frame_top, text="Quiz", command=self.set_mode_quiz)
        self.btn_mode_quiz.pack(side=tk.LEFT, padx=2)

        self.btn_mode_flash = tk.Button(self.frame_top, text="Flashcard", command=self.set_mode_flashcard)
        self.btn_mode_flash.pack(side=tk.LEFT, padx=2)

        self.btn_quit = tk.Button(self.frame_top, text="Quitter", command=master.quit, fg="red")
        self.btn_quit.pack(side=tk.LEFT, padx=10)

        self.label_word = tk.Label(master, text="", font=("Arial", 16, "bold"))
        self.label_word.pack(pady=15)

        self.entry = tk.Entry(master, font=("Arial", 14))
        self.entry.pack(pady=5)
        self.entry.bind('<Return>', self.next_word_or_check)
        self.entry.bind('<Escape>', self.quitter)  
        self.entry.bind('<Tab>', self.change_mode)         


        self.btn_valider = tk.Button(master, text="Valider", command=self.check_answer)
        self.btn_valider.pack(pady=5)

        self.btn_hint = tk.Button(master, text="Indice", command=self.show_hint)
        self.btn_hint.pack(pady=5)

        self.btn_show = tk.Button(master, text="Voir la traduction", command=self.show_translation)
        self.btn_next_flash = tk.Button(master, text="Mot suivant", command=self.next_word)

        self.label_score = tk.Label(master, text="Score : 0/0")
        self.label_score.pack(pady=10)

        self.label_result = tk.Label(master, text="", font=("Arial", 12))
        self.label_result.pack(pady=5)

        self.btn_next = tk.Button(master, text="Mot suivant", command=self.next_word)
        self.btn_next.pack(pady=5)

        self.set_mode_quiz()  

    def confirmer_et_reset(self, action):
        if self.total > 0:
            confirmation = messagebox.askyesno(
                "Confirmation",
                "Changer de mode ou de langue va réinitialiser le score. Continuer ?"
            )
            if not confirmation:
                return False
            self.score = 0
            self.total = 0
            self.label_score.config(text="Score : 0/0")
        action()
        return True

    def set_russe_fr(self):
        def action():
            self.inverse = False
            self.next_word()
        self.confirmer_et_reset(action)

    def set_fr_russe(self):
        def action():
            self.inverse = True
            self.next_word()
        self.confirmer_et_reset(action)

    def set_mode_quiz(self):
        def action():
            self.flashcard_mode = False
            self.btn_mode_quiz.config(relief=tk.SUNKEN)
            self.btn_mode_flash.config(relief=tk.RAISED)
            self.entry.pack(pady=5)
            self.btn_valider.pack(pady=5)
            self.btn_hint.pack(pady=5)
            self.btn_next.pack(pady=5)
            self.btn_show.pack_forget()
            self.btn_next_flash.pack_forget()
            self.label_score.pack(pady=10)  
            self.next_word()
        self.confirmer_et_reset(action)

    def set_mode_flashcard(self):
        def action():
            self.flashcard_mode = True
            self.btn_mode_flash.config(relief=tk.SUNKEN)
            self.btn_mode_quiz.config(relief=tk.RAISED)
            self.entry.pack_forget()
            self.btn_valider.pack_forget()
            self.btn_next.pack_forget()
            self.btn_show.pack(pady=5)
            self.btn_next_flash.pack(pady=5)
            self.label_score.pack_forget()  
            self.btn_hint.pack_forget()
            self.next_word()
        self.confirmer_et_reset(action)

    def change_mode(self, event):
        if self.flashcard_mode:
            self.set_mode_quiz()
        else:
            self.set_mode_flashcard()
        event.widget.focus_set()
        print("Mode changé avec Tab")
        return "break"  

    #  Logique du jeu 
    def next_word(self):
        self.current_pair = get_word_pair()
        mot_a_traduire = self.current_pair[1] if self.inverse else self.current_pair[0]
        self.label_word.config(text=mot_a_traduire)
        self.label_result.config(text="")
        if self.flashcard_mode:
            self.btn_show.config(state=tk.NORMAL)
            self.btn_next_flash.config(state=tk.DISABLED)
        else:
            self.entry.delete(0, tk.END)
            self.btn_valider.config(state=tk.NORMAL)
            self.btn_next.config(state=tk.DISABLED)
            self.entry.focus_set()

    def check_answer(self, event=None):
        user_input = self.entry.get().strip().lower()
        bonne_reponse = self.current_pair[0] if self.inverse else self.current_pair[1]
        if user_input == bonne_reponse.lower():
            self.score += 1
            self.label_result.config(text="✅ Bonne réponse !", fg="green")
        else:
            self.label_result.config(
                text=f"❌ Mauvaise réponse. La bonne réponse était : {bonne_reponse}",
                fg="red"
            )
        self.total += 1
        self.label_score.config(text=f"Score : {self.score}/{self.total}")
        self.btn_valider.config(state=tk.DISABLED)
        self.answered = True
        self.btn_next.config(state=tk.NORMAL)

    def next_word_or_check(self, event):
        if self.answered:
            self.next_word()
            self.answered = False
        else:
            self.check_answer(event)

    def quitter(self, event=None):
        self.master.quit()

    def show_translation(self):
        bonne_reponse = self.current_pair[0] if self.inverse else self.current_pair[1]
        self.label_result.config(text=f"Traduction : {bonne_reponse}", fg="blue")
        self.btn_show.config(state=tk.DISABLED)
        self.btn_next_flash.config(state=tk.NORMAL)

    def show_hint(self):
        if not self.flashcard_mode:
            mot_a_traduire = self.current_pair[0] if self.inverse else self.current_pair[1]
            hint = ''.join(sorted(mot_a_traduire))
            self.label_result.config(text=f"Indice : {hint}", fg="orange")
            

