import tkinter as tk
from tkinter import messagebox
import sqlite3

def connect_db(db_name="charactersheet.db"):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    return con, cur

def create_table():
    con, cur = connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS charactersheet (
            name TEXT,
            race TEXT,
            class TEXT,
            level INTEGER,
            background TEXT,
            alignment TEXT,
            strength INTEGER,
            dexterity INTEGER,
            constitution INTEGER,
            intelligence INTEGER,
            wisdom INTEGER,
            charisma INTEGER,
            armorClass INTEGER,
            health INTEGER,
            knownSpells_amount INTEGER,
            knownSpells_prepared INTEGER,
            knownSpells_additional TEXT,
            knownSpells_cantrips TEXT,
            knownSpells_level1 TEXT,
            knownSpells_level2 TEXT,
            knownSpells_level3 TEXT,
            knownSpells_level4 TEXT,
            knownSpells_level5 TEXT,
            knownSpells_level6 TEXT,
            knownSpells_level7 TEXT,
            knownSpells_level8 TEXT,
            knownSpells_level9 TEXT
        )
    """)
    con.commit()
    con.close()

def setup_gui():
    root = tk.Tk()
    root.title("D&D Character Sheet")
    root.geometry("1000x600")

    left_frame = tk.Frame(root)
    left_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

    right_frame = tk.Frame(root)
    right_frame.pack(side="right", padx=10, pady=10, fill="y")

    fields = [
        "name", "race", "class", "level", "background", "alignment",
        "strength", "dexterity", "constitution",
        "intelligence", "wisdom", "charisma",
        "armorClass", "health", "knownSpells_amount", "knownSpells_prepared",
        "knownSpells_additional", "knownSpells_cantrips",
        "knownSpells_level1", "knownSpells_level2", "knownSpells_level3",
        "knownSpells_level4", "knownSpells_level5", "knownSpells_level6",
        "knownSpells_level7", "knownSpells_level8", "knownSpells_level9"
    ]

    entries = {}

    for i, field in enumerate(fields):
        label = tk.Label(left_frame, text=field + ":")
        label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
        entry = tk.Entry(left_frame, width=40)
        entry.grid(row=i, column=1, padx=5, pady=2)
        entries[field] = entry

    def save_character():
        data = [entries[f].get() for f in fields]

        if not data[0]:
            messagebox.showwarning("Missing Name", "Character name is required.")
            return

        try:
            con, cur = connect_db()
            cur.execute(f"""
                INSERT INTO charactersheet VALUES (
                    {','.join('?' for _ in fields)}
                )
            """, data)
            con.commit()
            con.close()
            messagebox.showinfo("Saved", f"{data[0]} saved to database!")
            load_character_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    save_btn = tk.Button(left_frame, text="Save Character", command=save_character)
    save_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def save_to_text_file():
        data = {field: entries[field].get() for field in fields}
        name = data.get("name", "").strip()

        if not name:
            messagebox.showwarning("Missing Name", "Enter a name before exporting.")
            return

        try:
            with open(f"{name}.txt", "w", encoding="utf-8") as f:
                for key, value in data.items():
                    f.write(f"{key}: {value}\n")
            messagebox.showinfo("Exported", f"{name}.txt has been created.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    export_btn = tk.Button(left_frame, text="Export to Text File", command=save_to_text_file)
    export_btn.grid(row=len(fields)+1, column=0, columnspan=2, pady=5)

    list_label = tk.Label(right_frame, text="Characters")
    list_label.pack()

    scrollbar = tk.Scrollbar(right_frame)
    scrollbar.pack(side="right", fill="y")

    character_listbox = tk.Listbox(right_frame, width=40, yscrollcommand=scrollbar.set)
    character_listbox.pack(fill="both", expand=True)
    scrollbar.config(command=character_listbox.yview)

    def load_character_list():
        character_listbox.delete(0, tk.END)
        con, cur = connect_db()
        cur.execute("SELECT name FROM charactersheet ORDER BY name")
        for row in cur.fetchall():
            character_listbox.insert(tk.END, row[0])
        con.close()

    def load_selected_character(event):
        selection = character_listbox.curselection()
        if not selection:
            return
        name = character_listbox.get(selection[0])
        con, cur = connect_db()
        cur.execute("SELECT * FROM charactersheet WHERE name = ?", (name,))
        row = cur.fetchone()
        con.close()
        if row:
            for i, field in enumerate(fields):
                entries[field].delete(0, tk.END)
                entries[field].insert(0, row[i])

    character_listbox.bind("<<ListboxSelect>>", load_selected_character)

    return root, load_character_list

if __name__ == "__main__":
    create_table()
    app, refresh_list = setup_gui()
    refresh_list()
    app.mainloop()
