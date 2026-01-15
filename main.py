from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)

DB = "data.json"

def load():
    try:
        with open(DB) as f:
            return json.load(f)
    except:
        return {"carts": []}

def save(data):
    with open(DB, "w") as f:
        json.dump(data, f)

@app.route("/")
def home():
    return "RevnCart is running"

@app.route("/cart", methods=["POST"])
def cart():
    data = load()
    cart = request.json
    cart["time"] = int(time.time())
    cart["status"] = "abandoned"
    data["carts"].append(cart)
    save(data)
    return jsonify({"ok": True})

@app.route("/recover")
def recover():
    data = load()
    recovered = []
    for c in data["carts"]:
        if c["status"] == "abandoned":
            recovered.append(c)
    return jsonify(recovered)

app.run(host="0.0.0.0", port=10000)
