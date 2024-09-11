from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager  # Importar JWTManager
from flask_cors import CORS
from app.models import db
from app.controllers.auth_controller import auth_bp
from app.controllers.cart_controller import cart_bp
from app.controllers.product_controller import product_bp 
from app.controllers.order_controller import order_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')

    # Inicializar o banco de dados e JWT
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(product_bp) 
    app.register_blueprint(order_bp)

    return app

