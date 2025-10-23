import serial
import time
from database import update_eingecheckt
# Projektlogik, Methodenplanung und GUI-/Datenbankstruktur stammen vollständig vom Autor; 
# GitHub Copilot / ChatGPT wurde nur teils für Python-Syntax und Bibliotheksdetails genutzt.

"""
serial_listener.py
Skript hört die Schnittestelle zum Arduino ab und aktualisiert die Datenbank.
@author: Vincent Gentz 
Matrikelnummer:
Datum: 22.10.2025"""
# Konfiguration
PORT = 'COM3'
BAUD = 9600

"""listen() wartet auf UID-Nachrichten vom Arduino und aktualisiert die Datenbank."""

def listen():
    # versucht Verbindung aufzubauen
    try:
        print(f"Versuche Verbindung zu {PORT} mit {BAUD} Baud...")
        with serial.Serial(PORT, BAUD, timeout=1) as ser:
            print(f"Serial Listener erfolgreich gestartet auf {PORT}")
            print("Warte auf Arduino-Daten")

            time.sleep(2)  # Arduino Zeit zum Booten geben
            
            while True:
                if ser.in_waiting > 0: # Überprüfen, ob Daten im Puffer sind
                    line = ser.readline().decode('utf-8', errors='ignore').strip() # Zeile lesen und dekodieren
                    
                    if line:
                        print(f"[EMPFANGEN] {line}")
                        
                        # UID-Zeile erkennen: "Karte erkannt! UID: 4C3BE937"
                        if "UID:" in line:
                            # UID extrahieren (alles nach "UID: ")
                            uid_start = line.find("UID:") + 4
                            uid = line[uid_start:].strip().upper()

                            print(f"→ UID erkannt: {uid}")
                            print(f"→ Suche Person in Datenbank...")
                            
                            # Datenbank aktualisieren
                            result = update_eingecheckt(uid)
                            
                            if result > 0:
                                print(f"Eingecheckt-Status für UID {uid} erfolgreich geändert")
                            else:
                                print(f"FEHLER: UID {uid} nicht in Datenbank gefunden!")
                                print(f"Bitte Person mit UID {uid} in GUI hinzufügen")
                
                time.sleep(0.1)  # Kleine Pause zur CPU-Entlastung
                
    except serial.SerialException as e:
        print(f"\nFEHLER beim Öffnen von {PORT}:")
        print(f"   {e}\n")
        print("Überprüfe:")
        print(" Arduino ist angeschlossen (USB-Kabel)")
        print(" COM3 ist der richtige Port (Geräte-Manager prüfen)")
        print(" Arduino IDE Serial Monitor ist GESCHLOSSEN")
        print(" Kein anderes Programm nutzt den Port")
        
    except KeyboardInterrupt:
        print("\n\nSerial Listener beendet (Strg+C)")
        
    except Exception as e:
        print(f"\nUnerwarteter Fehler: {e}")

if __name__ == '__main__':
    print("  RFID Serial Listener")
    listen()
