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

print("Welcome to Notes App!")
notes = load_notes()

while True:
    print("\n1. Add Note")
    print("2. Show Notes")
    print("3. Delete Note")
    print("4. Exit")

    choice = input("Choose (1-4): ")

    if choice == "4":
        print("Goodbye!")
        break
    elif choice == "1":
        add_note(notes)
    elif choice == "2":
        show_notes(notes)
    elif choice == "3":
        delete_note(notes)
    else:
        print("Invalid choice!")