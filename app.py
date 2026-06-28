from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return "<h1>About Me</h1><p>I learned Python and Git in 43 days!</p>"

@app.route("/projects")
def projects():
    return """
    <h1>My Projects</h1>
    <ul>
        <li>Calculator</li>
        <li>Notes App</li>
        <li>Unit Converter</li>
        <li>Reminder App</li>
        <li>Weather App</li>
        <li>Currency Converter</li>
        <li>Dashboard</li>
    </ul>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)