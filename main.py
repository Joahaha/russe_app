import tkinter as tk
from windows.main_window import MainWindow
# from auth_window import AuthWindow  

def launch_game(username=None):
    """Lance la fenêtre principale du jeu, éventuellement avec un utilisateur."""
    root = tk.Tk()
    app = MainWindow()
    root.mainloop()

# def launch_auth():
#     root = tk.Tk()
#     app = AuthWindow(root, on_success=launch_game)
#     root.mainloop()

if __name__ == "__main__":
    # launch_auth()
    launch_game()
