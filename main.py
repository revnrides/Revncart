from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# ---------------- EMAIL CONFIG ----------------
GMAIL_ADDRESS = "your-new-email@gmail.com"  # replace with your email
GMAIL_APP_PASSWORD = "your-16-character-app-password"  # replace with your app password

def send_abandoned_cart_email(customer_email, customer_name, cart_items, checkout_link):
    subject = "You left items in your cart 🛒"
    body = f"""
Hi {customer_name},

You left these items in your cart:
{', '.join(cart_items)}

Complete your order here:
{checkout_link}

— Your Store
"""
    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = customer_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, customer_email, msg.as_string())
        server.quit()
        print("Email sent to", customer_email)
    except Exception as e:
        print("Email error:", e)

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return "revncart is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}

    # Abandoned cart data (example: Shopify webhook)
    customer_email = data.get("customer_email")
    customer_name = data.get("customer_name", "Customer")
    cart_items = data.get("cart_items", [])
    checkout_link = data.get("checkout_link", "https://example.com/cart")

    if customer_email and cart_items:
        send_abandoned_cart_email(
            customer_email,
            customer_name,
            cart_items,
            checkout_link
        )

    # Existing bot reply logic
    message = data.get("message", "")
    phone = data.get("phone", "unknown")

    print("Customer:", phone)
    print("Message:", message)

    reply = "Hi! We received your message: " + message

    return jsonify({"reply": reply})

# ---------------- RUN APP (optional local test) ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
