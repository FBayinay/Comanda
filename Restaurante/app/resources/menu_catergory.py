from flask import Blueprint, request, jsonify
from app.mapping import MenuCategorySchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.menu_category_services import MenuCategoryService

menu_category_routes = Blueprint('menu_category_routes', __name__)
menu_category_schema = MenuCategorySchema()
response_schema = ResponseSchema()
menu_category_service = MenuCategoryService()

@menu_category_routes.route('/menu-categories', methods=['POST'])
def create_menu_category():
    data = request.json
    if not all(key in data for key in ('categoria', 'descripcion')):
        return jsonify({"error": "Datos incompletos"}), 400

    response_builder = ResponseBuilder()
    try:
        new_category = menu_category_service.create_category(data['categoria'], data['descripcion'])
        response_builder.add_message("Menu category created").add_status_code(100).add_data(menu_category_schema.dump(new_category))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

@menu_category_routes.route('/menu-categories', methods=['GET'])
def get_menu_categories():
    response_builder = ResponseBuilder()
    categories = menu_category_service.get_all_categories()
    response_builder.add_message("Menu categories retrieved").add_status_code(100).add_data([menu_category_schema.dump(cat) for cat in categories])
    return response_schema.dump(response_builder.build()), 200

@menu_category_routes.route('/menu-categories/<int:id>', methods=['GET'])
def get_menu_category(id: int):
    response_builder = ResponseBuilder()
    category = menu_category_service.get_category_by_id(id)
    if category:
        response_builder.add_message("Menu category found").add_status_code(100).add_data(menu_category_schema.dump(category))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Menu category not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

@menu_category_routes.route('/menu-categories/<int:id>', methods=['PUT'])
def update_menu_category(id: int):
    data = request.json
    response_builder = ResponseBuilder()
    try:
        updated_category = menu_category_service.update_category(
            id,
            categoria=data.get('categoria'),
            descripcion=data.get('descripcion')
        )
        if updated_category:
            response_builder.add_message("Menu category updated").add_status_code(100).add_data(menu_category_schema.dump(updated_category))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Menu category not found").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

@menu_category_routes.route('/menu-categories/<int:id>', methods=['DELETE'])
def delete_menu_category(id: int):
    response_builder = ResponseBuilder()
    menu_category_service.delete_category(id)
    response_builder.add_message("Menu category deleted").add_status_code(100).add_data({'id': id})
    return response_schema.dump(response_builder.build()), 204
