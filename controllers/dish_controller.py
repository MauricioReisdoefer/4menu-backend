from flask import request, jsonify
from db import db
from models.dish_model import DishModel


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

def delete_dish(dish_id):
    dish = DishModel.query.get(dish_id)
    if not dish:
        return jsonify({"message": "Dish not found"}), 404

    db.session.delete(dish)
    db.session.commit()
    return jsonify({"message": "Dish deleted"}), 200
