import requests
import json
from datetime import datetime

WEATHER_API_KEY = "YOUR_API_KEY"

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data["cod"] == 200:
        name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        print("\nWeather in " + name + ", " + country)
        print("Temperature: " + str(temp) + "C")
        print("Description: " + desc)
        print("Humidity: " + str(humidity) + "%")
    else:
        print("City not found!")

def get_rate(base, target):
    url = "https://api.exchangerate-api.com/v4/latest/" + base
    response = requests.get(url)
    data = response.json()
    if target in data["rates"]:
        rate = data["rates"][target]
        print("\n1 " + base + " = " + str(rate) + " " + target)
    else:
        print("Currency not found!")

def show_dashboard():
    print("\n====== My Dashboard ======")
    print("Time: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("\n--- Weather ---")
    get_weather("London")
    print("\n--- Exchange Rate ---")
    get_rate("USD", "EUR")
    get_rate("USD", "GBP")
    print("\n==========================")

while True:
    print("\n1. Show Dashboard")
    print("2. Custom Weather")
    print("3. Custom Currency")
    print("4. Exit")

    choice = input("Choose (1-4): ")

    if choice == "4":
        print("Goodbye!")
        break
    elif choice == "1":
        show_dashboard()
    elif choice == "2":
        city = input("Enter city: ")
        get_weather(city)
    elif choice == "3":
        base = input("Enter base currency: ").upper()
        target = input("Enter target currency: ").upper()
        get_rate(base, target)
    else:
        print("Invalid choice!")