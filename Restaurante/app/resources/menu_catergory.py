from flask import Blueprint, request, jsonify
from app.repositories import MenuCategoryRepository
from app.models import MenuCategory

menu_category_routes = Blueprint('menu_category_routes', __name__)
menu_category_repo = MenuCategoryRepository()

# Crear una nueva categoría de menú (Create)
@menu_category_routes.route('/menu-categories', methods=['POST'])
def create_menu_category():
    data = request.json
    new_category = MenuCategory(categoria=data['categoria'], descripcion=data['descripcion'])
    saved_category = menu_category_repo.save(new_category)
    return jsonify({"id": saved_category.id_categoria, "categoria": saved_category.categoria, "descripcion": saved_category.descripcion}), 201

# Obtener todas las categorías de menú (Read)
@menu_category_routes.route('/menu-categories', methods=['GET'])
def get_menu_categories():
    categories = menu_category_repo.all()
    return jsonify([{"id": category.id_categoria, "categoria": category.categoria, "descripcion": category.descripcion} for category in categories])

# Obtener una categoría de menú por ID (Read)
@menu_category_routes.route('/menu-categories/<int:id>', methods=['GET'])
def get_menu_category(id):
    category = menu_category_repo.find(id)
    if category:
        return jsonify({"id": category.id_categoria, "categoria": category.categoria, "descripcion": category.descripcion})
    return jsonify({"error": "MenuCategory not found"}), 404

# Actualizar una categoría de menú existente (Update)
@menu_category_routes.route('/menu-categories/<int:id>', methods=['PUT'])
def update_menu_category(id):
    data = request.json
    category = MenuCategory(categoria=data['categoria'], descripcion=data['descripcion'])
    updated_category = menu_category_repo.update(category, id)
    if updated_category:
        return jsonify({"id": updated_category.id_categoria, "categoria": updated_category.categoria, "descripcion": updated_category.descripcion})
    return jsonify({"error": "MenuCategory not found"}), 404

# Eliminar una categoría de menú (Delete)
@menu_category_routes.route('/menu-categories/<int:id>', methods=['DELETE'])
def delete_menu_category(id):
    menu_category_repo.delete(id)
    return jsonify({"message": "MenuCategory deleted"}), 204
