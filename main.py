from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "revncart is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # Get customer message
    message = data.get("message", "")
    phone = data.get("phone", "unknown")

    print("Customer:", phone)
    print("Message:", message)

    # Simple bot reply
    reply = "Hi! We received your message: " + message

    return jsonify({
        "reply": reply
    })
    from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# ---------------- Email function ----------------
GMAIL_ADDRESS = "your-new-email@gmail.com"
GMAIL_APP_PASSWORD = "your-16-character-app-password"

def send_abandoned_cart_email(customer_email, customer_name, cart_items, checkout_link):
    subject = "You left items in your cart! 🛒"
    body = f"""
    Hi {customer_name},

    We noticed you left the following items in your cart:
    {', '.join(cart_items)}

    Complete your order now before they’re gone!
    Click here to checkout: {checkout_link}

    — Your Store Name
    """
    msg = MIMEMultipart()
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = customer_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, customer_email, msg.as_string())
        server.quit()
        print(f"Email sent to {customer_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# ---------------- Routes ----------------
@app.route("/")
def home():
    return "revncart is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    # Example: Replace these with real Shopify webhook fields
    customer_email = data.get("customer_email")
    customer_name = data.get("customer_name")
    cart_items = data.get("cart_items", [])
    checkout_link = data.get("checkout_link", "https://yourstore.com/cart")

    # Send abandoned cart email
    if customer_email and cart_items:
        send_abandoned_cart_email(customer_email, customer_name, cart_items, checkout_link)

    # Existing bot message part
    message = data.get("message", "")
    phone = data.get("phone", "unknown")

    print("Customer:", phone)
    print("Message:", message)

    reply = "Hi! We received your message: " + message

    return jsonify({
        "reply": reply
    })
