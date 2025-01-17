from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS library
import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import verify_recaptcha

app = Flask(__name__)

CORS(app, resources={r"/validate-captcha": {"origins": "https://www.prepforinterviews.com"}})

RECAPTCHA_SECRET_KEY = "6LcXxroqAAAAAGeX9BkQ5oAxyKeeyoGPpesYUQkL"
GMAIL_USER = os.getenv("doar_ktovet")
GMAIL_PASSWORD = os.getenv("doar_sisma")

@app.route("/validate-captcha", methods=["POST"])
def validate_captcha():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")
    recaptcha_response = data.get("g-recaptcha-response")
    #recaptcha_metadata = verify_recaptcha.verify_recaptcha(recaptcha_response)

    # Verify reCAPTCHA response
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        },
    )
    result = response.json()

    print("results: " + str(result))

    if result.get("success"):
        # Send an email with the form data
        try:
            send_email(name, email, message, recaptcha_response)
            return jsonify({"success": True, "message": "CAPTCHA validation and email successful."})
        except Exception as e:
            print(f"Error sending email: {e}")
            return jsonify({"success": False, "message": "CAPTCHA validated but email failed."}), 500
    else:
        return jsonify({"success": False, "message": "CAPTCHA validation failed."}), 400




def send_email(name, email, message, recaptcha_response):
    """
    Sends an email containing the form data and reCAPTCHA response.
    """
    # Create email content
    subject = "New Form Submission with reCAPTCHA Data"
    body = f"""
    You have received a new form submission:

    Name: {name}
    Email: {email}
    Message: {message}

    reCAPTCHA Response:
    {recaptcha_response}
    """

    # Set up the email message
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = GMAIL_USER  # Send to your own email address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send the email using Gmail's SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(GMAIL_USER, GMAIL_PASSWORD)  # Login to Gmail
        server.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())  # Send email


if __name__ == "__main__":
    app.run(debug=True)