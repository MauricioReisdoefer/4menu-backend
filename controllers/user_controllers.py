from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from db import db

user_bp = Blueprint("users", __name__, url_prefix="/users")

# Criar usuário
@user_bp.route("/create", methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        user = UserModel(
            name=data["name"],
            email=data["email"],
            password=data["password"]
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Listar todos usuários
@user_bp.route("/list", methods=["GET"])
def get_users():
    users = UserModel.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# Buscar usuário por ID
@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

# Atualizar usuário
@user_bp.route("/update/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if "name" in data:
        user.name = data["name"].strip()
    if "email" in data:
        user.email = UserModel.normalize_email(data["email"])
    if "password" in data:
        user.set_password(data["password"])

    try:
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Deletar usuário
@user_bp.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
