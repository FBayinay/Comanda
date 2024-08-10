from flask import Flask

class RouteApp:
    def init_app(self, app):
        from .home_route import home
        from .role_routes import role_routes  
        from .action_routes import action_routes
        
        app.register_blueprint(home, url_prefix='/home')
        app.register_blueprint(role_routes, url_prefix='/api')
        app.register_blueprint(action_routes,url_prefix='/api')
