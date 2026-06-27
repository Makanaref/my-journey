import os
from datetime import datetime

NOTES_FILE = "notes.txt"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return f.read().splitlines()
    return []

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        for note in notes:
            f.write(note + "\n")

def add_note(notes):
    note = input("Enter your note: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    note_with_time = "[" + timestamp + "] " + note
    notes.append(note_with_time)
    save_notes(notes)
    print("Note saved!")

def show_notes(notes):
    if len(notes) == 0:
        print("No notes yet!")
    else:
        print("\n--- Your Notes ---")
        for i, note in enumerate(notes):
            print(str(i + 1) + ". " + note)

def delete_note(notes):
    show_notes(notes)
    if len(notes) == 0:
        return
    try:
        num = int(input("Enter note number to delete: "))
        if num < 1 or num > len(notes):
            print("Invalid number!")
            return
        deleted = notes.pop(num - 1)
        save_notes(notes)
        print("Deleted: " + deleted)
    except ValueError:
        print("Error: Please enter a valid number!")

def edit_note(notes):
    show_notes(notes)
    if len(notes) == 0:
        return
    try:
        num = int(input("Enter note number to edit: "))
        if num < 1 or num > len(notes):
            print("Invalid number!")
            return
        print("Old note: " + notes[num - 1])
        new_note = input("Enter new note: ")
        notes[num - 1] = new_note
        save_notes(notes)
        print("Note updated!")
    except ValueError:
        print("Error: Please enter a valid number!")

def search_notes(notes):
    if len(notes) == 0:
        print("No notes yet!")
        return
    keyword = input("Enter search keyword: ")
    results = []
    for i, note in enumerate(notes):
        if keyword.lower() in note.lower():
            results.append(str(i + 1) + ". " + note)
    if len(results) == 0:
        print("No notes found!")
    else:
        print("\n--- Search Results ---")
        for result in results:
            print(result)

print("Welcome to Notes App!")
notes = load_notes()

while True:
    print("\n1. Add Note")
    print("2. Show Notes")
    print("3. Delete Note")
    print("4. Edit Note")
    print("5. Search Notes")
    print("6. Exit")

    choice = input("Choose (1-6): ")

    if choice == "6":
        print("Goodbye!")
        break
    elif choice == "1":
        add_note(notes)
    elif choice == "2":
        show_notes(notes)
    elif choice == "3":
        delete_note(notes)
    elif choice == "4":
        edit_note(notes)
    elif choice == "5":
        search_notes(notes)
    else:
        print("Invalid choice!")