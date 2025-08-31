from flask import Flask
from flask_cors import CORS
from db import db
from routes.user_routes import user_bp
from routes.restaurant_routes import restaurant_bp
from routes.secao_routes import secao_bp
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)
        
    CORS(app)  
    app.register_blueprint(user_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(secao_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
