import csv

# بنویس تو CSV
with open("students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age", "Grade"])
    writer.writerow(["Ali", 20, "A"])
    writer.writerow(["Sara", 22, "B"])
    writer.writerow(["Donk", 21, "A+"])

print("Saved to students.csv!")

# بخون از CSV
with open("students.csv", "r") as f:
    reader = csv.reader(f)
    print("\n--- Students ---")
    for row in reader:
        print(row)