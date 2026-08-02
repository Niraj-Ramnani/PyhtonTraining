# 1. Build Flask server with /, /about and /status JSON endpoints.
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "This is home page of assignment 2 "
    })


@app.route("/about")
def about():
    return jsonify({
        "application": "This is about page of assignment 2",
        "version": "question 1"
    })


@app.route("/status")
def status():
    return jsonify({
        "status": "Server is running",
        "code": 200
    })


if __name__ == "__main__":
    app.run(debug=True)