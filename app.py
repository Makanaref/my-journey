from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

WEATHER_API_KEY = "d3dff36f2d219ec36f5c48b6c6bb4819"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/weather")
def weather():
    return render_template("weather.html")

@app.route("/currency")
def currency():
    return render_template("currency.html")

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")

@app.route("/notes")
def notes():
    return render_template("notes.html")

@app.route("/converter")
def converter():
    return render_template("converter.html")

@app.route("/reminder")
def reminder():
    return render_template("reminder.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/get-weather")
def get_weather():
    city = request.args.get("city")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
    response = requests.get(url, params=params)
    data = response.json()
    if data["cod"] == 200:
        return jsonify({
            "name": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"]
        })
    else:
        return jsonify({"error": "City not found"})

@app.route("/get-currency")
def get_currency():
    base = request.args.get("base")
    target = request.args.get("target")
    amount = float(request.args.get("amount", 1))
    url = "https://api.exchangerate-api.com/v4/latest/" + base
    response = requests.get(url)
    data = response.json()
    if target in data["rates"]:
        rate = data["rates"][target]
        result = round(amount * rate, 2)
        return jsonify({"rate": rate, "result": result})
    else:
        return jsonify({"error": "Currency not found"})

@app.route("/blog")
def blog():
    return render_template("blog.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

@app.route("/skills")
def skills():
    return render_template("skills.html")

@app.route("/timeline")
def timeline():
    return render_template("timeline.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/quote")
def quote():
    return render_template("quote.html")

@app.route("/counter")
def counter():
    return render_template("counter.html")

@app.route("/timer")
def timer():
    return render_template("timer.html")

@app.route("/random")
def random_number():
    return render_template("random.html")

@app.route("/password")
def password():
    return render_template("password.html")

@app.route("/bmi")
def bmi():
    return render_template("bmi.html")