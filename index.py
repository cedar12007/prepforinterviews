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

    print("request: " + str(request.get_json()))
    # Parse the JSON data
    data = request.get_json()
    captcha_response = data.get('captcha')

    if not captcha_response:
        return jsonify({"success": False, "message": "CAPTCHA response is missing."}), 400

    # Verify CAPTCHA with Google
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': captcha_response
    }
    response = requests.post(verify_url, data=payload)
    result = response.json()

    if result.get("success"):
        return jsonify({"success": True, "message": "CAPTCHA passed!"})
    else:
        return jsonify({"success": False, "message": "CAPTCHA verification failed."}), 400

if __name__ == '__main__':
    app.run(debug=True)

#CORS(app, resources={r"/validate-captcha": {"origins": "https://yourusername.github.io"}})