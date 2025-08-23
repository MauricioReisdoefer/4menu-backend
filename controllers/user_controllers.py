from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from models.user_model import UserModel
from db import db
from datetime import timedelta

user_bp = Blueprint("users", __name__, url_prefix="/users")

# Criar usuário
@user_bp.route("/create", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    try:
        user = UserModel(
            name=data["name"].strip(),
            email=UserModel.normalize_email(data["email"]),
        )
        user.set_password(data["password"])  
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# Login (gera JWT)
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email e password são obrigatórios"}), 400

    user = UserModel.query.filter_by(
        email=UserModel.normalize_email(email)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciais inválidas"}), 401

    # identity = id do usuário
    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(hours=8)
    )
    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200


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


# Atualizar usuário (precisa estar logado e ser o próprio dono)
@user_bp.route("/update/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json() or {}
    if "name" in data and data["name"] is not None:
        user.name = data["name"].strip()
    if "email" in data and data["email"] is not None:
        user.email = UserModel.normalize_email(data["email"])
    if "password" in data and data["password"]:
        user.set_password(data["password"])

    try:
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# Deletar usuário (precisa estar logado e ser o próprio dono)
@user_bp.route("/delete/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

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