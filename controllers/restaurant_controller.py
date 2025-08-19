from flask import Blueprint, request, jsonify
from models.restaurant_model import RestaurantModel
from db import db

restaurant_bp = Blueprint("restaurants", __name__, url_prefix="/restaurants")

# Criar restaurante
@restaurant_bp.route("/create", methods=["POST"])
def create_restaurant():
    data = request.get_json()

    if not data or "name" not in data or "owner_id" not in data:
        return jsonify({"error": "Campos obrigatórios: name, owner_id"}), 400

    new_restaurant = RestaurantModel(
        name=data["name"],
        owner_id=data["owner_id"]
    )

    db.session.add(new_restaurant)
    db.session.commit()

    return jsonify({
        "message": "Restaurante criado com sucesso!",
        "restaurant": {
            "id": new_restaurant.id,
            "name": new_restaurant.name,
            "owner_id": new_restaurant.owner_id
        }
    }), 201


# Listar todos restaurantes
@restaurant_bp.route("/list", methods=["GET"])
def get_restaurants():
    restaurants = RestaurantModel.query.all()
    return jsonify([
        {
            "id": r.id,
            "name": r.name,
            "owner_id": r.owner_id
        } for r in restaurants
    ]), 200


# Buscar restaurante por ID
@restaurant_bp.route("/<int:restaurant_id>", methods=["GET"])
def get_restaurant(restaurant_id):
    restaurant = RestaurantModel.query.get(restaurant_id)
    if not restaurant:
        return jsonify({"error": "Restaurante não encontrado"}), 404

    return jsonify({
        "id": restaurant.id,
        "name": restaurant.name,
        "owner_id": restaurant.owner_id
    }), 200


# Atualizar restaurante
@restaurant_bp.route("/update/<int:restaurant_id>", methods=["PUT"])
def update_restaurant(restaurant_id):
    data = request.get_json()
    restaurant = RestaurantModel.query.get(restaurant_id)

    if not restaurant:
        return jsonify({"error": "Restaurante não encontrado"}), 404

    if "name" in data:
        restaurant.name = data["name"]
    if "owner_id" in data:
        restaurant.owner_id = data["owner_id"]

    db.session.commit()

    return jsonify({
        "message": "Restaurante atualizado com sucesso!",
        "restaurant": {
            "id": restaurant.id,
            "name": restaurant.name,
            "owner_id": restaurant.owner_id
        }
    }), 200


# Deletar restaurante
@restaurant_bp.route("/delete/<int:restaurant_id>", methods=["DELETE"])
def delete_restaurant(restaurant_id):
    restaurant = RestaurantModel.query.get(restaurant_id)

    if not restaurant:
        return jsonify({"error": "Restaurante não encontrado"}), 404

    db.session.delete(restaurant)
    db.session.commit()

    return jsonify({"message": "Restaurante deletado com sucesso!"}), 200
