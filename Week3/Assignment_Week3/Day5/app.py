# 3. Mini Project: Online Food Ordering REST backend with Authentication, Restaurants, Menu, Orders, User Profile, JWT, validation and proper HTTP status codes.
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "secret"
jwt = JWTManager(app)

users = []
restaurants = []
menus = []
orders = []


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body required"}), 400

    required = ["name", "email", "password"]

    for field in required:
        if field not in data:
            return jsonify({"error": f"{field} required"}), 400

    for user in users:
        if user["email"] == data["email"]:
            return jsonify({"error": "Email already exists"}), 400

    user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"],
        "password": generate_password_hash(data["password"])
    }

    users.append(user)

    return jsonify({"message": "User registered"}), 201



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
                    identity=str(user["id"])
                )

                return jsonify({
                    "token": token
                }), 200


    return jsonify({
        "error": "Invalid credentials"
    }), 401



@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = int(get_jwt_identity())

    for user in users:

        if user["id"] == user_id:

            return jsonify({
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }), 200


    return jsonify({
        "error": "User not found"
    }), 404



@app.route("/restaurants", methods=["POST"])
@jwt_required()
def add_restaurant():

    data = request.get_json()

    if "name" not in data:
        return jsonify({
            "error":"Restaurant name required"
        }),400


    restaurant = {
        "id":len(restaurants)+1,
        "name":data["name"]
    }


    restaurants.append(restaurant)

    return jsonify(restaurant),201



@app.route("/restaurants", methods=["GET"])
def get_restaurants():

    return jsonify(restaurants),200



@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):

    for restaurant in restaurants:

        if restaurant["id"] == id:
            return jsonify(restaurant),200


    return jsonify({
        "error":"Restaurant not found"
    }),404



@app.route("/menu", methods=["POST"])
@jwt_required()
def add_menu_item():

    data=request.get_json()

    required=[
        "restaurant_id",
        "name",
        "price"
    ]

    for field in required:

        if field not in data:
            return jsonify({
                "error":f"{field} required"
            }),400


    if data["price"] < 0:
        return jsonify({
            "error":"Price cannot be negative"
        }),400


    item={
        "id":len(menus)+1,
        "restaurant_id":data["restaurant_id"],
        "name":data["name"],
        "price":data["price"]
    }


    menus.append(item)

    return jsonify(item),201



@app.route("/menu/<int:restaurant_id>", methods=["GET"])
def get_menu(restaurant_id):

    result=[]

    for item in menus:

        if item["restaurant_id"] == restaurant_id:
            result.append(item)


    return jsonify(result),200



@app.route("/orders", methods=["POST"])
@jwt_required()
def create_order():

    user_id=int(get_jwt_identity())

    data=request.get_json()


    if "items" not in data:
        return jsonify({
            "error":"Items required"
        }),400


    total=0

    for item_id in data["items"]:

        for menu in menus:

            if menu["id"] == item_id:
                total += menu["price"]



    order={

        "id":len(orders)+1,

        "user_id":user_id,

        "items":data["items"],

        "total":total,

        "status":"placed"

    }


    orders.append(order)


    return jsonify(order),201



@app.route("/orders", methods=["GET"])
@jwt_required()
def get_orders():

    user_id=int(get_jwt_identity())

    user_orders=[]


    for order in orders:

        if order["user_id"] == user_id:
            user_orders.append(order)


    return jsonify(user_orders),200



@app.route("/orders/<int:id>", methods=["GET"])
@jwt_required()
def get_order(id):

    user_id=int(get_jwt_identity())


    for order in orders:

        if order["id"] == id and order["user_id"] == user_id:

            return jsonify(order),200



    return jsonify({
        "error":"Order not found"
    }),404

#---Main Program---#

if __name__=="__main__":
    app.run(debug=True)