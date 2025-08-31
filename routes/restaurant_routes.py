from flask import Blueprint
from controllers.restaurant_controller import (
    create_restaurant,
    get_my_restaurants,
    get_restaurant_by_id,
    get_restaurants,
    update_restaurant,
    delete_restaurant,
)

restaurant_bp = Blueprint("restaurants", __name__, url_prefix="/restaurants")

restaurant_bp.add_url_rule("/add", view_func=create_restaurant, methods=["POST"])
restaurant_bp.add_url_rule("/me", view_func=get_my_restaurants, methods=["GET"])
restaurant_bp.add_url_rule("/<int:_id>", view_func=get_restaurant_by_id, methods=["GET"])
restaurant_bp.add_url_rule("/", view_func=get_restaurants, methods=["GET"])
restaurant_bp.add_url_rule("/update/<int:_id>", view_func=update_restaurant, methods=["PUT"])
restaurant_bp.add_url_rule("/delete/<int:_id>", view_func=delete_restaurant, methods=["DELETE"])
