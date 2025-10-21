import sqlite3
from typing import Optional, List, Dict

DB_PATH = 'database.db'

def init_db(path: str = DB_PATH):
    """Erstellt die Tabelle 'personen', falls sie noch nicht existiert."""
    with sqlite3.connect(path) as conn:
        cur = conn.cursor()
        cur.execute('''
                CREATE TABLE IF NOT EXISTS personen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vorname TEXT NOT NULL,
                nachname TEXT NOT NULL,
                parkplatznummer TEXT NOT NULL,
                belegt INTEGER DEFAULT 0,
                eingecheckt INTEGER DEFAULT 0
            )
        ''')
        print("Datenbank und Tabelle wurden erstellt, falls sie noch nicht existieren.")

init_db()

def add_person(vorname: str, nachname: str, parkplatznummer: str, path: Optional[str] = None) -> int:
    """Fügt eine neue Person zur Datenbank hinzu und gibt ID zurück."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO personen (vorname, nachname, parkplatznummer) VALUES (?, ?, ?)', (vorname, nachname, parkplatznummer))
            return cur.lastrowid
        except sqlite3.Error as e:
            print(f"Fehler beim Hinzufügen der Person: {e}")
            return 0

def delete_person(vorname: str, nachname: str, parkplatznummer: str, path: Optional[str] = None) -> int:
    """Löscht eine Person aus der Datenbank und gibt die Anzahl der gelöschten Zeilen zurück."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM personen WHERE vorname = ? AND nachname = ? AND parkplatznummer = ?', (vorname, nachname, parkplatznummer))
            return cur.rowcount
        except sqlite3.Error as e:
            print(f"Fehler beim Löschen der Person: {e}")
            return 0

def show_all_personen():
    """Gibt alle Personen aus der Datenbank aus."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM personen")
        rows = cur.fetchall()
        if rows:
            print("ID | Vorname | Nachname | Parkplatznummer | Belegt | Eingecheckt")
            print("-" * 70)
            for row in rows:
                print(row)
        else:
            print("Keine Personen in der Datenbank.")

def update_eingecheckt(vorname: str, nachname: str, eingecheckt: int, path: Optional[str] = None) -> int:
    """Aktualisiert das eingecheckt-Feld für eine Person und gibt die Anzahl der aktualisierten Zeilen zurück."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        try:
            cur.execute('UPDATE personen SET eingecheckt = ? WHERE vorname = ? AND nachname = ?', (eingecheckt, vorname, nachname))
            return cur.rowcount
        except sqlite3.Error as e:
            print(f"Fehler beim Aktualisieren von eingecheckt: {e}")
            return 0

def update_belegt(vorname: str, nachname: str, belegt: int, path: Optional[str] = None) -> int:
    """Aktualisiert das belegt-Feld für eine Person und gibt die Anzahl der aktualisierten Zeilen zurück."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        try:
            cur.execute('UPDATE personen SET belegt = ? WHERE vorname = ? AND nachname = ?', (belegt, vorname, nachname))
            return cur.rowcount
        except sqlite3.Error as e:
            print(f"Fehler beim Aktualisieren von belegt: {e}")
            return 0
        
def check(parkplatznummer: str):
    """Überprüft, ob ein Parkplatz belegt ist."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        try:
            cur.execute('SELECT belegt FROM personen WHERE parkplatznummer = ?', (parkplatznummer,))
            if cur.rowcount == 0:
                print("Parkplatznummer nicht gefunden.")
                return None
            result = cur.fetchone()
            return result[0] == 1  # Gibt True zurück, wenn belegt, sonst False
        except sqlite3.Error as e:
            print(f"Fehler beim Überprüfen des Parkplatzes: {e}")
            return None