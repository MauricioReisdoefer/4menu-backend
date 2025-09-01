from flask import Blueprint
from controllers.item_controller import criar_item, deletar_item, get_item

item_bp = Blueprint("items", __name__, url_prefix="/item")

item_bp.route("/create", methods=["POST"])(criar_item)
item_bp.route("/delete/<int:secao_id>", methods=["DELETE"])(deletar_item)
item_bp.route("/get/<int:secao_id>", methods=["GET"])(get_item)