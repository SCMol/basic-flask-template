from flask import Flask, render_template, request
import requests

DEVELOPMENT_ENV = True

app = Flask(__name__)

app_data = {
    "description": "For all your fish needs",
    "html_title": "Feeeesh",
    "project_name": "Fish Doc",
    "keywords": "flask, webapp, template, basic",
}

# Define FastAPI endpoint URLs
HEALTH_CHECK_API_URL = "https://fishapi-rhatlat23q-ew.a.run.app/analyze-image"
SPECIES_ID_API_URL = "https://fishapi-rhatlat23q-ew.a.run.app/id-species"
DISEASE_ID_API_URL = "https://fishapi-rhatlat23q-ew.a.run.app/analyze-disease"

@app.route("/")
def index():
    return render_template("index.html", app_data=app_data)

@app.route("/health-check", methods=['GET', 'POST'])
def health_check():
    if request.method == 'POST':
        return analyze_image(HEALTH_CHECK_API_URL)
    return render_template("health-check.html", app_data=app_data)

@app.route("/species-id", methods=['GET', 'POST'])
def species_id():
    if request.method == 'POST':
        return analyze_image(SPECIES_ID_API_URL)
    return render_template("species-id.html", app_data=app_data)

@app.route("/disease-id", methods=['GET', 'POST'])
def disease_id():
    if request.method == 'POST':
        return analyze_image(DISEASE_ID_API_URL)
    return render_template("disease-id.html", app_data=app_data)

def analyze_image(api_url):
    if 'file' not in request.files:
        return render_template("error.html", message="No file uploaded.")

    file = request.files['file']
    if file.filename == '':
        return render_template("error.html", message="No file selected.")

    # Prepare payload for FastAPI
    files = {'file': (file.filename, file.read(), 'image/jpeg')}

    # Send request to FastAPI
    response = requests.post(api_url, files=files)

    # Get results
    results = response.json()

    return render_template("results.html", results=results)

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)
