# 1. Register/Login API with password hashing and JWT/basic token.
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)


app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = "secret"

jwt = JWTManager(app)


users = []



@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    required_fields = [
        "username",
        "email",
        "password"
    ]

    for field in required_fields:

        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400


    for user in users:

        if user["email"] == data["email"]:

            return jsonify({
                "error": "Email already registered"
            }), 400

    hashed_password = generate_password_hash(
        data["password"]
    )


    user = {

        "id": len(users) + 1,

        "username": data["username"],

        "email": data["email"],

        "password": hashed_password

    }


    users.append(user)


    return jsonify({

        "message": "User registered successfully"

    }), 201



@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()


    for user in users:

        if user["email"] == data["email"]:


            if check_password_hash(
                user["password"],
                data["password"]
            ):


                token = create_access_token(
                    identity=user["id"]
                )


                return jsonify({

                    "access_token": token

                })


    return jsonify({

        "error": "Invalid email or password"

    }), 401



@app.route("/profile")
@jwt_required()
def profile():

    user_id = get_jwt_identity()


    return jsonify({

        "message": "Protected route accessed",

        "user_id": user_id

    })


if __name__ == "__main__":
    app.run(debug=True)