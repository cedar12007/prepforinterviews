from flask import Flask, request, jsonify, send_from_directory
import os

import requests
#from flask_cors import CORS  # Import CORS

app = Flask(__name__)

@app.route('/')
def serve_html():
    # Serve the index.html file directly from the root directory
    return send_from_directory(os.getcwd(), 'index.html')

#CORS(app)  # Enable CORS for the whole app
# Enable CORS for the entire app
#CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://localhost:63342/", "https://www.prepforinterview.com/"])  # Allow specific origin(s)
# Define the allowed origins
allowed_origins = ["http://127.0.0.1:5500", "http://localhost:5500", "http://localhost:63342/", "https://www.prepforinterview.com/"]

@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')

    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'

    # Handle OPTIONS request (pre-flight request)
    if request.method == 'OPTIONS':
        response.status_code = 200
    return response

# Replace with your reCAPTCHA secret key
RECAPTCHA_SECRET_KEY = "6LcXxroqAAAAAGeX9BkQ5oAxyKeeyoGPpesYUQkL"

@app.route('/validate-captcha', methods=['POST'])
def validate_captcha():
    print("request: " + str(request.get_json()))

    data = request.json
    recaptcha_response = data.get("g-recaptcha-response")

    # Verify reCAPTCHA response
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        },
    )
    result = response.json()

    if result.get("success") and result.get("score", 0) >= 0.5:  # Check score for v3
        # Process form data here
        return jsonify({"success": True, "message": "CAPTCHA validation successful."})
    else:
        return jsonify({"success": False, "message": "CAPTCHA validation failed."}), 400


if __name__ == '__main__':
    app.run(debug=True)

#CORS(app, resources={r"/validate-captcha": {"origins": "https://yourusername.github.io"}})