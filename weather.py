import requests
import json
from datetime import datetime

API_KEY = "d3dff36f2d219ec36f5c48b6c6bb4819"
HISTORY_FILE = "weather_history.json"

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_to_history(city, temp, desc):
    history = load_history()
    record = {
        "city": city,
        "temp": temp,
        "description": desc,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    history.append(record)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def show_history():
    history = load_history()
    if len(history) == 0:
        print("No history yet!")
    else:
        print("\n--- Search History ---")
        for item in history:
            print(item["time"] + " | " + item["city"] + " | " + str(item["temp"]) + "C | " + item["description"])

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data["cod"] == 200:
        name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        print("\nWeather in " + name + ", " + country)
        print("Temperature: " + str(temp) + "C")
        print("Feels like: " + str(feels) + "C")
        print("Min: " + str(temp_min) + "C  |  Max: " + str(temp_max) + "C")
        print("Description: " + desc)
        print("Humidity: " + str(humidity) + "%")
        print("Wind: " + str(wind) + " m/s")

        save_to_history(name, temp, desc)
    else:
        print("City not found!")

while True:
    print("\n1. Search Weather")
    print("2. Show History")
    print("3. Exit")

    choice = input("Choose (1-3): ")

    if choice == "3":
        print("Goodbye!")
        break
    elif choice == "2":
        show_history()
    elif choice == "1":
        city = input("Enter city name: ")
        get_weather(city)
    else:
        print("Invalid choice!")