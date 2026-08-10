import os
import json
from decimal import Decimal
from functools import wraps

import psycopg
from psycopg.rows import dict_row
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


def get_conn():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def db_error_response(exc):
    return jsonify({"error": str(exc)}), 400


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify({"error": "Forbidden"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.post("/register")
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body required"}), 400

    required = ["name", "email", "password"]
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"error": f"{missing[0]} required"}), 400

    if len(data["password"]) < 6:
        return jsonify({"error": "Password must contain at least 6 characters"}), 400

    role_name = data.get("role", "customer").lower()
    if role_name not in {"customer", "restaurant_owner"}:
        return jsonify({"error": "Invalid role"}), 400

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT role_id FROM roles WHERE role_name = %s", (role_name,))
                role = cur.fetchone()
                cur.execute(
                    """
                    INSERT INTO users (role_id, name, email, password_hash, phone)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING user_id, name, email, phone, role_id, is_active, created_at
                    """,
                    (
                        role["role_id"],
                        data["name"].strip(),
                        data["email"].strip().lower(),
                        generate_password_hash(data["password"]),
                        data.get("phone"),
                    ),
                )
                user = cur.fetchone()
                conn.commit()
                return jsonify(user), 201
    except psycopg.errors.UniqueViolation:
        return jsonify({"error": "Email or phone already exists"}), 409
    except Exception as exc:
        return db_error_response(exc)


@app.post("/login")
def login():
    data = request.get_json(silent=True)
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT u.user_id, u.name, u.email, u.password_hash,
                       r.role_name, u.is_active
                FROM users u
                JOIN roles r ON r.role_id = u.role_id
                WHERE u.email = %s
                """,
                (data["email"].strip().lower(),),
            )
            user = cur.fetchone()

    if not user or not user["is_active"] or not check_password_hash(
        user["password_hash"], data["password"]
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(
        identity=str(user["user_id"]),
        additional_claims={"role": user["role_name"], "name": user["name"]},
    )
    return jsonify({"access_token": token}), 200


@app.get("/profile")
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT u.user_id, u.name, u.email, u.phone,
                       r.role_name, u.is_active, u.created_at
                FROM users u
                JOIN roles r ON r.role_id = u.role_id
                WHERE u.user_id = %s
                """,
                (user_id,),
            )
            user = cur.fetchone()

    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@app.get("/restaurants")
def get_restaurants():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT restaurant_id, name, address, phone, is_active,
                       revenue, created_at
                FROM restaurants
                ORDER BY restaurant_id
                """
            )
            return jsonify(cur.fetchall()), 200


@app.get("/restaurants/<int:restaurant_id>")
def get_restaurant(restaurant_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM restaurants WHERE restaurant_id = %s",
                (restaurant_id,),
            )
            restaurant = cur.fetchone()
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(restaurant), 200


@app.post("/restaurants")
@role_required("admin", "restaurant_owner")
def add_restaurant():
    data = request.get_json(silent=True)
    if not data or not data.get("name") or not data.get("address"):
        return jsonify({"error": "Name and address required"}), 400

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO restaurants (name, address, phone)
                    VALUES (%s, %s, %s)
                    RETURNING *
                    """,
                    (data["name"].strip(), data["address"].strip(), data.get("phone")),
                )
                restaurant = cur.fetchone()
                conn.commit()
                return jsonify(restaurant), 201
    except psycopg.errors.UniqueViolation:
        return jsonify({"error": "Restaurant name or phone already exists"}), 409


@app.put("/restaurants/<int:restaurant_id>")
@role_required("admin", "restaurant_owner")
def update_restaurant(restaurant_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body required"}), 400

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE restaurants
                SET name = COALESCE(%s, name),
                    address = COALESCE(%s, address),
                    phone = COALESCE(%s, phone),
                    is_active = COALESCE(%s, is_active)
                WHERE restaurant_id = %s
                RETURNING *
                """,
                (
                    data.get("name"),
                    data.get("address"),
                    data.get("phone"),
                    data.get("is_active"),
                    restaurant_id,
                ),
            )
            restaurant = cur.fetchone()
            if not restaurant:
                return jsonify({"error": "Restaurant not found"}), 404
            conn.commit()
            return jsonify(restaurant), 200


@app.delete("/restaurants/<int:restaurant_id>")
@role_required("admin")
def delete_restaurant(restaurant_id):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM restaurants WHERE restaurant_id = %s RETURNING restaurant_id",
                    (restaurant_id,),
                )
                deleted = cur.fetchone()
                if not deleted:
                    return jsonify({"error": "Restaurant not found"}), 404
                conn.commit()
                return jsonify({"message": "Restaurant deleted"}), 200
    except psycopg.errors.RaiseException as exc:
        conn.rollback()
        return jsonify({"error": str(exc)}), 409


@app.post("/menu")
@role_required("admin", "restaurant_owner")
def add_food_item():
    data = request.get_json(silent=True)
    required = ["restaurant_id", "category_id", "name", "price", "inventory"]
    if not data:
        return jsonify({"error": "Request body required"}), 400
    missing = [field for field in required if field not in data]
    if missing:
        return jsonify({"error": f"{missing[0]} required"}), 400

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO food_items
                        (restaurant_id, category_id, name, description, price, inventory)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *
                    """,
                    (
                        data["restaurant_id"],
                        data["category_id"],
                        data["name"].strip(),
                        data.get("description"),
                        data["price"],
                        data["inventory"],
                    ),
                )
                item = cur.fetchone()
                conn.commit()
                return jsonify(item), 201
    except psycopg.errors.ForeignKeyViolation:
        return jsonify({"error": "Restaurant or category not found"}), 404
    except psycopg.errors.CheckViolation:
        return jsonify({"error": "Invalid price or inventory"}), 400


@app.get("/menu/<int:restaurant_id>")
def get_menu(restaurant_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT f.food_item_id, f.restaurant_id, f.category_id,
                       f.name, f.description, f.price, f.inventory,
                       f.is_available, c.name AS category_name
                FROM food_items f
                JOIN categories c ON c.category_id = f.category_id
                WHERE f.restaurant_id = %s
                ORDER BY f.food_item_id
                """,
                (restaurant_id,),
            )
            return jsonify(cur.fetchall()), 200


@app.put("/menu/<int:food_item_id>")
@role_required("admin", "restaurant_owner")
def update_food_item(food_item_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body required"}), 400

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE food_items
                SET name = COALESCE(%s, name),
                    description = COALESCE(%s, description),
                    price = COALESCE(%s, price),
                    inventory = COALESCE(%s, inventory),
                    is_available = COALESCE(%s, is_available)
                WHERE food_item_id = %s
                RETURNING *
                """,
                (
                    data.get("name"),
                    data.get("description"),
                    data.get("price"),
                    data.get("inventory"),
                    data.get("is_available"),
                    food_item_id,
                ),
            )
            item = cur.fetchone()
            if not item:
                return jsonify({"error": "Food item not found"}), 404
            conn.commit()
            return jsonify(item), 200


@app.delete("/menu/<int:food_item_id>")
@role_required("admin", "restaurant_owner")
def delete_food_item(food_item_id):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM food_items WHERE food_item_id = %s RETURNING food_item_id",
                    (food_item_id,),
                )
                item = cur.fetchone()
                if not item:
                    return jsonify({"error": "Food item not found"}), 404
                conn.commit()
                return jsonify({"message": "Food item deleted"}), 200
    except psycopg.errors.ForeignKeyViolation:
        return jsonify({"error": "Food item is referenced by an order"}), 409


@app.post("/orders")
@jwt_required()
def create_order():
    data = request.get_json(silent=True)
    if not data or not isinstance(data.get("items"), list) or not data["items"]:
        return jsonify({"error": "Non-empty items list required"}), 400

    user_id = int(get_jwt_identity())

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT place_order(%s, %s, %s, %s)", (
                    user_id,
                    data["restaurant_id"],
                    json.dumps(data["items"]),
                    data.get("payment_method", "upi"),
                ))
                result = cur.fetchone()
                conn.commit()
                return jsonify(result), 201
    except psycopg.errors.RaiseException as exc:
        conn.rollback()
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        conn.rollback()
        return db_error_response(exc)


@app.get("/orders")
@jwt_required()
def get_orders():
    user_id = int(get_jwt_identity())
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT o.order_id, o.user_id, o.restaurant_id,
                       r.name AS restaurant_name, o.total_amount,
                       o.status, o.ordered_at
                FROM orders o
                JOIN restaurants r ON r.restaurant_id = o.restaurant_id
                WHERE o.user_id = %s
                ORDER BY o.ordered_at DESC
                """,
                (user_id,),
            )
            return jsonify(cur.fetchall()), 200


@app.get("/orders/<int:order_id>")
@jwt_required()
def get_order(order_id):
    user_id = int(get_jwt_identity())
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM customer_order_history
                WHERE order_id = %s AND user_id = %s
                ORDER BY order_item_id
                """,
                (order_id, user_id),
            )
            rows = cur.fetchall()
    if not rows:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(rows), 200


@app.patch("/orders/<int:order_id>/cancel")
@jwt_required()
def cancel_order(order_id):
    user_id = int(get_jwt_identity())
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT cancel_order(%s, %s)", (order_id, user_id))
                result = cur.fetchone()
                conn.commit()
                return jsonify(result), 200
    except psycopg.errors.RaiseException as exc:
        conn.rollback()
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(debug=True)
