from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS library
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

RECAPTCHA_SECRET_KEY = "6LcXxroqAAAAAGeX9BkQ5oAxyKeeyoGPpesYUQkL"

@app.route("/validate-captcha", methods=["POST"])
def validate_captcha():
    data = request.json
    print("validate-captcha data: " + str(data))
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

    if result.get("success"):
        return jsonify({"success": True, "message": "CAPTCHA validation successful."})
    else:
        return jsonify({"success": False, "message": "CAPTCHA validation failed."}), 400

if __name__ == "__main__":
    app.run(debug=True)