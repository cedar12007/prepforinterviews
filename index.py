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
#RECAPTCHA_SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
RECAPTCHA_SECRET_KEY = "6Lf0zrkqAAAAAGqtAf-HyJn27SDi-v9lbKLk_XHx"

@app.route('/validate-captcha', methods=['POST'])
def validate_captcha():
    print("request: " + str(request.get_json()))

    # Ensure the request Content-Type is JSON
    if not request.is_json:
        return jsonify({"success": False, "message": "Invalid Content-Type. Expected 'application/json'."}), 400

    data = request.get_json()
    print("request: " + str(data))
    captcha_token = data.get('captcha')
    if not captcha_token:
        return jsonify({"success": False, "message": "CAPTCHA token is missing."}), 400

        # Get the reCAPTCHA token from the form submission
        recaptcha_response = request.form.get('g-recaptcha-response')

        # Verify the reCAPTCHA token with Google's API
        verification_url = 'https://www.google.com/recaptcha/api/siteverify'
        verification_payload = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        response = requests.post(verification_url, data=verification_payload)
        result = response.json()

        # Check if reCAPTCHA validation succeeded
        if result.get('success'):
            return jsonify(message='reCAPTCHA verified successfully!'), 200
        else:
            return jsonify(message='reCAPTCHA verification failed.'), 400


if __name__ == '__main__':
    app.run(debug=True)

#CORS(app, resources={r"/validate-captcha": {"origins": "https://yourusername.github.io"}})