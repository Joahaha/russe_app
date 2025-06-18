from get_word_pair import get_word_pair
import random


def write_word(difficulty):

    mot = get_word_pair()
    print(mot[0])
    if difficulty == 'facile':
        print(f"Indice : {melanger_lettres(mot[1])}")
    reponse = input("Ecrit la traduction en français: ")
    if reponse.lower() == mot[1].lower():
        print("Bravo, c'est la bonne réponse !")
        return True
    else:
        print(f"Non, la bonne réponse était : {mot[1]}")
        return False
    
def melanger_lettres(mot):
    lettres = list(mot)
    random.shuffle(lettres)
    return ''.join(lettres)