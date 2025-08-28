from flask import Flask
from flask_cors import CORS
from db import db
from controllers.user_controllers import user_bp
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    
    app.config["JWT_SECRET_KEY"] = "fodase"
    jwt = JWTManager(app)
        
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    CORS(app)  
    app.register_blueprint(user_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
