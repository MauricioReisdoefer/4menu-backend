import pytest
from werkzeug.security import check_password_hash
from db import db
from models import UserModel  
from flask import Flask

@pytest.fixture(scope="module")
def test_app():
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

def test_create_user(session):
    user = UserModel(name="Maurício", email="TESTE@EMAIL.COM", password="123456")
    session.add(user)
    session.commit()

    saved_user = UserModel.query.filter_by(email="teste@email.com").first()

    assert saved_user is not None
    assert saved_user.name == "Maurício"
    assert saved_user.email == "teste@email.com"
    assert saved_user.password_hash != "123456"
    assert check_password_hash(saved_user.password_hash, "123456")

def test_check_password(session):
    user = UserModel(name="Outro", email="outro@email.com", password="senhaSegura")
    session.add(user)
    session.commit()

    saved_user = UserModel.query.filter_by(email="outro@email.com").first()

    assert saved_user.check_password("senhaSegura") is True
    assert saved_user.check_password("errada") is False

def test_to_dict(session):
    user = UserModel(name="TesteDict", email="dict@email.com", password="123")
    session.add(user)
    session.commit()

    saved_user = UserModel.query.filter_by(email="dict@email.com").first()
    user_dict = saved_user.to_dict()

    assert "id" in user_dict
    assert user_dict["name"] == "TesteDict"
    assert user_dict["email"] == "dict@email.com"
    assert "created_at" in user_dict
    assert "updated_at" in user_dict
