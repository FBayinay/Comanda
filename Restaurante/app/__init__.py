import os
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
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)
    
    # Inicialización de extensiones
    route_app = RouteApp()
    route_app.init_app(app)
    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    


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
