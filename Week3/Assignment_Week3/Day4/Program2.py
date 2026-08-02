# 2. Role-based authorization for Admin and User.
from flask import Flask, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt
)
from functools import wraps


app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = "secret"

jwt = JWTManager(app)



users = [

    {
        "id":1,
        "username":"admin",
        "role":"admin"
    },

    {
        "id":2,
        "username":"user1",
        "role":"user"
    }

]



def role_required(role):

    def decorator(function):

        @wraps(function)

        def wrapper(*args, **kwargs):

            claims = get_jwt()


            if claims["role"] != role:

                return jsonify({

                    "error":"Access denied"

                }),403


            return function(*args, **kwargs)


        return wrapper

    return decorator


@app.route("/login/<int:id>")
def login(id):

    for user in users:

        if user["id"] == id:


            token = create_access_token(

                identity=user["id"],

                additional_claims={

                    "role":user["role"]

                }

            )


            return jsonify({

                "token":token

            })


    return jsonify({

        "error":"User not found"

    }),404



@app.route("/profile")
@jwt_required()
def profile():

    return jsonify({

        "message":"Anyone logged in can access"

    })




@app.route("/admin/dashboard")
@jwt_required()
@role_required("admin")
def admin_dashboard():

    return jsonify({

        "message":"Welcome Admin"

    })



if __name__ == "__main__":
    app.run(debug=True)