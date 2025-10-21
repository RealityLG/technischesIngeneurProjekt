# Projektablaufplan (PAP)

Projekt: Technisches Ingenieur Projekt — Zugangskontrolle / Parkplatzverwaltung (Prototyp)
Datum: 2025-10-19
Autor: (Dein Name)

Kurzbeschreibung
-----------------
Dieses Projekt ist ein Prototyp zur Verwaltung von Parkplätzen mit RFID/Scan-Input (Arduino), einer lokalen SQLite-Datenbank und einfachen Benutzeroberflächen (CLI/GUI/Web). Ziel ist ein minimaler, erweiterbarer Stack für Tests und für die spätere Integration in ein größeres System.

Ziele
------
- Lokaler Prototyp: Arduino sendet IDs über Serial; Python empfängt, prüft gegen DB, markiert Belegung.
- Basisdatenmodell in SQLite: `personen` und `entries` (Log).
- Lokale Bedienoberfläche: Tkinter GUI zum Anzeigen/Hinzufügen/Löschen von Personen.
- Optional: kleine Flask API + Web GUI für Browserzugriff.

Meilensteine (high-level)
-------------------------
- M1: Basis DB & CLI (fertig) — 1 Tag
- M2: Serial Receiver & Logging (fertig) — 1 Tag
- M3: Lokale GUI (Tkinter) — 2 Tage
- M4: Web API + Browser UI (optional) — 2 Tage
- M5: Integrationstest, Fehlertests & Dokumentation — 2 Tage

Zeitplan (vorschlag)
--------------------
- Woche 1 (Prototyp): M1, M2
- Woche 2: M3 (GUI-Feinschliff), Basis-Tests
- Woche 3: M4 (Web-Frontend) + Integration

Arbeitspakete (AP)
-------------------

AP-01: Repository & Basisstruktur
- Beschreibung: Ordnerstruktur, README, requirements
- Dauer: 0.5d
- Ergebnis: `python/`, `arduino/`, README.md

AP-02: Datenbank-Modul
- Beschreibung: `database.py` mit Init, add, delete, list, update Funktionen
- Dauer: 0.5d
- Ergebnis: `database.py`, `database.db`

AP-03: Serial Empfänger
- Beschreibung: `serial_receiver.py` verarbeitet Serial-Input, parst IDs, prüft DB, schreibt Logs
- Dauer: 1d
- Ergebnis: Logs, replies an Arduino (AUTH/DENIED)

AP-04: CLI & Tests
- Beschreibung: Kleine CLI für schnelle Tests (add/delete/list)
- Dauer: 0.5d
- Ergebnis: `python/cli.py` (optional)

AP-05: Tkinter GUI (Minimal)
- Beschreibung: GUI zeigt Tabelle, erlaubt Hinzufügen & Löschen (kontextmenü)
- Dauer: 1.5d
- Ergebnis: `gui.py` mit Funktionen: refresh, add-dialog, delete-selection

AP-06: Flask API + Web-Frontend (optional)
- Beschreibung: REST Endpoints + `templates/index.html` + CSS
- Dauer: 2d
- Ergebnis: `web.py`, `templates/`, `static/`

AP-07: Tests & Dokumentation
- Beschreibung: Unit tests für `database.py`, kurze Integrationstests, README Erweiterung
- Dauer: 2d
- Ergebnis: `tests/`, aktualisiertes README

Abhängigkeiten
--------------
- Python 3.10+ (vorhanden), Flask (optional), pyserial (optional), Tkinter (teil der Standardinstallation)

Risiken & Gegenmaßnahmen
-------------------------
- Locking bei SQLite bei vielen gleichzeitigen Schreibern — Gegenmaßnahme: Serialisiere Schreibzugriffe, bei Bedarf DB auf Postgres migrieren.
- Inkonsistente DB-Schema-Versionen — Gegenmaßnahme: einfache Migrationslogik (ALTER TABLE) beim Start.
- Fehlende Pakete auf Zielsystem — Gegenmaßnahme: `requirements.txt` pflegen.

Akzeptanzkriterien
-------------------
- DB initialisiert und enthält Tabelle `personen` und `entries`.
- GUI zeigt aktuell gespeicherte Personen und erlaubt Hinzufügen & Löschen.
- Serial-Receiver kann eine ID lesen, in DB prüfen und AUTH/DENIED senden.

Deliverables
------------
- `database.py`, `database.db`
- `python/serial_receiver.py`
- `gui.py`
- `web.py`, `templates/index.html` (optional)
- `PAP.md` (dieses Dokument)

Nächste Schritte (konkret für dich)
---------------------------------
1. Prüfe das aktuelle `database.py` und mache Backup von `database.db`.
2. Implementiere und teste Kontextmenü + Löschfunktion in der GUI (wir haben bereits Codebeispiele).
3. Implementiere Hinzufügen per Dialog (wir haben das Beispielcode geliefert).
4. Optional: Erstelle Flask-API und Web-Frontend für Remotezugriff.

Kontakt / Zuständigkeiten
-------------------------
Owner: Du (Vincent) — Entwicklungsentscheidungen
Reviewer: (optional) Kolleg*in
