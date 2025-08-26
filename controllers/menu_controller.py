from flask import Blueprint, request, jsonify
from models.menu_model import MenuModel
from services.menu_service import (
    create_menu,
    get_all_menus,
    get_menu_by_id,
    update_menu,
    delete_menu
)

menu_bp = Blueprint("menus", __name__, url_prefix="/menus")


# Criar um menu
@menu_bp.route("/", methods=["POST"])
def create_menu_route():
    data = request.get_json()
    name = data.get("name")
    restaurant_id = data.get("restaurant_id")

    if not name or not restaurant_id:
        return jsonify({"error": "Nome e restaurant_id são obrigatórios"}), 400

    new_menu = create_menu(name, restaurant_id)
    return jsonify({
        "id": new_menu.id,
        "name": new_menu.name,
        "restaurant_id": new_menu.restaurant_id
    }), 201


# Buscar todos os menus
@menu_bp.route("/", methods=["GET"])
def get_all_menus_route():
    menus = get_all_menus()
    return jsonify([
        {"id": menu.id, "name": menu.name, "restaurant_id": menu.restaurant_id}
        for menu in menus
    ]), 200


# Buscar um menu por id
@menu_bp.route("/<int:menu_id>", methods=["GET"])
def get_menu_by_id_route(menu_id):
    menu = get_menu_by_id(menu_id)
    if not menu:
        return jsonify({"error": "Menu não encontrado"}), 404
    return jsonify({
        "id": menu.id,
        "name": menu.name,
        "restaurant_id": menu.restaurant_id
    }), 200


# Atualizar um menu
@menu_bp.route("/<int:menu_id>", methods=["PUT"])
def update_menu_route(menu_id):
    data = request.get_json()
    name = data.get("name")
    restaurant_id = data.get("restaurant_id")

    updated_menu = update_menu(menu_id, name, restaurant_id)
    if not updated_menu:
        return jsonify({"error": "Menu não encontrado"}), 404

    return jsonify({
        "id": updated_menu.id,
        "name": updated_menu.name,
        "restaurant_id": updated_menu.restaurant_id
    }), 200


# Deletar um menu
@menu_bp.route("/<int:menu_id>", methods=["DELETE"])
def delete_menu_route(menu_id):
    success = delete_menu(menu_id)
    if not success:
        return jsonify({"error": "Menu não encontrado"}), 404
    return jsonify({"message": "Menu deletado com sucesso"}), 200