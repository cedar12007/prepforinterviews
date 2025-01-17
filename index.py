from flask import Flask, request, jsonify, session
from flask_cors import CORS  # Import CORS library
import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

import verify_recaptcha

app = Flask(__name__)

app.secret_key = os.getenv("mafteah_sod")

CORS(app, resources={r"/validate-captcha": {"origins": "https://www.prepforinterviews.com"}})

RECAPTCHA_SECRET_KEY = "6LcXxroqAAAAAGeX9BkQ5oAxyKeeyoGPpesYUQkL"
GMAIL_USER = os.getenv("doar_ktovet")
GMAIL_PASSWORD = os.getenv("doar_sisma")
# Maximum allowed submissions per IP within the time window
MAX_SUBMISSIONS = 3
TIME_WINDOW = 60 * 5  # 5 minutes in seconds

@app.route("/validate-captcha", methods=["POST"])
def validate_captcha():
    ip_address = request.remote_addr  # Get the user's IP address
    print("ip_address: " + str(ip_address))
    # Track submissions per session
    if ip_address not in session:
        session[ip_address] = {"count": 0, "timestamp": time.time()}
        print("session ip_address count " + str(session[ip_address]))

    current_time = time.time()
    time_elapsed = current_time - session[ip_address]["timestamp"]
    print("time elapsed: " + str(time_elapsed) )

    # Reset the count if the time window has passed
    if time_elapsed > TIME_WINDOW:
        session[ip_address]["count"] = 0
        session[ip_address]["timestamp"] = current_time

    # Check if the IP has exceeded the submission limit
    if session[ip_address]["count"] >= MAX_SUBMISSIONS:
        return jsonify({"success": False, "message": "Rate limit exceeded. Please try again later."}), 429

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

    # Increment the submission count for this IP address
    session[ip_address]["count"] += 1

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