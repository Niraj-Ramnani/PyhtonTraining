from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import profile_service
from app.utils.validators import require_fields

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@profile_bp.route("", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    profile = profile_service.get_profile(user_id)
    if profile is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(profile), 200


@profile_bp.route("", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, ["name"])
    if missing:
        return jsonify({"error": "name is required"}), 400

    updated = profile_service.update_profile(user_id, data["name"], data.get("phone"))
    return jsonify(updated), 200
