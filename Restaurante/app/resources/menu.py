from flask import Blueprint, request, jsonify
from app.mapping import MenuSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.menu_services import MenuService

menu_routes = Blueprint('menu_routes', __name__)
menu_schema = MenuSchema()
response_schema = ResponseSchema()
menu_service = MenuService()

@menu_routes.route('/menus', methods=['POST'])
def create_menu():
    data = request.json
    if not all(key in data for key in ('tipo', 'fecha_inicio')):
        return jsonify({"error": "Datos incompletos"}), 400

    response_builder = ResponseBuilder()
    try:
        new_menu = menu_service.create_menu(
            tipo=data['tipo'],
            fecha_inicio=data['fecha_inicio'],
            fecha_fin=data.get('fecha_fin')
        )
        response_builder.add_message("Menu created").add_status_code(100).add_data(menu_schema.dump(new_menu))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

@menu_routes.route('/menus', methods=['GET'])
def get_menus():
    response_builder = ResponseBuilder()
    menus = menu_service.get_all_menus()
    response_builder.add_message("Menus retrieved").add_status_code(100).add_data([menu_schema.dump(menu) for menu in menus])
    return response_schema.dump(response_builder.build()), 200

@menu_routes.route('/menus/<int:id>', methods=['GET'])
def get_menu(id: int):
    response_builder = ResponseBuilder()
    menu = menu_service.get_menu_by_id(id)
    if menu:
        response_builder.add_message("Menu found").add_status_code(100).add_data(menu_schema.dump(menu))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Menu not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

@menu_routes.route('/menus/<int:id>', methods=['PUT'])
def update_menu(id: int):
    data = request.json
    response_builder = ResponseBuilder()
    try:
        updated_menu = menu_service.update_menu(
            id,
            tipo=data.get('tipo'),
            fecha_inicio=data.get('fecha_inicio'),
            fecha_fin=data.get('fecha_fin')
        )
        if updated_menu:
            response_builder.add_message("Menu updated").add_status_code(100).add_data(menu_schema.dump(updated_menu))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Menu not found").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

@menu_routes.route('/menus/<int:id>', methods=['DELETE'])
def delete_menu(id: int):
    response_builder = ResponseBuilder()
    menu_service.delete_menu(id)
    response_builder.add_message("Menu deleted").add_status_code(100).add_data({'id': id})
    return response_schema.dump(response_builder.build()), 204
