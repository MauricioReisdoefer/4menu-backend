from flask import Blueprint
from controllers.secao_controller import criar_secao, deletar_secao

secao_bp = Blueprint("secao", __name__, url_prefix="/secao")

secao_bp.route("/create", methods=["POST"])(criar_secao)
secao_bp.route("/delete/<int:secao_id>", methods=["DELETE"])(deletar_secao)