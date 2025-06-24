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
            'current_pair':'',
            'answered': False
        }
        
        self.create_widgets()
        self.set_current_pair(get_word_pair())
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
        self.game_state['total'] += 1
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
        self.game_controls.btn_valider.config(text="Mot suivant", command=self.next_word)
        self.game_state['answered'] = True

    def show_hint(self):
        pair = self.game_state['current_pair']
        if self.game_state['inverse']:
            hint = pair[0]
        else:
            hint = pair[1]
        hint = hint[:2] + "..."  # Show first two letters as a hint
        self.main_content.show_result(f"Indice : {hint}", "blue")
        self.game_controls.btn_hint.config(state=tk.DISABLED)

        pass

    def show_translation(self):
        pass

    def next_word(self):
        self.game_state['current_pair'] = get_word_pair()
        self.game_state['answered'] = False
        
        pair = self.game_state['current_pair']
        if self.game_state['inverse']:
            word_to_show = pair[1]
        else:
            word_to_show = pair[0]
        
        self.main_content.label_word.config(text=word_to_show)
        self.main_content.entry.delete(0, tk.END)
        self.main_content.show_result("", "black")
        
        self.update_score_display()
        self.game_controls.update_buttons(self.is_flashcard_mode(), self.game_state['answered'])

    def set_russe_fr(self):
        pass

    def set_fr_russe(self):
        pass

    def set_mode_quiz(self):
        self.reset_score()
        self.game_controls.btn_show.place_forget()
        self.set_quiz()
        self.game_controls.update_buttons(self.is_flashcard_mode(), self.is_answered())
    
        
    
    def set_flashcard(self):
        self.game_state['flashcard_mode'] = True

    def set_quiz(self):
        self.game_state['flashcard_mode'] = False

    def is_flashcard_mode(self):
        print("Flashcard mode:", self.game_state['flashcard_mode'])
        return self.game_state['flashcard_mode']
    
    def is_answered(self):
        return self.game_state['answered']
    
    def set_current_pair(self, pair):
        self.game_state['current_pair'] = pair
        self.main_content.label_word.config(text=pair[0] if not self.game_state['inverse'] else pair[1])
        self.main_content.entry.delete(0, tk.END)
        self.main_content.show_result("", "black")

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
        
        self.btn_valider.pack(pady=5)
        self.btn_hint.pack(pady=5)
        self.btn_show.pack(pady=5)
    
    def update_buttons(self,flashcard_mode,answered):
        if flashcard_mode:
            self.btn_hint.place_forget()    
            self.btn_show.pack(pady=5)
            print("Flashcard mode")

        else:
            print("Quiz mode")
            if answered:
                self.btn_valider.config(text="Mot suivant", command=self.controller.next_word)
            else:
                self.btn_valider.config(text="Valider", command=self.controller.check_answer)
            self.btn_valider.config(state=tk.NORMAL)
            self.btn_hint.config(state=tk.NORMAL)
            self.btn_show.pack_forget()
        

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
