import sqlite3
import random
from engine.get_word_pair import get_word_pair

mot = get_word_pair()

print(f"Si tu veux un mot en russe et sa traduction en français écrit 1, si tu veux l'inverse écrit 2.")
choix = input("Ton choix (1 ou 2) : ")
if choix == '2':
    mot = (mot[1], mot[0])  

print(f"{mot[0]}")
input("Appuie sur Entrée pour voir la traduction…")
print(f"Traduction : {mot[1]}")


