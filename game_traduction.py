from write_word import write_word

def game_traduction():
    difficulty = input("Choisis une difficulté (facile, moyen, difficile) : ").strip().lower()
    if difficulty not in ['facile', 'moyen', 'difficile']:
        print("Difficulté non reconnue. Utilisation de la difficulté par défaut : facile.")
        difficulty = 'facile'
    score = 0
    while True:
        if write_word(difficulty):
            score += 1
            if difficulty == 'facile'and score == 5:
                difficulty = 'moyen'
                print("Bravo ! Tu as atteint le niveau moyen.")
        else:
            print(f"Ton score final est : {score}")
            break

if __name__ == "__main__":
    game_traduction()