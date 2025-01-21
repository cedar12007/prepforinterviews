from flask import Flask, request, jsonify, session
from flask_cors import CORS  # Import CORS library
import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_session import Session
from upstash_redis import Redis
import time


app = Flask(__name__)

app.secret_key = os.getenv("mafteah_sod")


CORS(app, resources={r"/validate-captcha": {"origins": "https://www.prepforinterviews.com"}})

RECAPTCHA_SECRET_KEY = "6LcXxroqAAAAAGeX9BkQ5oAxyKeeyoGPpesYUQkL"
GMAIL_USER = os.getenv("doar_ktovet")
GMAIL_PASSWORD = os.getenv("doar_sisma")

REDIS_TOKEN = os.getenv("redis_token")
REDIS_URL = os.getenv("redis_url")
REDIS_PORT = os.getenv("redis_port")
#REDIS_PY_URL=os.getenv("redis_py_url") #redis://...


redis_client = Redis(
    url=REDIS_URL,
    token=REDIS_TOKEN)

# Maximum allowed submissions per IP within the time window
MAX_SUBMISSIONS = 3
TIME_WINDOW = 60 * 5  # 5 minutes in seconds

@app.route("/validate-captcha", methods=["POST"])
def validate_captcha():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")
    recaptcha_response = data.get("g-recaptcha-response")
    #recaptcha_metadata = verify_recaptcha.verify_recaptcha(recaptcha_response)

    ip_address = request.remote_addr  # Get the user's IP address
    recaptcha_response = request.json.get("g-recaptcha-response")

    ip_record = redis_client.get(ip_address)
    print("ip_record: " + str(ip_record))
    current_time = time.time()

    # Track submissions per session
    if ip_record == None:
        print("ip_record doesn't exist")
        redis_client.set(ip_address, "1-" + str(current_time))
    else:
        attempt_count = int(ip_record[0])
        split_string = ip_record.split("-")  # Split by the hyphen
        first_attempt = split_string[1]  # Access the second element (the first timestamp)
        time_stamps = ip_record[ip_record.find("-") + 1:]  # Slice everything after the first hyphen
        print("attempt count: " + str(attempt_count))
        print("first_attempt: " + first_attempt)
        time_elapsed = current_time - float(first_attempt)
        print("time_difference: " + str(time_elapsed))
        if time_elapsed > TIME_WINDOW:
            print("time elapsed, setting ip_address record to zero")
            redis_client.set(ip_address, "1-" + str(current_time))
        elif attempt_count <= MAX_SUBMISSIONS:
            redis_client.set(ip_address, str(attempt_count + 1) + "-" + time_stamps + "-" + str(current_time))
            print("time didn't elapse, add another timestamp.  New record value: " + str(redis_client.get(ip_address)))
        else:
            print("Submission limit exceeded. Please try again later.")
            return jsonify({"success": False, "message": "Submission limit exceeded. Please try again later."}), 429

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