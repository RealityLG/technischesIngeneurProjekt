import tkinter as tk
from tkinter import ttk, messagebox
import database
# Projektlogik, Methodenplanung und GUI-/Datenbankstruktur stammen vollständig vom Autor; 
# GitHub Copilot / ChatGPT wurde nur teils für Python-Syntax und Bibliotheksdetails genutzt.

"""gui.py
GUI für Parkplatzverwaltungssystem
@author: Vincent Gentz
Matrikelnummer:
Datum: 22.10.2025"""

# Datenbankpfad aus database.py importieren, falls nicht vorhanden, wird erstellt
DB_PATH = database.DB_PATH if hasattr(database, 'DB_PATH') else 'app_database.db'


class ParkGUI(tk.Tk):
    # Initialisierung des Grundfensters der GUI
    def __init__(self):
        super().__init__()
        self.title('Personen - Parkverwaltung')
        self.geometry('1000x420')
        self.create_widgets()
        self.load_data()
    
    # Erstellung der Widgets
    def create_widgets(self):
        cols = ('UID', 'Vorname', 'Nachname', 'Parkplatznummer', 'Belegt', 'Eingecheckt')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=20)
        
        # Spaltenbreiten definieren
        self.tree.column('UID', width=100)
        self.tree.column('Vorname', width=120)
        self.tree.column('Nachname', width=120)
        self.tree.column('Parkplatznummer', width=120)
        self.tree.column('Belegt', width=80)
        self.tree.column('Eingecheckt', width=100)
        
        # Spaltenüberschriften definieren
        for col in cols:
            self.tree.heading(col, text=col)

        # Baumansicht und Scrollbar
        self.tree.pack(side='left', fill='both', expand=True, padx=(8,0), pady=8)

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='left', fill='y', pady=8)

        # Kontextmenü für Löschen
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Löschen", command=self.delete_selected)
        self.tree.bind("<Button-3>", self.show_context_menu)

        # Rechte Seite mit Buttons
        right = ttk.Frame(self)
        right.pack(side='right', fill='y', padx=8, pady=8)

        ttk.Button(right, text="Person hinzufügen", command=self.Dialogfenster_hinzufuegen, width=20).pack(pady=5)
        ttk.Button(right, text="Aktualisieren", command=self.load_data, width=20).pack(pady=5)
        ttk.Button(right, text="Beenden", command=self.quit, width=20).pack(pady=5)

    # Kontextmenü anzeigen
    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y) # Zeile unter Mauszeiger finden
        if item:
            self.tree.selection_set(item) # Zeile auswählen
            self.menu.post(event.x_root, event.y_root) # Menü anzeigen

    # Ausgewählte Person löschen
    def delete_selected(self):
        selected = self.tree.selection() # Ausgewählte Zeile holen

        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wähle eine Person aus.")
            return
        
        item = selected[0] # 
        values = self.tree.item(item, 'values')
        uid = values[0]
        
        confirm = messagebox.askyesno("Löschen bestätigen", 
                                      f"Person mit UID {uid} wirklich löschen?")
        if confirm:
            database.delete_person(uid)
            self.load_data()

    # Daten aus Datenbank laden und anzeigen
    def load_data(self):
        # Alle Einträge löschen
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Neue Einträge laden
        personen = database.show_all_personen()
        for p in personen:
            self.tree.insert('', 'end', values=(
                p['uid'],
                p['vorname'],
                p['nachname'],
                p['parkplatznummer'],
                'Ja' if p['belegt'] else 'Nein',
                'Ja' if p['eingecheckt'] else 'Nein'
            ))

    # Dialog zum Hinzufügen einer neuen Person öffnen
    def Dialogfenster_hinzufuegen(self):

        dlg = tk.Toplevel(self)
        dlg.title("Person hinzufügen")
        dlg.geometry("350x220")
        #self.center_window(dlg)
        
        # Eingabefeld für UID, Vorname, Nachname, Parkplatznummer
        ttk.Label(dlg, text="UID:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        uid_entry = ttk.Entry(dlg, width=25)
        uid_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dlg, text="Vorname:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        vorname_entry = ttk.Entry(dlg, width=25)
        vorname_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dlg, text="Nachname:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        nachname_entry = ttk.Entry(dlg, width=25)
        nachname_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dlg, text="Parkplatznummer:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        parkplatz_entry = ttk.Entry(dlg, width=25)
        parkplatz_entry.grid(row=3, column=1, padx=10, pady=5)

        # Hinzufügen-Button mit Hilfe von add_person_gui
        ttk.Button(dlg, text="Hinzufügen", 
                   command=lambda: self.add_person_gui(dlg, uid_entry.get(), vorname_entry.get(), 
                                                    nachname_entry.get(), parkplatz_entry.get())
                  ).grid(row=4, column=0, columnspan=2, pady=10)

    # Kontrolle der Eingaben und Hinzufügen der Person zur Datenbank mit add_person
    def add_person_gui(self, dlg, uid: str, vorname: str, nachname: str, parkplatz: str):
        uid = uid.upper().replace(" ", "")
        
        if not uid or not vorname or not nachname or not parkplatz:
            messagebox.showwarning("Eingabefehler", "Bitte alle Felder ausfüllen!")
            return
        

        try:
            database.add_person(uid=uid, vorname=vorname, nachname=nachname, parkplatznummer=parkplatz) # Fügt Person hinzu
            messagebox.showinfo("Erfolg", f"Person {vorname} {nachname} mit UID {uid} hinzugefügt!")
            dlg.destroy() # Zwischenspeicher schließen
            self.load_data()
        except Exception as e: 
            messagebox.showerror("Fehler", f"Fehler beim Hinzufügen: {e}")

    # Zentriert ein Fenster auf dem Bildschirm
    def fokus_window(self, win):
        win.update_idletasks() # Aktualisiert Fensterinformationen
        width = win.winfo_width() 
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == '__main__':
    app = ParkGUI()
    app.mainloop()