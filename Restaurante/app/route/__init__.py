from .route import bp as route_bp

def init_app(app):
    app.register_blueprint(route_bp)
