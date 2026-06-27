print("Welcome to Calculator!")
print("1. Add")
print("2. Subtract")

choice = input("Choose (1 or 2): ")
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

if choice == "1":
    print("Result:", num1 + num2)
elif choice == "2":
    print("Result:", num1 - num2)
else:
    print("Invalid choice!")