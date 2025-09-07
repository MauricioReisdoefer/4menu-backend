from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from fastjson_db import JsonTable, JsonQuerier
from models.user_model import User

# ---------------------------
# Tabela JSON
# ---------------------------
user_table = JsonTable("tables/users.json", User)
user_querier = JsonQuerier(user_table)

# Criar usuário
def create_user():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email e password são obrigatórios"}), 400

    # Verifica se já existe
    if user_querier.filter(email=email):
        return jsonify({"error": "Usuário já existe"}), 400

    user = User(name=name.strip(), email=email.strip().lower())
    user.set_password(password)
    user_table.insert(user)
    user_table.flush()

    return jsonify(user.__dict__), 201

# Login
def login():
    data = request.get_json() or {}
    username = data.get("name")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "name e password são obrigatórios"}), 400

    user = user_querier.get_first(name=username.strip().lower())
    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciais inválidas"}), 401

    access_token = create_access_token(identity=str(user._id))
    return jsonify({"access_token": access_token, "user": user.__dict__}), 200

# Listar todos usuários
def get_users():
    users = user_table.get_all()
    return jsonify([u.__dict__ for u in users]), 200

# Buscar usuário por ID
def get_user(user_id):
    user = user_querier.get_first(_id=user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.__dict__), 200

# Atualizar usuário
@jwt_required()
def update_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    user = user_querier.get_first(_id=user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json() or {}
    if "name" in data and data["name"]:
        user.name = data["name"].strip()
    if "email" in data and data["email"]:
        user.email = data["email"].strip().lower()
    if "password" in data and data["password"]:
        user.set_password(data["password"])

    user_table.update(user._id, user)
    user_table.flush()
    return jsonify(user.__dict__), 200

# Deletar usuário
@jwt_required()
def delete_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    if not user_table.delete(user_id):
        return jsonify({"error": "User not found"}), 404

    user_table.flush()
    return jsonify({"message": "User deleted"}), 200

@jwt_required()
def viewme():
    # Pega o ID do usuário da JWT
    current_user_id = int(get_jwt_identity())

    # Busca o usuário na tabela
    user = user_querier.get_first(_id=current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Retorna o usuário como JSON
    return jsonify(user.__dict__), 200