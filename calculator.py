history = []

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Cannot divide by zero!"
    return a / b

def show_history():
    if len(history) == 0:
        print("No history yet!")
    else:
        print("\n--- History ---")
        for item in history:
            print(item)

def calculate(choice, num1, num2):
    if choice == "1":
        result = add(num1, num2)
        history.append(str(num1) + " + " + str(num2) + " = " + str(result))
    elif choice == "2":
        result = subtract(num1, num2)
        history.append(str(num1) + " - " + str(num2) + " = " + str(result))
    elif choice == "3":
        result = multiply(num1, num2)
        history.append(str(num1) + " * " + str(num2) + " = " + str(result))
    elif choice == "4":
        result = divide(num1, num2)
        history.append(str(num1) + " / " + str(num2) + " = " + str(result))
    else:
        print("Invalid choice!")
        return
    print("Result:", result)

print("Welcome to Calculator!")

while True:
    print("\n1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Show History")
    print("6. Exit")

    choice = input("Choose (1-6): ")

    if choice == "6":
        print("Goodbye!")
        break
    elif choice == "5":
        show_history()
    else:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            calculate(choice, num1, num2)
        except ValueError:
            print("Error: Please enter a valid number!")