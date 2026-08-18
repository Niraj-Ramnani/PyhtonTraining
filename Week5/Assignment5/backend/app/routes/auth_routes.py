from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services import auth_service
from app.utils.validators import require_fields, is_valid_email

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    missing = require_fields(data, ["name", "email", "password"])
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    if not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email format"}), 400

    if len(data["password"]) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    user_id = auth_service.create_user(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        phone=data.get("phone"),
    )

    if user_id is None:
        return jsonify({"error": "Email is already registered"}), 409

    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    missing = require_fields(data, ["email", "password"])
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    user = auth_service.verify_login(data["email"], data["password"])
    if user is None:
        return jsonify({"error": "Invalid email or password"}), 401

    role_name = auth_service.get_role_name(user["role_id"])
    access_token = create_access_token(
        identity=str(user["user_id"]),
        additional_claims={"role": role_name},
    )

    return jsonify({
        "access_token": access_token,
        "user": {"user_id": user["user_id"], "name": user["name"], "email": user["email"], "role": role_name},
    }), 200
