from flask import Blueprint, jsonify
from app.services import report_service
from app.utils.decorators import admin_required

report_bp = Blueprint("reports", __name__, url_prefix="/api/reports")


@report_bp.route("/highest-spending-customer", methods=["GET"])
@admin_required
def highest_spending_customer():
    return jsonify(report_service.highest_spending_customer()), 200


@report_bp.route("/never-ordered-items", methods=["GET"])
@admin_required
def never_ordered_items():
    return jsonify(report_service.never_ordered_items()), 200


@report_bp.route("/restaurants-above-average-orders", methods=["GET"])
@admin_required
def restaurants_above_average_orders():
    return jsonify(report_service.restaurants_above_average_orders()), 200


@report_bp.route("/most-expensive-item-per-restaurant", methods=["GET"])
@admin_required
def most_expensive_item_per_restaurant():
    return jsonify(report_service.most_expensive_item_per_restaurant()), 200


@report_bp.route("/frequent-customers", methods=["GET"])
@admin_required
def frequent_customers():
    return jsonify(report_service.frequent_customers()), 200
