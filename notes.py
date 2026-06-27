import os

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
    notes.append(note)
    save_notes(notes)
    print("Note saved!")

def show_notes(notes):
    if len(notes) == 0:
        print("No notes yet!")
    else:
        print("\n--- Your Notes ---")
        for i, note in enumerate(notes):
            print(str(i + 1) + ". " + note)

print("Welcome to Notes App!")
notes = load_notes()

while True:
    print("\n1. Add Note")
    print("2. Show Notes")
    print("3. Exit")

    choice = input("Choose (1-3): ")

    if choice == "3":
        print("Goodbye!")
        break
    elif choice == "1":
        add_note(notes)
    elif choice == "2":
        show_notes(notes)
    else:
        print("Invalid choice!")