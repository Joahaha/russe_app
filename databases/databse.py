import sqlite3
import csv

def init_vocab_db(db_path='vocabulaire.db', csv_path='vocabulaire.csv'):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Création de la table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS vocabulaire(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            russe TEXT,
            francais TEXT
        )
    ''')
    # Import du CSV
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute('INSERT INTO vocabulaire (russe, francais) VALUES (?, ?)', (row['russe'], row['francais']))

    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_vocab_db()
    
    print("Base de données initialisée avec succès.")
