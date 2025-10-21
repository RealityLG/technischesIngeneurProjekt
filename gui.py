#gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import database

DB_PATH = database.DB_PATH if hasattr(database, 'DB_PATH') else 'app_database.db'

class ParkGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Personen - Parkverwaltung')
        self.geometry('900x420')
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        cols = ('ID', 'Vorname', 'Nachname', 'Parkplatznummer', 'Belegt', 'Check-in-Zeit')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=20)
        for col in cols:
            self.tree.heading(col, text=col.capitalize())
            if col == 'ID':
                self.tree.column(col, width=50, anchor='center')
            else:
                self.tree.column(col, width=140, anchor='w')

        self.tree.pack(side='left', fill='both', expand=True, padx=(8,0), pady=8)

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y', pady=8)

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Löschen", command=self.delete_selected)
        self.tree.bind("<Button-3>", self.show_context_menu)

        right = ttk.Frame(self)
        right.pack(side='left', fill='y', pady=8)

        right = ttk.Frame(self)
        right.pack(side='right', fill='y', padx=8, pady=8)

        ttk.Button(right, text='Refresh', command=self.load_data).pack(fill='x', pady=8)
        ttk.Button(right, text='Hinzufügen', command=self.open_add_dialog).pack(fill='x', pady=6)
        
    def show_context_menu(self, event):
        """Zeigt Kontextmenü beim Rechtsklick und selektiert die Zeile unter der Maus."""
        iid = self.tree.identify_row(event.y)
        if iid:
            # selektiere die Zeile, damit delete_selected weiß, was gelöscht wird
            self.tree.selection_set(iid)
            try:
                self.menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.menu.grab_release()

    def delete_selected(self):
        """Löscht die aktuell selektierte Zeile (nutzt database.delete_person oder Fallback SQL)."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Keine Auswahl", "Bitte erst eine Zeile auswählen.")
            return
        vals = self.tree.item(sel[0], 'values')
        # Annahme: columns = (ID, Vorname, Nachname, Parkplatznummer, Belegt, Eingecheckt)
        try:
            vorname = vals[1]
            nachname = vals[2]
            parkplatz = vals[3]
        except Exception:
            messagebox.showerror("Fehler", f"Unerwartetes Zeilenformat: {vals}")
            return

        if not messagebox.askyesno("Löschen bestätigen", f"Soll {vorname} {nachname} (Parkplatz {parkplatz}) gelöscht werden?"):
            return

        # Versuche zuerst bestehende delete_person(vorname, nachname)
        try:
            if hasattr(database, 'delete_person'):
                deleted = database.delete_person(vorname, nachname, parkplatz)
        except Exception as e:
            messagebox.showerror("Fehler beim Löschen", f"Fehler: {e}")
            return

        if deleted:
            messagebox.showinfo("Gelöscht", f"{deleted} Eintrag(e) gelöscht.")
            self.load_data()
        else:
            messagebox.showinfo("Nicht gefunden", "Keine Einträge gelöscht.")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if not os.path.exists(DB_PATH):
            messagebox.showerror("Error", f"Database file '{DB_PATH}' not found.")
            return
        
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute("SELECT id, vorname, nachname, parkplatznummer, belegt, eingecheckt FROM personen")
            rows = cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            return
        finally:
            try:
                connection.close()
            except Exception:
                pass

        for row in rows:
            belegt = 'Ja' if row[4] else 'Nein'
            eingecheckt = row[5] if row[5] else 'Nicht eingecheckt'
            self.tree.insert('', 'end', values =(row[0], row[1], row[2], row[3], belegt, eingecheckt))

    def open_add_dialog(self):
        """Öffnet ein Modal, um eine neue Person einzugeben."""
        dlg = tk.Toplevel(self)
        dlg.title("Person hinzufügen")
        dlg.transient(self)
        dlg.grab_set()

        # Labels + Entries
        ttk.Label(dlg, text="Vorname:").grid(row=0, column=0, sticky='w', padx=8, pady=6)
        e_vor = ttk.Entry(dlg)
        e_vor.grid(row=0, column=1, padx=8, pady=6)

        ttk.Label(dlg, text="Nachname:").grid(row=1, column=0, sticky='w', padx=8, pady=6)
        e_nach = ttk.Entry(dlg)
        e_nach.grid(row=1, column=1, padx=8, pady=6)

        ttk.Label(dlg, text="Parkplatznummer:").grid(row=2, column=0, sticky='w', padx=8, pady=6)
        e_park = ttk.Entry(dlg)
        e_park.grid(row=2, column=1, padx=8, pady=6)

        # Buttons
        btn_frame = ttk.Frame(dlg)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(6,8))

        add_btn = ttk.Button(btn_frame, text="Hinzufügen",
                             command=lambda: self.perform_add(dlg, e_vor.get().strip(), e_nach.get().strip(), e_park.get().strip()))
        add_btn.pack(side='left', padx=6)

        ttk.Button(btn_frame, text="Abbrechen", command=dlg.destroy).pack(side='left', padx=6)

        # Fokus auf Vorname setzen
        e_vor.focus_set()

        # Enter = hinzufügen
        dlg.bind('<Return>', lambda event: self.perform_add(dlg, e_vor.get().strip(), e_nach.get().strip(), e_park.get().strip()))

        # Fenster zentrieren
        self.center_window(dlg)

    def perform_add(self, dlg, vorname: str, nachname: str, parkplatz: str):
        """Validiert Eingabe, ruft database.add_person auf, schließt Dialog und lädt Tabelle neu."""
        if not (vorname and nachname and parkplatz):
            messagebox.showwarning("Fehler", "Bitte Vorname, Nachname und Parkplatznummer ausfüllen.")
            return

        try:
            # database.add_person erwartet (vorname, nachname, parkplatznummer)
            new_id = database.add_person(vorname, nachname, parkplatz)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Hinzufügen:\n{e}")
            return

        if new_id:
            messagebox.showinfo("Erfolgreich", f"Person hinzugefügt (ID={new_id}).")
            try:
                dlg.destroy()
            except Exception:
                pass
            self.load_data()
        else:
            messagebox.showerror("Fehler", "Konnte Person nicht hinzufügen (siehe Konsole).")

    def center_window(self, win):
        """Kleinere Hilfsfunktion: zentriert ein Toplevel über dem Hauptfenster."""
        win.update_idletasks()
        w = win.winfo_width()
        h = win.winfo_height()
        # falls noch 1x1 (nicht gesetzt) — gib Standardgröße
        if w <= 1: w = 300
        if h <= 1: h = 140
        x = self.winfo_rootx() + (self.winfo_width() - w) // 2
        y = self.winfo_rooty() + (self.winfo_height() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

if __name__ == '__main__':
    app = ParkGUI()
    app.mainloop()
