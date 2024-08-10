from flask import Flask
from flask_marshmallow import Marshmallow
import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.route import init_app as init_route_app
from app.config import config


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app() -> None:
    """
    Using an Application Factory
    Ref: Book Flask Web Development Page 78
    """
    app_context = os.getenv('FLASK_CONTEXT')
    print(f"app_context: {app_context}")
    #https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)
    init_route_app(app)
    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    
    
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app
