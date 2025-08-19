import pytest
from db import db
from models.user_model import UserModel
from models.restaurant_model import RestaurantModel

@pytest.fixture(scope="module")
def test_app():
    from flask import Flask

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def session(test_app):
    with test_app.app_context():
        yield db.session


def test_create_restaurant_with_owner(session):
    user = UserModel(name="Carlos", email="carlos@email.com", password="123")
    session.add(user)
    session.commit()

    rest = RestaurantModel(name="Restaurante do Carlos", owner=user)
    session.add(rest)
    session.commit()

    saved_rest = RestaurantModel.query.filter_by(name="Restaurante do Carlos").first()

    assert saved_rest is not None
    assert saved_rest.owner_id == user.id
    assert saved_rest.owner.name == "Carlos"
    assert user.restaurants[0].name == "Restaurante do Carlos"


def test_restaurant_without_owner_should_fail(session):
    rest = RestaurantModel(name="Restaurante sem dono", owner_id=None)
    session.add(rest)

    with pytest.raises(Exception):
        session.commit()
    session.rollback()
