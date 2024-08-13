from flask import Blueprint, request, jsonify
from app.mapping import MenuItemSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.menu_item_services import MenuItemService

menu_item_routes = Blueprint('menu_item_routes', __name__)
menu_item_schema = MenuItemSchema()
response_schema = ResponseSchema()
menu_item_service = MenuItemService()

@menu_item_routes.route('/menu-items', methods=['POST'])
def create_menu_item():
    data = request.json
    if not all(key in data for key in ('id_menu', 'id_categoria', 'nombre', 'precio')):
        return jsonify({"error": "Datos incompletos"}), 400

    response_builder = ResponseBuilder()
    try:
        new_item = menu_item_service.create_item(
            id_menu=data['id_menu'],
            id_categoria=data['id_categoria'],
            nombre=data['nombre'],
            precio=data['precio'],
            descripcion=data.get('descripcion')
        )
        response_builder.add_message("Menu item created").add_status_code(100).add_data(menu_item_schema.dump(new_item))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

@menu_item_routes.route('/menu-items', methods=['GET'])
def get_menu_items():
    response_builder = ResponseBuilder()
    items = menu_item_service.get_all_items()
    response_builder.add_message("Menu items retrieved").add_status_code(100).add_data([menu_item_schema.dump(item) for item in items])
    return response_schema.dump(response_builder.build()), 200

@menu_item_routes.route('/menu-items/<int:id>', methods=['GET'])
def get_menu_item(id: int):
    response_builder = ResponseBuilder()
    item = menu_item_service.get_item_by_id(id)
    if item:
        response_builder.add_message("Menu item found").add_status_code(100).add_data(menu_item_schema.dump(item))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Menu item not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

@menu_item_routes.route('/menu-items/<int:id>', methods=['PUT'])
def update_menu_item(id: int):
    data = request.json
    response_builder = ResponseBuilder()
    try:
        updated_item = menu_item_service.update_item(
            id,
            id_menu=data.get('id_menu'),
            id_categoria=data.get('id_categoria'),
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            precio=data.get('precio')
        )
        if updated_item:
            response_builder.add_message("Menu item updated").add_status_code(100).add_data(menu_item_schema.dump(updated_item))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Menu item not found").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

@menu_item_routes.route('/menu-items/<int:id>', methods=['DELETE'])
def delete_menu_item(id: int):
    response_builder = ResponseBuilder()
    menu_item_service.delete_item(id)
    response_builder.add_message("Menu item deleted").add_status_code(100).add_data({'id': id})
    return response_schema.dump(response_builder.build()), 204
