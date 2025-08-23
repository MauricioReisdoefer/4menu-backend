import pytest
from flask import Flask
from db import db
from models.restaurant_model import RestaurantModel
from routes import restaurant_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.register_blueprint(restaurant_bp)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_create_restaurant(client):
    response = client.post("/restaurants/create", json={
        "name": "Pizzaria Teste",
        "owner_id": 1
    })
    data = response.get_json()

    assert response.status_code == 201
    assert data["restaurant"]["name"] == "Pizzaria Teste"
    assert data["restaurant"]["owner_id"] == 1


def test_list_restaurants(client):
    # cria restaurante antes
    client.post("/restaurants/create", json={
        "name": "Sushi House",
        "owner_id": 2
    })

    response = client.get("/restaurants/list")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Sushi House"


def test_get_restaurant_by_id(client):
    # cria restaurante
    res = client.post("/restaurants/create", json={
        "name": "Burger King",
        "owner_id": 3
    })
    created_id = res.get_json()["restaurant"]["id"]

    response = client.get(f"/restaurants/{created_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["name"] == "Burger King"
    assert data["owner_id"] == 3


def test_update_restaurant(client):
    # cria restaurante
    res = client.post("/restaurants/create", json={
        "name": "Padaria Antiga",
        "owner_id": 4
    })
    created_id = res.get_json()["restaurant"]["id"]

    # atualiza
    response = client.put(f"/restaurants/update/{created_id}", json={
        "name": "Padaria Moderna"
    })
    data = response.get_json()

    assert response.status_code == 200
    assert data["restaurant"]["name"] == "Padaria Moderna"


def test_delete_restaurant(client):
    # cria restaurante
    res = client.post("/restaurants/create", json={
        "name": "Churrascaria Gaúcha",
        "owner_id": 5
    })
    created_id = res.get_json()["restaurant"]["id"]

    # deleta
    response = client.delete(f"/restaurants/delete/{created_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Restaurante deletado com sucesso!"

    # confirma que não existe mais
    res = client.get(f"/restaurants/{created_id}")
    assert res.status_code == 404
