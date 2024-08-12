from flask import Blueprint, request, jsonify
from app.repositories import MenuRepository
from app.models import Menu

menu_routes = Blueprint('menu_routes', __name__)
menu_repo = MenuRepository()

# Crear un nuevo menú (Create)
@menu_routes.route('/menus', methods=['POST'])
def create_menu():
    data = request.json
    new_menu = Menu(tipo=data['tipo'], fecha_inicio=data['fecha_inicio'], fecha_fin=data.get('fecha_fin'))
    saved_menu = menu_repo.save(new_menu)
    return jsonify({"id": saved_menu.id_menu, "tipo": saved_menu.tipo, "fecha_inicio": saved_menu.fecha_inicio, "fecha_fin": saved_menu.fecha_fin}), 201

# Obtener todos los menús (Read)
@menu_routes.route('/menus', methods=['GET'])
def get_menus():
    menus = menu_repo.all()
    return jsonify([{"id": menu.id_menu, "tipo": menu.tipo, "fecha_inicio": menu.fecha_inicio, "fecha_fin": menu.fecha_fin} for menu in menus])

# Obtener un menú por ID (Read)
@menu_routes.route('/menus/<int:id>', methods=['GET'])
def get_menu(id):
    menu = menu_repo.find(id)
    if menu:
        return jsonify({"id": menu.id_menu, "tipo": menu.tipo, "fecha_inicio": menu.fecha_inicio, "fecha_fin": menu.fecha_fin})
    return jsonify({"error": "Menu not found"}), 404

# Actualizar un menú existente (Update)
@menu_routes.route('/menus/<int:id>', methods=['PUT'])
def update_menu(id):
    data = request.json
    menu = Menu(tipo=data['tipo'], fecha_inicio=data['fecha_inicio'], fecha_fin=data.get('fecha_fin'))
    updated_menu = menu_repo.update(menu, id)
    if updated_menu:
        return jsonify({"id": updated_menu.id_menu, "tipo": updated_menu.tipo, "fecha_inicio": updated_menu.fecha_inicio, "fecha_fin": updated_menu.fecha_fin})
    return jsonify({"error": "Menu not found"}), 404

# Eliminar un menú (Delete)
@menu_routes.route('/menus/<int:id>', methods=['DELETE'])
def delete_menu(id):
    menu_repo.delete(id)
    return jsonify({"message": "Menu deleted"}), 204
