from flask import Flask, request, jsonify
import requests
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
#CORS(app)  # Enable CORS for the whole app
# Enable CORS for the entire app
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://localhost:63342/, https://www.prepforinterview.com/"])  # Allow specific origin(s)

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

    # Define your Site Key (ID) and Secret Key
    site_key = "6Lf0zrkqAAAAAGqtAf-HyJn27SDi-v9lbKLk_XHxe"  # The same key used on the frontend
    secret_key = "6Lf0zrkqAAAAAGqtAf-HyJn27SDi-v9lbKLk_XHx"  # reCAPTCHA v3 uses the Site Key for both frontend and backend

    # Verify the CAPTCHA response with Google's reCAPTCHA API
    payload = {
        'secret': secret_key,
        'response': captcha_token
    }
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    response = requests.post(verify_url, data=payload)
    result = response.json()

    # Check if the CAPTCHA was successfully verified
    if result['success']:
        return jsonify({"success": True, "message": "CAPTCHA passed!"})
    else:
        return jsonify({"success": False, "message": "CAPTCHA verification failed."}), 400


if __name__ == '__main__':
    app.run(debug=True)

#CORS(app, resources={r"/validate-captcha": {"origins": "https://yourusername.github.io"}})