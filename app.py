from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Welcome to My Web App!</h1><p>Built with Python and Flask.</p>"

@app.route("/about")
def about():
    return "<h1>About Me</h1><p>I learned Python and Git in 41 days!</p>"

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
    app.run(debug=True)