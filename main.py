from engine.graphique_russe import TraductionGame
import tkinter as tk

def main():
    root = tk.Tk()
    game = TraductionGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
