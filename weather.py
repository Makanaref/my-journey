import requests

API_KEY = "d3dff36f2d219ec36f5c48b6c6bb4819"

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

        print("\n🌍 Weather in " + name + ", " + country)
        print("🌡️  Temperature: " + str(temp) + "°C")
        print("🤔 Feels like: " + str(feels) + "°C")
        print("⬇️  Min: " + str(temp_min) + "°C  |  ⬆️  Max: " + str(temp_max) + "°C")
        print("☁️  Description: " + desc)
        print("💧 Humidity: " + str(humidity) + "%")
        print("💨 Wind: " + str(wind) + " m/s")
    else:
        print("City not found!")

while True:
    city = input("\nEnter city name (or 'exit'): ")
    if city.lower() == "exit":
        print("Goodbye!")
        break
    get_weather(city)