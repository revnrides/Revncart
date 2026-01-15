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
