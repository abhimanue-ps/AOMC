from flask import Flask, request, jsonify
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def home():
    return "AOMC Backend Running with Config!"

@app.route("/add", methods=["GET"])
def add_numbers():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)
    if a is None or b is None:
        return jsonify({"error": "Please provide both numbers"}), 400
    return jsonify({"result": a + b})

@app.route("/subtract", methods=["GET"])
def subtract_numbers():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)
    if a is None or b is None:
        return jsonify({"error": "Please provide both numbers"}), 400
    return jsonify({"result": a - b})

@app.route("/multiply", methods=["GET"])
def multiply_numbers():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)
    if a is None or b is None:
        return jsonify({"error": "Please provide both numbers"}), 400
    return jsonify({"result": a * b})

@app.route("/divide", methods=["GET"])
def divide_numbers():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)
    if a is None or b is None:
        return jsonify({"error": "Please provide both numbers"}), 400
    if b == 0:
        return jsonify({"error": "Division by zero is not allowed"}), 400
    return jsonify({"result": a / b})

if __name__ == "__main__":
    app.run()

