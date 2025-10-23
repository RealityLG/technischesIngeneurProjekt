import sqlite3
from typing import Optional, List, Dict
# Projektlogik, Methodenplanung und GUI-/Datenbankstruktur stammen vollständig vom Autor; 
# GitHub Copilot / ChatGPT wurde nur teils für Python-Syntax und Bibliotheksdetails genutzt.

"""
database.py
Datenbankfunktionen für Parkplatzverwaltungssystem
@author: Vincent Gentz
Matrikelnummer:
Datum: 22.10.2025"""
DB_PATH = 'database.db'
# Initialisierung der Datenbank und Tabelle 'Personen' falls nicht vorhanden
def initialise_db(path: str = DB_PATH):
    with sqlite3.connect(path) as conn:
        cur = conn.cursor()
        # Tabelle wird mit SQL erstellt
        cur.execute('''
            CREATE TABLE IF NOT EXISTS personen (
                uid TEXT PRIMARY KEY,
                vorname TEXT NOT NULL,
                nachname TEXT NOT NULL,
                parkplatznummer TEXT NOT NULL,
                belegt INTEGER DEFAULT 0,
                eingecheckt INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        print("Datenbank initialisiert.")
 # Datenbank wird initialisiert, erstellt Tabelle falls nicht vorhanden
initialise_db()

"""add_person(...) fügt neue Person der Datenbank hinzu
 uid: Chip UID für Individuum
 Vor-/Nachname: Name der Person
 parkplatznummer: Zugewiesene Parkplatznummer"""

def add_person(uid: str, vorname: str, nachname: str, parkplatznummer: str, path: Optional[str] = None) -> str:
    # Datenbank wird als Variable geöffnet
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor() # für SQL Befehle
        try:
            # Einfügen der Person
            cur.execute('INSERT INTO personen (uid, vorname, nachname, parkplatznummer) VALUES (?, ?, ?, ?)', 
                       (uid, vorname, nachname, parkplatznummer))
            print(f"Person {vorname} {nachname} mit UID {uid} wurde hinzugefügt.")
            return uid
        except sqlite3.Error as e:
            print(f"Fehler beim Hinzufügen der Person: {e}")
            return ""

"""delete_person(...) löscht eine Person aus der Datenbank anhand der UID
   uid: Chip UID der zu löschenden Person"""

def delete_person(uid: str, path: Optional[str] = None) -> int:
    # Datenbank wird als Variable geöffnet
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor() # für SQL Befehle
        try:
            # Löschen der Person
            cur.execute('DELETE FROM personen WHERE uid = ?', (uid,))
            print(f"Person mit UID {uid} wurde gelöscht.")
            return cur.rowcount
        except sqlite3.Error as e:
            print(f"Fehler beim Löschen der Person: {e}")
            return 0

"""show_all_personen() gibt alle Personen in der Datenbank zurück."""

def show_all_personen() -> List[Dict]:
    # Datenbank wird als Variable geöffnet
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor() # für SQL Befehle
        cur.execute('SELECT uid, vorname, nachname, parkplatznummer, belegt, eingecheckt FROM personen') # Alle Personen abfragen
        rows = cur.fetchall()
        # Ergebnis in Liste von Dictionaries umwandeln
        return [
            {
                'uid': row[0],
                'vorname': row[1],
                'nachname': row[2],
                'parkplatznummer': row[3],
                'belegt': row[4],
                'eingecheckt': row[5]
            }
            for row in rows
        ]

"""update_eingecheckt(...) ändert eingecheckt-Status einer Person anhand der UID"""

def update_eingecheckt(uid: str, path: Optional[str] = None) -> int:
    # Datenbank wird als Variable geöffnet
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor() # für SQL Befehle
        try:
            # Aktuellen Status abfragen
            cur.execute('SELECT eingecheckt FROM personen WHERE uid = ?', (uid,))
            result = cur.fetchone()
            
            if result is None:
                print(f"UID {uid} nicht in Datenbank gefunden.")
                return 0
            
            # Status umkehren (0 -> 1 oder 1 -> 0)
            neuer_status = 1 if result[0] == 0 else 0
            
            # Status aktualisieren
            cur.execute('UPDATE personen SET eingecheckt = ? WHERE uid = ?', (neuer_status, uid))
            print(f"UID {uid}: eingecheckt wurde von {result[0]} auf {neuer_status} geändert.")
            return cur.rowcount
            
        except sqlite3.Error as e:
            print(f"Fehler beim Aktualisieren von eingecheckt: {e}")
            return 0

"""update_belegt(...) aktualisiert das belegt-Feld für eine Person anhand der UID."""

def update_belegt(uid: str, belegt: int, path: Optional[str] = None) -> int:
    # Datenbank wird als Variable geöffnet
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor() # für SQL Befehle
        try:
            # belegt-Feld aktualisieren
            cur.execute('UPDATE personen SET belegt = ? WHERE uid = ?', (belegt, uid))
            print(f"UID {uid}: belegt wurde auf {belegt} gesetzt.")
            return cur.rowcount
        except sqlite3.Error as e:
            print(f"Fehler beim Aktualisieren von belegt: {e}")
            return 0

"""check(...) überprüft, ob ein Parkplatz belegt ist anhand der Parkplatznummer."""

def check(parkplatznummer: str) -> bool:
    # Datenbank wird als Variable geöffnet
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor() # für SQL Befehle
        cur.execute('SELECT belegt FROM personen WHERE parkplatznummer = ?', (parkplatznummer,)) # Belegt-Status abfragen
        result = cur.fetchone()
        # Ergebnis zurückgeben
        if result:
            return result[0] == 1
        return False