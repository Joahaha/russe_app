import tkinter as tk
from tkinter import messagebox
from engine.get_word_pair import get_word_pair

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

class AuthWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.title("Authentification")
        # Ajouter les composants d'authentification ici

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.title("Jeu de traduction russe ↔ français")
        self.game_state = {
            'score': 0,
            'total': 0,
            'inverse': False,
            'flashcard_mode': False,
            'current_pair': None,
            'answered': False
        }
        
        self.create_widgets()
        self.bind_shortcuts()
        self.set_mode_quiz()

    def create_widgets(self):
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(pady=5)
        
        self.translation_controls = TranslationControls(self.top_frame, self)
        self.mode_controls = ModeControls(self.top_frame, self)
        
        self.main_content = MainContent(self)
        
        self.game_controls = GameControls(self)

    def bind_shortcuts(self):
        self.bind('<Return>', self.next_word_or_check)
        self.bind('<Escape>', self.quitter)
        self.bind('<Tab>', self.set_other_mode )

    def reset_score(self):
        self.game_state.update({'score': 0, 'total': 0})
        self.main_content.label_score.config(text="Score : 0/0")

    def update_score_display(self):
        self.main_content.label_score.config(
            text=f"Score : {self.game_state['score']}/{self.game_state['total']}"
        )

    def next_word_or_check(self, event=None):
        if self.game_state['answered']:
            self.next_word()
            self.game_state['answered'] = False
        else:
            self.check_answer()

    def check_answer(self):
        user_input = self.main_content.entry.get().strip().lower()
        correct_answer = self.get_correct_answer()
        
        if user_input == correct_answer.lower():
            self.handle_correct_answer()
        else:
            self.handle_wrong_answer(correct_answer)
        
        self.update_score_display()
        self.toggle_answer_controls()

    def get_correct_answer(self):
        pair = self.game_state['current_pair']
        return pair[0] if self.game_state['inverse'] else pair[1]

    def handle_correct_answer(self):
        self.game_state['score'] += 1
        self.main_content.show_result("✅ Bonne réponse !", "green")

    def handle_wrong_answer(self, correct_answer):
        self.main_content.show_result(
            f"❌ Mauvaise réponse. La bonne réponse était : {correct_answer}", 
            "red"
        )

    def toggle_answer_controls(self):
        self.main_content.btn_valider.config(state=tk.DISABLED)
        self.main_content.btn_next.config(state=tk.NORMAL)
        self.game_state['answered'] = True

    def show_hint(self):
        pass

    def show_translation(self):
        pass

    def next_word(self):
        pass

    def set_russe_fr(self):
        pass

    def set_fr_russe(self):
        pass

    def set_mode_quiz(self):
        pass

    def set_mode_flashcard(self):
        pass

    def quitter(self, event=None):
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter le jeu ?"):
            self.destroy()

    def set_other_mode(self, mode):
        if mode == 'quiz':
            self.set_mode_quiz()
        elif mode == 'flashcard':
            self.set_mode_flashcard()
        
    
class TranslationControls(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.label = tk.Label(self, text="Sens :")
        self.btn_russe_fr = tk.Button(self, text="Russe → Français", 
                                    command=lambda: controller.set_russe_fr())
        self.btn_fr_russe = tk.Button(self, text="Français → Russe", 
                                    command=lambda: controller.set_fr_russe())
        
        self.pack_components()
    
    def pack_components(self):
        self.label.pack(side=tk.LEFT)
        self.btn_russe_fr.pack(side=tk.LEFT, padx=2)
        self.btn_fr_russe.pack(side=tk.LEFT, padx=2)

class ModeControls(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.label = tk.Label(self, text="Mode :")
        self.btn_quiz = tk.Button(self, text="Quiz", 
                                command=lambda: controller.set_mode_quiz())
        self.btn_flash = tk.Button(self, text="Flashcard", 
                                 command=lambda: controller.set_mode_flashcard())        
        self.pack_components()
    
    def pack_components(self):
        self.label.pack(side=tk.LEFT, padx=(15, 0))
        self.btn_quiz.pack(side=tk.LEFT, padx=2)
        self.btn_flash.pack(side=tk.LEFT, padx=2)

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
        self.btn_next = tk.Button(self, text="Mot suivant", 
                                command=self.controller.next_word)
        
        self.btn_valider.pack(pady=5)
        self.btn_hint.pack(pady=5)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
