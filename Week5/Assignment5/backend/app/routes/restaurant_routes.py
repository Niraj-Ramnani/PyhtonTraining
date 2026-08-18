from flask import Blueprint, request, jsonify
from app.services import restaurant_service
from app.utils.validators import require_fields
from app.utils.decorators import admin_required

restaurant_bp = Blueprint("restaurants", __name__, url_prefix="/api/restaurants")


@restaurant_bp.route("", methods=["GET"])
def list_restaurants():
    return jsonify(restaurant_service.get_all_restaurants()), 200


@restaurant_bp.route("/<int:restaurant_id>", methods=["GET"])
def get_restaurant(restaurant_id):
    restaurant = restaurant_service.get_restaurant_by_id(restaurant_id)
    if restaurant is None:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(restaurant), 200


@restaurant_bp.route("", methods=["POST"])
@admin_required
def create_restaurant():
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["name", "address"])
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    restaurant = restaurant_service.create_restaurant(
        name=data["name"],
        address=data["address"],
        phone=data.get("phone"),
        rating=data.get("rating", 0),
    )
    return jsonify(restaurant), 201


@restaurant_bp.route("/<int:restaurant_id>", methods=["PUT"])
@admin_required
def update_restaurant(restaurant_id):
    existing = restaurant_service.get_restaurant_by_id(restaurant_id)
    if existing is None:
        return jsonify({"error": "Restaurant not found"}), 404

    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["name", "address"])
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    updated = restaurant_service.update_restaurant(
        restaurant_id,
        name=data["name"],
        address=data["address"],
        phone=data.get("phone", existing["phone"]),
        rating=data.get("rating", existing["rating"]),
    )
    return jsonify(updated), 200


@restaurant_bp.route("/<int:restaurant_id>", methods=["DELETE"])
@admin_required
def delete_restaurant(restaurant_id):
    deleted = restaurant_service.delete_restaurant(restaurant_id)
    if not deleted:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify({"message": "Restaurant deleted"}), 200
