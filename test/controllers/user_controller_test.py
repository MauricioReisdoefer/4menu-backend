import pytest
from flask import Flask
from flask_jwt_extended import JWTManager
from db import db
from controllers.user_controllers import user_bp
from models.user_model import UserModel

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret"

    db.init_app(app)
    JWTManager(app)
    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def created_user(client):
    res = client.post("/users/create", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "123456"
    })
    return res.get_json()


@pytest.fixture
def access_token(client, created_user):
    res = client.post("/users/login", json={
        "email": created_user["email"],
        "password": "123456"
    })
    return res.get_json()["access_token"]


def test_create_user(created_user):
    assert created_user["name"] == "Test User"
    assert "id" in created_user


def test_login(client, created_user):
    res = client.post("/users/login", json={
        "email": created_user["email"],
        "password": "123456"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data
    assert "user" in data


def test_update_user(client, created_user, access_token):
    user_id = created_user["id"]
    res = client.put(f"/users/update/{user_id}",
                     json={"name": "Novo Nome"},
                     headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    assert res.get_json()["name"] == "Novo Nome"


def test_update_user_unauthorized(client, created_user):
    user_id = created_user["id"]
    res = client.put(f"/users/update/{user_id}", json={"name": "Hacker"})
    assert res.status_code == 401


def test_list_users(client, created_user):
    res = client.get("/users/list")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 1


def test_get_user_by_id(client, created_user):
    user_id = created_user["id"]
    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["id"] == user_id


def test_delete_user(client, created_user, access_token):
    user_id = created_user["id"]
    res = client.delete(f"/users/delete/{user_id}",
                        headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    assert res.get_json()["message"] == "User deleted"


def test_user_deleted(client, created_user, access_token):
    user_id = created_user["id"]
    client.delete(f"/users/delete/{user_id}",
                  headers={"Authorization": f"Bearer {access_token}"})
    res = client.get(f"/users/{user_id}")
    assert res.status_code == 404
