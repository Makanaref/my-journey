def km_to_mile(km):
    return km * 0.621371

def mile_to_km(mile):
    return mile * 1.60934

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

print("Welcome to Unit Converter!")

while True:
    print("\n1. Kilometer to Mile")
    print("2. Mile to Kilometer")
    print("3. Celsius to Fahrenheit")
    print("4. Fahrenheit to Celsius")
    print("5. Exit")

    choice = input("Choose (1-5): ")

    if choice == "5":
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
        else:
            print("Invalid choice!")
    except ValueError:
        print("Error: Please enter a valid number!")