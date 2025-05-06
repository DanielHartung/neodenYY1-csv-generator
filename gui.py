import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import pandas as pd
from yy1 import Machine
from Part import unit_norminal
from Part import Part
from Part import typing, typing_list, prenum
from generator import Generator

class PickAndPlaceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        #Varialbes
        self.partlist = []

        # Fenster initialisieren
        self.title("Pick and Place Data Processor")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # MNT-Datei laden Button
        self.load_button = ctk.CTkButton(self, text="Load MNT file", command=self.load_mnt_file)
        self.load_button.pack(pady=20, anchor="n")

        # Haupt-Frame für Tabelle und Scrollbar erstellen
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Canvas für die Tabelle und Scrollbar erstellen
        self.table_canvas = tk.Canvas(self.main_frame)
        self.table_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar rechts hinzufügen
        self.scrollbar = ctk.CTkScrollbar(self.main_frame, orientation="vertical", command=self.table_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.table_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame für die Tabelle auf dem Canvas
        self.table_frame = ctk.CTkFrame(self.table_canvas)
        self.table_canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # CSV-Daten und Checkboxes speichern
        self.data = None
        self.checkboxes = []
        self.feeders = []

        # Canvas scrollable machen
        self.table_frame.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))

        # Generate Button
        self.generate_button = ctk.CTkButton(self, text="Generate CSV", command=self.generate_output)
        self.generate_button.pack(pady=20, anchor="s")

    def load_machine_file(self):
        print('Load Machine file')
        self.machine = Machine('machine.csv')

    def load_mnt_file(self):
        # Datei-Auswahl Dialog
        file_path = filedialog.askopenfilename(filetypes=[("MNT files", "*.mnt")])

        if file_path:
            # MNT-Datei lesen, Semikolon als Trennzeichen verwenden
            self.data = pd.read_csv(file_path, delimiter=";")
            self.load_machine_file()
            self.display_table()

    def display_table(self):
        # Zuerst alle vorherigen Widgets löschen
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Tabellenkopf anzeigen
        headers = ["Part", "Value", "TYP", "X Pos", "Y Pos", "Rotation", "Feeder", "Place?"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(self.table_frame, text=header)
            header_label.grid(row=0, column=i, padx=5, pady=5)

        # Daten anzeigen
        self.checkboxes.clear()
        self.feeders.clear()

        # Dynamische Zuweisung von Feedern (z.B. einfach der Reihe nach 1, 2, 3, ...)
        for i, row in self.data.iterrows():
            part = Part()

            for j, value in enumerate(row):
                if j == 0:
                    part.name = value
                    part.typ = typing(part.name)
                if j == 1:
                    if part.typ in typing_list:
                        part.nvalue = prenum(value)
                    else:
                        part.nvalue = value
                elif j == 2:
                    part.package = value
                elif j == 3:
                    part.pos_x = value
                elif j == 4:
                    part.pos_y = value
                elif j == 5:
                    part.rotation = value
                entry = ctk.CTkLabel(self.table_frame, text=str(value))
                entry.grid(row=i + 1, column=j, padx=5, pady=5)

            # generate Part and save it
            self.partlist.append(part)

            # Feeder-Nummer zuweisen (zum Beispiel einfach hochzählen)
            # Search for Feeder
            feeder = self.machine.find_feeder(part.nvalue,part.package)

            if feeder != None:
                feeder_number = feeder.id
            else:
                feeder_number = 0
            feeder_label = ctk.CTkLabel(self.table_frame, text=str(feeder_number))
            feeder_label.grid(row=i + 1, column=len(row), padx=5, pady=5)
            self.feeders.append(feeder_number)

            # Checkbox hinzufügen
            if feeder != None:
                var = tk.BooleanVar(value=True)
            else:
                var = tk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(self.table_frame, variable=var, text="")
            checkbox.grid(row=i + 1, column=len(row) + 1, padx=5, pady=5)
            self.checkboxes.append(var)

        # Die Größe der Canvas anpassen, damit sie scrollbar wird
        self.table_frame.update_idletasks()
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

    def generate_output(self):
        if self.data is not None:
            self.data["Feeder"] = self.feeders
            self.data["Place?"] = [checkbox.get() for checkbox in self.checkboxes]

            if len(self.partlist) == len(self.data['Place?']):
                gen_list = []
                for x in range(len(self.partlist)):
                    if self.data['Place?'][x] == True:
                        gen_list.append(self.partlist[x])


                self.machine.generate_placeable_partlist(gen_list)

                placeable_parts = self.machine.get_placeable_parts()
                nozzle_changes = self.machine.get_nozzle_changes()

                save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
                if save_path:
                    try:
                        g = Generator(placeable_parts, nozzle_changes)
                        g.generate(save_path)
                        ctk.CTkLabel(self, text="CSV erfolgreich gespeichert!").pack(pady=10)
                    except Exception as e:
                        ctk.CTkLabel(self, text=f"Fehler beim Speichern der CSV: {str(e)}").pack(pady=10)


# Main
if __name__ == "__main__":
    app = PickAndPlaceApp()
    app.mainloop()
