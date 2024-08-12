from flask import Blueprint, request, jsonify
from app.repositories import MenuItemRepository
from app.models import MenuItem

menu_item_routes = Blueprint('menu_item_routes', __name__)
menu_item_repo = MenuItemRepository()

# Crear un nuevo ítem de menú (Create)
@menu_item_routes.route('/menu-items', methods=['POST'])
def create_menu_item():
    data = request.json
    new_item = MenuItem(
        id_menu=data['id_menu'],
        id_categoria=data['id_categoria'],
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        precio=data['precio']
    )
    saved_item = menu_item_repo.save(new_item)
    return jsonify({
        "id": saved_item.id_items,
        "id_menu": saved_item.id_menu,
        "id_categoria": saved_item.id_categoria,
        "nombre": saved_item.nombre,
        "descripcion": saved_item.descripcion,
        "precio": str(saved_item.precio)  # Convertir a string para JSON
    }), 201

# Obtener todos los ítems de menú (Read)
@menu_item_routes.route('/menu-items', methods=['GET'])
def get_menu_items():
    items = menu_item_repo.all()
    return jsonify([{
        "id": item.id_items,
        "id_menu": item.id_menu,
        "id_categoria": item.id_categoria,
        "nombre": item.nombre,
        "descripcion": item.descripcion,
        "precio": str(item.precio)  # Convertir a string para JSON
    } for item in items])

# Obtener un ítem de menú por ID (Read)
@menu_item_routes.route('/menu-items/<int:id>', methods=['GET'])
def get_menu_item(id):
    item = menu_item_repo.find(id)
    if item:
        return jsonify({
            "id": item.id_items,
            "id_menu": item.id_menu,
            "id_categoria": item.id_categoria,
            "nombre": item.nombre,
            "descripcion": item.descripcion,
            "precio": str(item.precio)  # Convertir a string para JSON
        })
    return jsonify({"error": "MenuItem not found"}), 404

# Actualizar un ítem de menú existente (Update)
@menu_item_routes.route('/menu-items/<int:id>', methods=['PUT'])
def update_menu_item(id):
    data = request.json
    item = MenuItem(
        id_menu=data['id_menu'],
        id_categoria=data['id_categoria'],
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        precio=data['precio']
    )
    updated_item = menu_item_repo.update(item, id)
    if updated_item:
        return jsonify({
            "id": updated_item.id_items,
            "id_menu": updated_item.id_menu,
            "id_categoria": updated_item.id_categoria,
            "nombre": updated_item.nombre,
            "descripcion": updated_item.descripcion,
            "precio": str(updated_item.precio)  # Convertir a string para JSON
        })
    return jsonify({"error": "MenuItem not found"}), 404

# Eliminar un ítem de menú (Delete)
@menu_item_routes.route('/menu-items/<int:id>', methods=['DELETE'])
def delete_menu_item(id):
    menu_item_repo.delete(id)
    return jsonify({"message": "MenuItem deleted"}), 204
