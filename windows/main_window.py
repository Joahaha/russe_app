import tkinter as tk
from tkinter import messagebox
from engine.get_word_pair import get_word_pair
from controls.translation_controls import TranslationControls
from controls.mode_controls import ModeControls
from controls.main_content import MainContent
from controls.game_controls import GameControls

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jeu de traduction russe ↔ français")
        self.game_state = {
            'score': 0,
            'total': 0,
            'inverse': False,
            'flashcard_mode': False,
            'current_pair': '',
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
        self.translation_controls.pack(side=tk.LEFT)
        self.mode_controls = ModeControls(self.top_frame, self)
        self.mode_controls.pack(side=tk.LEFT)
        
        self.main_content = MainContent(self)
        self.game_controls = GameControls(self)

    def bind_shortcuts(self):
        self.bind('<Return>', self.next_word_or_check)
        self.bind('<Escape>', self.quitter)
        # Pour Tab, il faudrait une logique pour alterner quiz/flashcard
        # self.bind('<Tab>', self.toggle_mode)

    def reset_score(self):
        self.game_state.update({'score': 0, 'total': 0})
        self.main_content.label_score.config(text="Score : 0/0")

    def update_score_display(self):
        self.main_content.label_score.config(
            text=f"Score : {self.game_state['score']}/{self.game_state['total']}"
        )

    def next_word_or_check(self, event=None):
        if self.is_answered():
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
        hint = (pair[0] if self.game_state['inverse'] else pair[1])[:2] + "..."
        self.main_content.show_result(f"Indice : {hint}", "blue")
        self.game_controls.btn_hint.config(state=tk.DISABLED)

    def show_translation(self):
        pair = self.game_state['current_pair']
        translation = pair[0] if self.game_state['inverse'] else pair[1]
        self.main_content.show_result(f"Traduction : {translation}", "blue")

    def next_word(self):
        self.game_state['current_pair'] = get_word_pair()
        self.game_state['answered'] = False
        
        pair = self.game_state['current_pair']
        word_to_show = pair[1] if self.game_state['inverse'] else pair[0]
        
        self.main_content.label_word.config(text=word_to_show)
        self.main_content.entry.delete(0, tk.END)
        self.main_content.show_result("", "black")
        
        self.update_score_display()
        self.game_controls.update_buttons(self.is_flashcard_mode(), self.game_state['answered'])

    def set_russe_fr(self):
        self.game_state['inverse'] = False
        self.set_current_pair(get_word_pair())

    def set_fr_russe(self):
        self.game_state['inverse'] = True
        self.set_current_pair(get_word_pair())

    def set_mode_quiz(self):
        self.reset_score()
        self.set_quiz()
        self.game_controls.update_buttons(self.is_flashcard_mode(), self.is_answered())
    
    def set_quiz(self):
        self.game_state['flashcard_mode'] = False

    def set_flashcard(self):
        self.game_state['flashcard_mode'] = True

    def is_flashcard_mode(self):
        return self.game_state['flashcard_mode']
    
    def is_answered(self):
        return self.game_state['answered']
    
    def set_current_pair(self, pair):
        self.game_state['current_pair'] = pair
        self.main_content.label_word.config(text=pair[0] if not self.game_state['inverse'] else pair[1])
        self.main_content.entry.delete(0, tk.END)
        self.main_content.show_result("", "black")

    def set_mode_flashcard(self):
        self.set_flashcard()
        self.game_controls.update_buttons(self.is_flashcard_mode(), self.is_answered())

    def quitter(self, event=None):
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter le jeu ?"):
            self.destroy()
