from datetime import datetime
import os

REMINDERS_FILE = "reminders.txt"

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as f:
            return f.read().splitlines()
    return []

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        for item in reminders:
            f.write(item + "\n")

def add_reminder(reminders):
    title = input("Enter reminder title: ")
    date = input("Enter date (YYYY-MM-DD): ")
    timestamp = datetime.now().strftime("%H:%M")
    record = date + " | " + title + " | added at " + timestamp
    reminders.append(record)
    save_reminders(reminders)
    print("Reminder saved!")

def show_reminders(reminders):
    if len(reminders) == 0:
        print("No reminders yet!")
    else:
        print("\n--- Your Reminders ---")
        for i, item in enumerate(reminders):
            print(str(i + 1) + ". " + item)
def delete_reminder(reminders):
    show_reminders(reminders)
    if len(reminders) == 0:
        return
    try:
        num = int(input("Enter reminder number to delete: "))
        if num < 1 or num > len(reminders):
            print("Invalid number!")
            return
        deleted = reminders.pop(num - 1)
        save_reminders(reminders)
        print("Deleted: " + deleted)
    except ValueError:
        print("Error: Please enter a valid number!")

def sort_reminders(reminders):
    if len(reminders) == 0:
        print("No reminders yet!")
        return
    reminders.sort()
    save_reminders(reminders)
    print("Reminders sorted by date!")

print("Welcome to Reminder App!")
reminders = load_reminders()

while True:
    print("\n1. Add Reminder")
    print("2. Show Reminders")
    print("3. Delete Reminder")
    print("4. Sort by Date")
    print("5. Exit")

    choice = input("Choose (1-5): ")

    if choice == "5":
        print("Goodbye!")
        break
    elif choice == "1":
        add_reminder(reminders)
    elif choice == "2":
        show_reminders(reminders)
    elif choice == "3":
        delete_reminder(reminders)
    elif choice == "4":
        sort_reminders(reminders)
        show_reminders(reminders)
    else:
        print("Invalid choice!")