from flask import Flask, render_template, request, jsonify, abort
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-in-production")

# Security Headers
csp = {
    'default-src': "'self'",
    'style-src': ["'self'", "'unsafe-inline'"],
    'script-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
    'img-src': ["'self'", "data:", "https:"],
    'font-src': ["'self'", "https:"],
}
Talisman(app, content_security_policy=csp, force_https=False)

# Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "d3dff36f2d219ec36f5c48b6c6bb4819")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


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

@app.route("/tools")
def tools():
    return render_template("tools.html")

@app.route("/oracle")
def oracle():
    return render_template("oracle.html")
@app.route("/games")
def games():
    return render_template("games.html")
@app.route("/gm")
def gm():
    return render_template("gm.html")

@app.route("/get-weather")
@limiter.limit("30 per minute")
def get_weather():
    city = request.args.get("city", "").strip()
    if not city or len(city) > 100:
        return jsonify({"error": "Invalid city name"}), 400
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
    except Exception:
        return jsonify({"error": "Service unavailable"}), 503
    if data.get("cod") == 200:
        return jsonify({
            "name": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"]
        })
    else:
        return jsonify({"error": "City not found"}), 404

@app.route("/get-currency")
@limiter.limit("30 per minute")
def get_currency():
    base = request.args.get("base", "").strip().upper()
    target = request.args.get("target", "").strip().upper()
    try:
        amount = float(request.args.get("amount", 1))
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400
    if not base or not target or len(base) > 5 or len(target) > 5:
        return jsonify({"error": "Invalid currency"}), 400
    url = "https://api.exchangerate-api.com/v4/latest/" + base
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
    except Exception:
        return jsonify({"error": "Service unavailable"}), 503
    if target in data.get("rates", {}):
        rate = data["rates"][target]
        result = round(amount * rate, 2)
        return jsonify({"rate": rate, "result": result})
    else:
        return jsonify({"error": "Currency not found"}), 404

@app.route("/<page>")
def generic_page(page):
    allowed = [
        "todo", "timer", "stopwatch", "wordcount", "speedtest",
        "password", "color", "tip", "bmi", "age",
        "dice", "coin", "guess", "random", "quote", "counter",
        "blog", "skills", "timeline", "faq"
    ]
    if page in allowed:
        try:
            return render_template(f"{page}.html")
        except:
            abort(404)
    abort(404)

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({"error": "Too many requests, slow down!"}), 429

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)