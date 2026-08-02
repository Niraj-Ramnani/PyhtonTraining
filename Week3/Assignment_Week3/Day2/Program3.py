# 3. Create endpoints demonstrating HTTP 200, 201, 400, 401, 404 and 500 status codes with explanations.
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/success")
def success():
    return jsonify({
        "message": "Everything is OK"
    }), 200


@app.route("/created", methods=["POST"])
def created():
    return jsonify({
        "message": "Resource Created Successfully"
    }), 201


@app.route("/bad-request")
def bad_request():
    return jsonify({
        "error": "Bad Request"
    }), 400


@app.route("/unauthorized")
def unauthorized():
    return jsonify({
        "error": "Unauthorized"
    }), 401


@app.route("/not-found")
def not_found():
    return jsonify({
        "error": "Resource Not Found"
    }), 404


@app.route("/internal-error")
def internal_error():
    return jsonify({
        "error": "Internal Server Error"
    }), 500


if __name__ == "__main__":
    app.run(debug=True)