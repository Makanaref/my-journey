from datetime import datetime

history = []

def add_to_history(value, result, unit_from, unit_to):
    timestamp = datetime.now().strftime("%H:%M")
    record = "[" + timestamp + "] " + str(value) + " " + unit_from + " = " + str(result) + " " + unit_to
    history.append(record)

def show_history():
    if len(history) == 0:
        print("No history yet!")
    else:
        print("\n--- History ---")
        for item in history:
            print(item)

def km_to_mile(km):
    return km * 0.621371

def mile_to_km(mile):
    return mile * 1.60934

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

def kg_to_pound(kg):
    return kg * 2.20462

def pound_to_kg(pound):
    return pound * 0.453592

def meter_to_foot(m):
    return m * 3.28084

def foot_to_meter(foot):
    return foot * 0.3048

print("Welcome to Unit Converter!")

while True:
    print("\n1. Kilometer to Mile")
    print("2. Mile to Kilometer")
    print("3. Celsius to Fahrenheit")
    print("4. Fahrenheit to Celsius")
    print("5. Kilogram to Pound")
    print("6. Pound to Kilogram")
    print("7. Meter to Foot")
    print("8. Foot to Meter")
    print("9. Show History")
    print("0. Exit")

    choice = input("Choose (0-9): ")

    if choice == "0":
        print("Goodbye!")
        break
    elif choice == "9":
        show_history()
        continue

    try:
        num = float(input("Enter value: "))

        if choice == "1":
            result = round(km_to_mile(num), 2)
            print("Result:", result, "miles")
            add_to_history(num, result, "km", "miles")
        elif choice == "2":
            result = round(mile_to_km(num), 2)
            print("Result:", result, "km")
            add_to_history(num, result, "miles", "km")
        elif choice == "3":
            result = round(celsius_to_fahrenheit(num), 2)
            print("Result:", result, "°F")
            add_to_history(num, result, "°C", "°F")
        elif choice == "4":
            result = round(fahrenheit_to_celsius(num), 2)
            print("Result:", result, "°C")
            add_to_history(num, result, "°F", "°C")
        elif choice == "5":
            result = round(kg_to_pound(num), 2)
            print("Result:", result, "pounds")
            add_to_history(num, result, "kg", "pounds")
        elif choice == "6":
            result = round(pound_to_kg(num), 2)
            print("Result:", result, "kg")
            add_to_history(num, result, "pounds", "kg")
        elif choice == "7":
            result = round(meter_to_foot(num), 2)
            print("Result:", result, "feet")
            add_to_history(num, result, "m", "feet")
        elif choice == "8":
            result = round(foot_to_meter(num), 2)
            print("Result:", result, "meters")
            add_to_history(num, result, "feet", "m")
        else:
            print("Invalid choice!")
    except ValueError:
        print("Error: Please enter a valid number!")