from flask import Blueprint, request, jsonify
from db import db
from models.dish_model import DishModel

dish_bp = Blueprint("dishes", __name__, url_prefix="/dishes")


# GET all dishes
@dish_bp.route("/", methods=["GET"])
def get_dishes():
    dishes = DishModel.query.all()
    return jsonify([
        {
            "id": dish.id,
            "name": dish.name,
            "description": dish.description,
            "price": dish.price,
            "menu_id": dish.menu_id,
        } for dish in dishes
    ]), 200


# GET dish by id
@dish_bp.route("/<int:dish_id>", methods=["GET"])
def get_dish(dish_id):
    dish = DishModel.query.get(dish_id)
    if not dish:
        return jsonify({"message": "Dish not found"}), 404
    return jsonify({
        "id": dish.id,
        "name": dish.name,
        "description": dish.description,
        "price": dish.price,
        "menu_id": dish.menu_id,
    }), 200


# CREATE dish
@dish_bp.route("/", methods=["POST"])
def create_dish():
    data = request.get_json()
    if not data or "name" not in data or "price" not in data or "menu_id" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    new_dish = DishModel(
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        menu_id=data["menu_id"],
    )
    db.session.add(new_dish)
    db.session.commit()

    return jsonify({"message": "Dish created", "id": new_dish.id}), 201


# UPDATE dish
@dish_bp.route("/<int:dish_id>", methods=["PUT"])
def update_dish(dish_id):
    dish = DishModel.query.get(dish_id)
    if not dish:
        return jsonify({"message": "Dish not found"}), 404

    data = request.get_json()
    dish.name = data.get("name", dish.name)
    dish.description = data.get("description", dish.description)
    dish.price = data.get("price", dish.price)
    dish.menu_id = data.get("menu_id", dish.menu_id)

    db.session.commit()
    return jsonify({"message": "Dish updated"}), 200


# DELETE dish
@dish_bp.route("/<int:dish_id>", methods=["DELETE"])
def delete_dish(dish_id):
    dish = DishModel.query.get(dish_id)
    if not dish:
        return jsonify({"message": "Dish not found"}), 404

    db.session.delete(dish)
    db.session.commit()
    return jsonify({"message": "Dish deleted"}), 200
