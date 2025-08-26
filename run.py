from flask import Flask
from flask_cors import CORS
from db import db
from controllers.menu_controller import menu_bp
from controllers.dish_controller import dish_bp
from controllers.restaurant_controller import restaurant_bp
from controllers.user_controllers import user_bp

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    CORS(app)  
    app.register_blueprint(menu_bp)
    app.register_blueprint(dish_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(user_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
