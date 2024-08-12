from flask import Flask

class RouteApp:
    def init_app(self, app):
        from .home_route             import home
        from .role_routes             import role_routes  
        from .action_routes          import action_routes
        from .user_route             import user_routes
        from .login_route            import login_routes
        from .table_route            import table_routes
        from .product_route          import product_routes
        from .stock_route            import stock_routes
        from .supplier_route         import supplier_routes
        from .menu_route             import menu_routes
        from .menu_catergory_route   import menu_category_routes
        from .menu_item_route        import menu_item_routes
        from .command_route          import command_routes
        from .command_detail_route   import command_detail_routes
        from .movement_route         import movement_routes
        from .receipt_route          import receipt_routes
        from .order_route            import order_routes





        
        app.register_blueprint(home, url_prefix='/home')
        app.register_blueprint(role_routes, url_prefix='/api')
        app.register_blueprint(action_routes,url_prefix='/api')
        app.register_blueprint(user_routes, url_prefix='/api')
        app.register_blueprint(login_routes, url_prefix='/api')
        app.register_blueprint(table_routes, url_prefix='/api')
        app.register_blueprint(product_routes, url_prefix='/api')
        app.register_blueprint(stock_routes, url_prefix='/api')
        app.register_blueprint(supplier_routes, url_prefix='/api')
        app.register_blueprint(menu_routes, url_prefix='/api')
        app.register_blueprint(menu_category_routes, url_prefix='/api')
        app.register_blueprint(menu_item_routes, url_prefix='/api')
        app.register_blueprint(command_detail_routes, url_prefix='/api')
        app.register_blueprint(command_routes, url_prefix='/api')
        app.register_blueprint(movement_routes, url_prefix='/api')
        app.register_blueprint(receipt_routes, url_prefix='/api')
        app.register_blueprint(order_routes, url_prefix='/api')
      
    