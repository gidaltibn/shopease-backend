from flask import Flask, request  # Adicionando request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.models import db
from app.controllers.auth_controller import auth_bp
from app.controllers.cart_controller import cart_bp
from app.controllers.product_controller import product_bp
from app.controllers.order_controller import order_bp

def create_app():
    app = Flask(__name__)
    
    # Configurar o CORS para todas as rotas
    CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*", "methods": ["GET", "POST", "DELETE", "PUT", "OPTIONS"]}})

    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # Registrar os blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)

    # Adicionar tratamento para requisições OPTIONS (preflight)
    @app.before_request
    def handle_preflight():
        if request.method == 'OPTIONS':
            response = app.response_class()
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
            return response, 200

    return app
