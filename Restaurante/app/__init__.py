from pathlib import Path
import os
from dotenv import load_dotenv
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.route import RouteApp
from app.config import config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app() -> None:
    """
    Using an Application Factory
    Ref: Book Flask Web Development Page 78
    """
    # Cargar variables de entorno
    basedir = Path(__file__).resolve().parent.parent / 'docker'
    load_dotenv(basedir / '.env')

    app_context = os.getenv('FLASK_CONTEXT')
    print(f"app_context: {app_context}")
    
    # Crear la aplicación Flask
    app = Flask(__name__)
    config_class = config.factory(app_context)
    app.config.from_object(config_class)
    
    # Inicialización de extensiones
    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    route_app = RouteApp()
    route_app.init_app(app)

    # Importación de los modelos
    with app.app_context():
        from app.models import (
            Role, Action, User, Login, Product, Stock, Supplier, Order,
            WarehouseMovement, Table, MenuCategory, Menu, MenuItem, Command,
            CommandDetail, Receipt
        )
        # Crear todas las tablas si no existen
        db.create_all()
    
    @app.shell_context_processor    
    def ctx():
        return {"app": app, "db": db}
    
    return app
