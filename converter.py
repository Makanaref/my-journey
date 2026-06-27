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
    print("9. Exit")

    choice = input("Choose (1-9): ")

    if choice == "9":
        print("Goodbye!")
        break

    try:
        num = float(input("Enter value: "))

        if choice == "1":
            print("Result:", round(km_to_mile(num), 2), "miles")
        elif choice == "2":
            print("Result:", round(mile_to_km(num), 2), "km")
        elif choice == "3":
            print("Result:", round(celsius_to_fahrenheit(num), 2), "°F")
        elif choice == "4":
            print("Result:", round(fahrenheit_to_celsius(num), 2), "°C")
        elif choice == "5":
            print("Result:", round(kg_to_pound(num), 2), "pounds")
        elif choice == "6":
            print("Result:", round(pound_to_kg(num), 2), "kg")
        elif choice == "7":
            print("Result:", round(meter_to_foot(num), 2), "feet")
        elif choice == "8":
            print("Result:", round(foot_to_meter(num), 2), "meters")
        else:
            print("Invalid choice!")
    except ValueError:
        print("Error: Please enter a valid number!")