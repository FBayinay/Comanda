from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Cargar la configuración desde el archivo .env
    app.config.from_object(os.getenv('APP_SETTINGS', 'app.config.DevelopmentConfig'))

    db.init_app(app)
    migrate.init_app(app, db)

    # Importar los modelos aquí
    from .models import Role, Action, User, Login, Product, Stock, Supplier, Order, WarehouseMovement, Table, MenuCategory, Menu, MenuItem, Command, CommandDetail, Receipt

    with app.app_context():
        from . import routes
        db.create_all()

    return app
