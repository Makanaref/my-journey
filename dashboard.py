import requests
import json
from datetime import datetime

WEATHER_API_KEY = "d3dff36f2d219ec36f5c48b6c6bb4819"
LOG_FILE = "dashboard_log.json"

def load_log():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_log(entry):
    log = load_log()
    log.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=4)

def show_log():
    log = load_log()
    if len(log) == 0:
        print("No log yet!")
    else:
        print("\n--- Dashboard Log ---")
        for item in log:
            print(item["time"] + " | " + item["city"] + " | " + str(item["temp"]) + "C | " + item["base"] + " to " + item["target"] + ": " + str(item["rate"]))

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
        return name, temp
    else:
        print("City not found!")
        return None, None

def get_rate(base, target):
    url = "https://api.exchangerate-api.com/v4/latest/" + base
    response = requests.get(url)
    data = response.json()
    if target in data["rates"]:
        rate = data["rates"][target]
        print("\n1 " + base + " = " + str(rate) + " " + target)
        return rate
    else:
        print("Currency not found!")
        return None

def show_dashboard():
    print("\n====== My Dashboard ======")
    print("Time: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("\n--- Weather ---")
    city, temp = get_weather("London")
    print("\n--- Exchange Rate ---")
    rate = get_rate("USD", "EUR")
    print("\n==========================")

    if city and rate:
        save_log({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "city": city,
            "temp": temp,
            "base": "USD",
            "target": "EUR",
            "rate": rate
        })
        print("Dashboard saved to log!")

while True:
    print("\n1. Show Dashboard")
    print("2. Show Log")
    print("3. Custom Weather")
    print("4. Custom Currency")
    print("5. Exit")

    choice = input("Choose (1-5): ")

    if choice == "5":
        print("Goodbye!")
        break
    elif choice == "1":
        show_dashboard()
    elif choice == "2":
        show_log()
    elif choice == "3":
        city = input("Enter city: ")
        get_weather(city)
    elif choice == "4":
        base = input("Enter base currency: ").upper()
        target = input("Enter target currency: ").upper()
        get_rate(base, target)
    else:
        print("Invalid choice!")