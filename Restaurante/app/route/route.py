class RouteApp:
    def init_app(self, app):
        from app.resources import home,role_routes,action_routes,user_routes,login_routes,table_routes,product_routes,stock_routes,supplier_routes,menu_category_routes,menu_routes,menu_item_routes,command_detail_routes,command_routes,movement_routes,receipt_routes,order_routes        
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
      
    