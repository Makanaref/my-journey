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
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        print("\n--- Weather in " + name + " ---")
        print("Temperature: " + str(temp) + "°C")
        print("Feels like: " + str(feels) + "°C")
        print("Description: " + desc)
        print("Humidity: " + str(humidity) + "%")
    else:
        print("City not found!")

city = input("Enter city name: ")
get_weather(city)