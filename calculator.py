print("Welcome to Calculator!")

history = []

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
        if len(history) == 0:
            print("No history yet!")
        else:
            print("\n--- History ---")
            for item in history:
                print(item)
        continue

    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if choice == "1":
        result = num1 + num2
        history.append(str(num1) + " + " + str(num2) + " = " + str(result))
    elif choice == "2":
        result = num1 - num2
        history.append(str(num1) + " - " + str(num2) + " = " + str(result))
    elif choice == "3":
        result = num1 * num2
        history.append(str(num1) + " * " + str(num2) + " = " + str(result))
    elif choice == "4":
        if num2 == 0:
            print("Error: Cannot divide by zero!")
            continue
        result = num1 / num2
        history.append(str(num1) + " / " + str(num2) + " = " + str(result))
    else:
        print("Invalid choice!")
        continue

    print("Result:", result)