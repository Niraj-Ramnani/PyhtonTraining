from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "secretkey"

jwt = JWTManager(app)

users = []


def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            claims = get_jwt()

            if claims["role"] != role:
                return jsonify({"error": "Access denied"}), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body required"}), 400

    required = ["username", "email", "password", "role"]

    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    for user in users:
        if user["email"] == data["email"]:
            return jsonify({"error": "Email already exists"}), 400

    users.append({
        "id": len(users) + 1,
        "username": data["username"],
        "email": data["email"],
        "password": generate_password_hash(data["password"]),
        "role": data["role"]
    })

    return jsonify({"message": "User registered"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    for user in users:
        if user["email"] == data["email"] and check_password_hash(user["password"], data["password"]):
            token = create_access_token(
                identity=str(user["id"]),
                additional_claims={"role": user["role"]}
            )

            return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/user")
@jwt_required()
def user():
    return jsonify({"message": "Welcome User"}), 200


@app.route("/admin")
@jwt_required()
@role_required("admin")
def admin():
    return jsonify({"message": "Welcome Admin"}), 200


if __name__ == "__main__":
    app.run(debug=True)