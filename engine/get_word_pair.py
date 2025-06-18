import sqlite3
import random


def get_word_pair():
    conn = sqlite3.connect('databases/vocabulaire.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())

    cur.execute('SELECT russe, francais FROM vocabulaire')
    mots = cur.fetchall()
    mot = random.choice(mots)
    conn.close()
    return mot

