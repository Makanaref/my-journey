import requests
from datetime import datetime

def get_rate(base, target):
    url = "https://api.exchangerate-api.com/v4/latest/" + base
    response = requests.get(url)
    data = response.json()

    if target in data["rates"]:
        rate = data["rates"][target]
        print("\n--- Exchange Rate ---")
        print("1 " + base + " = " + str(rate) + " " + target)
        print("Updated: " + data["date"])
        return rate
    else:
        print("Currency not found!")
        return None

def convert(base, target, amount):
    rate = get_rate(base, target)
    if rate:
        result = round(amount * rate, 2)
        print("\n" + str(amount) + " " + base + " = " + str(result) + " " + target)

while True:
    print("\n1. Get Exchange Rate")
    print("2. Convert Currency")
    print("3. Exit")

    choice = input("Choose (1-3): ")

    if choice == "3":
        print("Goodbye!")
        break
    elif choice == "1":
        base = input("Enter base currency (e.g. USD): ").upper()
        target = input("Enter target currency (e.g. EUR): ").upper()
        get_rate(base, target)
    elif choice == "2":
        base = input("Enter base currency (e.g. USD): ").upper()
        target = input("Enter target currency (e.g. IRR): ").upper()
        amount = float(input("Enter amount: "))
        convert(base, target, amount)
    else:
        print("Invalid choice!")