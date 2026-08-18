from flask import Blueprint, request, jsonify
from app.services import food_service
from app.utils.validators import require_fields, is_positive_number
from app.utils.decorators import admin_required

food_bp = Blueprint("food_items", __name__, url_prefix="/api/food-items")


@food_bp.route("", methods=["GET"])
def list_food_items():
    restaurant_id = request.args.get("restaurant_id", type=int)
    category_id = request.args.get("category_id", type=int)
    return jsonify(food_service.get_food_items(restaurant_id, category_id)), 200


@food_bp.route("/<int:food_item_id>", methods=["GET"])
def get_food_item(food_item_id):
    item = food_service.get_food_item_by_id(food_item_id)
    if item is None:
        return jsonify({"error": "Food item not found"}), 404
    return jsonify(item), 200


@food_bp.route("", methods=["POST"])
@admin_required
def create_food_item():
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["restaurant_id", "category_id", "name", "price"])
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    if not is_positive_number(data["price"]):
        return jsonify({"error": "Price must be a positive number"}), 400

    item = food_service.create_food_item(
        restaurant_id=data["restaurant_id"],
        category_id=data["category_id"],
        name=data["name"],
        price=data["price"],
        is_available=data.get("is_available", 1),
    )
    return jsonify(item), 201


@food_bp.route("/<int:food_item_id>", methods=["PUT"])
@admin_required
def update_food_item(food_item_id):
    existing = food_service.get_food_item_by_id(food_item_id)
    if existing is None:
        return jsonify({"error": "Food item not found"}), 404

    data = request.get_json(silent=True) or {}
    price = data.get("price", existing["price"])
    if not is_positive_number(price):
        return jsonify({"error": "Price must be a positive number"}), 400

    updated = food_service.update_food_item(
        food_item_id,
        name=data.get("name", existing["name"]),
        price=price,
        is_available=data.get("is_available", existing["is_available"]),
    )
    return jsonify(updated), 200


@food_bp.route("/<int:food_item_id>", methods=["DELETE"])
@admin_required
def delete_food_item(food_item_id):
    deleted = food_service.delete_food_item(food_item_id)
    if not deleted:
        return jsonify({"error": "Food item not found"}), 404
    return jsonify({"message": "Food item deleted"}), 200


@food_bp.route("/categories", methods=["GET"])
def list_categories():
    return jsonify(food_service.get_all_categories()), 200
