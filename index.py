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
import datetime

from flask_session.sessions import RedisSessionInterface #monkey patch


app = Flask(__name__)

app.secret_key = os.getenv("mafteah_sod")


CORS(app, resources={r"/validate-captcha": {"origins": "https://www.prepforinterviews.com"}})

RECAPTCHA_SECRET_KEY = "6LcXxroqAAAAAGeX9BkQ5oAxyKeeyoGPpesYUQkL"
GMAIL_USER = os.getenv("doar_ktovet")
GMAIL_PASSWORD = os.getenv("doar_sisma")

REDIS_TOKEN = os.getenv("redis_token")
REDIS_URL = os.getenv("redis_url")
REDIS_PORT = os.getenv("redis_port")

redis_instance = Redis(url=REDIS_URL, token=REDIS_TOKEN)
# Key prefix for session keys
key_prefix = "flask_session:"


print("Redis: " + str(REDIS_URL) + " and " + str(REDIS_TOKEN))

# redis_client = Redis(
#     url=REDIS_URL,  # Replace with your Upstash Redis URL
#     token=REDIS_TOKEN             # Replace with your Upstash token
# )
#
# print("redis_client: " + str(redis_client))

# Configure Redis session management
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "rate_limiting:"  # Optional, used to prefix session keys
app.config["SESSION_REDIS"] = redis_instance

# Initialize Flask-Session extension
Session(app)

# Maximum allowed submissions per IP within the time window
MAX_SUBMISSIONS = 2
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

    # Track submissions per session
    if ip_address not in session:
        session[ip_address] = {"count": 0, "timestamp": time.time()}

    current_time = time.time()
    time_elapsed = current_time - session[ip_address]["timestamp"]

    # Reset the count if the time window has passed
    if time_elapsed > TIME_WINDOW:
        session[ip_address]["count"] = 0
        session[ip_address]["timestamp"] = current_time

    # Check if the IP has exceeded the submission limit
    if session[ip_address]["count"] >= MAX_SUBMISSIONS:
        return jsonify({"success": False, "message": "Rate limit exceeded. Please try again later."}), 429

    # Increment the submission count for this IP address
    session[ip_address]["count"] += 1

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

#Monkey Patch Flask-Session: If you don't want to modify the library code directly, you can apply a monkey patch in your Flask app:
class PatchedRedisSessionInterface(RedisSessionInterface):
    def save_session(self, app, session, response):
        if not session:
            self.redis.delete(self.key_prefix + session.sid)
            return
        if not session.modified:
            return

        expiration_time = self.get_expiration_time(app, session)

        if expiration_time is None:
            total_seconds = 86400  # Default to 1 day (in seconds)
        elif isinstance(expiration_time, datetime.datetime):
            if expiration_time.tzinfo is not None:
                expiration_time = expiration_time.replace(tzinfo=None)
            current_time = datetime.datetime.utcnow()
            total_seconds = (expiration_time - current_time).total_seconds()
        else:
            total_seconds = expiration_time.total_seconds()

        total_seconds = max(0, int(total_seconds))

        # Serialize session data
        val = self.serializer.dumps(dict(session))

        # Correctly call setex with positional arguments
        self.redis.setex(self.key_prefix + session.sid, total_seconds, val)

# Configure the app to use the patched Redis session interface
app.session_interface = PatchedRedisSessionInterface(redis_instance, key_prefix)

if __name__ == "__main__":
    app.run(debug=True)