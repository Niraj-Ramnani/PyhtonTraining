from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from db import init_db

from app.routes.auth_routes import auth_bp
from app.routes.restaurant_routes import restaurant_bp
from app.routes.food_routes import food_bp
from app.routes.order_routes import order_bp
from app.routes.profile_routes import profile_bp
from app.routes.report_routes import report_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    JWTManager(app)

    init_db()

    app.register_blueprint(auth_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(order_bp, url_prefix="/orders", name="orders_direct")
    app.register_blueprint(profile_bp)
    app.register_blueprint(report_bp)

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok"}), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app
