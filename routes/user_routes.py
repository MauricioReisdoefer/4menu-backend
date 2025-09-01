from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.user_controller import (
    create_user,
    login,
    get_users,
    get_user,
    update_user,
    delete_user,
    viewme
)

user_bp = Blueprint("users", __name__, url_prefix="/users")

user_bp.route("/create", methods=["POST"])(create_user)
user_bp.route("/login", methods=["POST"])(login)
user_bp.route("/list", methods=["GET"])(get_users)
user_bp.route("/<int:user_id>", methods=["GET"])(get_user)
user_bp.route("/update/<int:user_id>", methods=["PUT"])(jwt_required()(update_user))
user_bp.route("/delete/<int:user_id>", methods=["DELETE"])(jwt_required()(delete_user))
user_bp.route("/viewme", methods=["GET"])(jwt_required()(viewme))