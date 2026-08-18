from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import order_service
from app.utils.validators import require_fields, is_valid_payment_method

order_bp = Blueprint("orders", __name__, url_prefix="/api/orders")


@order_bp.route("", methods=["POST"])
@jwt_required(optional=True)
def create_order():
    data = request.get_json(silent=True) or {}

    jwt_user_id = get_jwt_identity()
    user_id = data.get("customer_id") or data.get("user_id")
    if user_id is None and jwt_user_id is not None:
        user_id = int(jwt_user_id)

    if user_id is None:
        return jsonify({"error": "customer_id (or user_id) is required or you must provide an Authorization token"}), 400

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"error": "customer_id must be a valid integer"}), 400

    restaurant_id = data.get("restaurant_id")
    if restaurant_id is None:
        return jsonify({"error": "restaurant_id is required"}), 400
    try:
        restaurant_id = int(restaurant_id)
    except (ValueError, TypeError):
        return jsonify({"error": "restaurant_id must be a valid integer"}), 400

    items = data.get("items") or data.get("food_items")
    if not items or not isinstance(items, list) or len(items) == 0:
        return jsonify({"error": "items (or food_items) must be a non-empty list"}), 400

    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            return jsonify({"error": f"Item at index {idx} must be an object with food_item_id and quantity"}), 400
        food_item_id = item.get("food_item_id") or item.get("id")
        if food_item_id is None:
            return jsonify({"error": f"Item at index {idx} is missing food_item_id"}), 400
        quantity = item.get("quantity")
        if quantity is None or not isinstance(quantity, int) or quantity <= 0:
            return jsonify({"error": f"Item at index {idx} has invalid quantity. Must be a positive integer"}), 400

    payment_info = data.get("payment_information") or data.get("payment_info") or data.get("payment_method") or "cash"
    if isinstance(payment_info, dict):
        payment_method = payment_info.get("payment_method") or payment_info.get("method") or "cash"
    else:
        payment_method = str(payment_info)

    payment_method = payment_method.strip().lower()
    if not is_valid_payment_method(payment_method):
        return jsonify({"error": f"Invalid payment_method '{payment_method}'. Allowed values: 'cash', 'card', 'upi'"}), 400

    try:
        order = order_service.create_order(
            user_id=user_id,
            restaurant_id=restaurant_id,
            items=items,
            payment_method=payment_method,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to create order: {str(e)}"}), 500

    response_payload = {
        "message": "Order created successfully",
        "order_id": order["order_id"],
        "order_status": order["order_status"],
        "customer_id": order["user_id"],
        "restaurant_id": order["restaurant_id"],
        "total_amount": order["total_amount"],
        "items": order["items"],
        "payment": order.get("payment"),
        "created_at": order["created_at"].isoformat() if hasattr(order["created_at"], "isoformat") else str(order["created_at"]),
    }

    return jsonify(response_payload), 201



@order_bp.route("", methods=["GET"])
@jwt_required()
def list_my_orders():
    user_id = int(get_jwt_identity())
    return jsonify(order_service.get_orders_for_user(user_id)), 200


@order_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    lookup_user_id = None if claims.get("role") == "admin" else user_id

    order = order_service.get_order_by_id(order_id, user_id=lookup_user_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order), 200


@order_bp.route("/<int:order_id>/status", methods=["PUT"])
@jwt_required()
def update_order_status(order_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["status"])
    if missing:
        return jsonify({"error": "status is required"}), 400

    valid_statuses = ["pending", "confirmed", "delivered", "cancelled"]
    if data["status"] not in valid_statuses:
        return jsonify({"error": f"status must be one of {valid_statuses}"}), 400

    updated = order_service.update_order_status(order_id, data["status"])
    if updated is None:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(updated), 200
