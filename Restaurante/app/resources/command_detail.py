from flask import Blueprint, request, jsonify
from app.repositories import CommandDetailRepository
from app.models import CommandDetail  

command_detail_routes = Blueprint('command_detail_routes', __name__)
command_detail_repo = CommandDetailRepository()

# Crear un nuevo detalle de comando (Create)
@command_detail_routes.route('/command-details', methods=['POST'])
def create_command_detail():
    data = request.json
    new_command_detail = CommandDetail(
        id_comanda=data['id_comanda'],
        id_item_menu=data['id_item_menu'],
        id_menu=data['id_menu'],
        cantidad=data['cantidad'],
        precio_total=data['precio_total']
    )
    saved_command_detail = command_detail_repo.save(new_command_detail)
    return jsonify({
        "id": saved_command_detail.id_detalles,
        "id_comanda": saved_command_detail.id_comanda,
        "id_item_menu": saved_command_detail.id_item_menu,
        "id_menu": saved_command_detail.id_menu,
        "cantidad": saved_command_detail.cantidad,
        "precio_total": str(saved_command_detail.precio_total)  # Convertir a string para JSON
    }), 201

# Obtener todos los detalles de comando (Read)
@command_detail_routes.route('/command-details', methods=['GET'])
def get_command_details():
    command_details = command_detail_repo.all()
    return jsonify([{
        "id": command_detail.id_detalles,
        "id_comanda": command_detail.id_comanda,
        "id_item_menu": command_detail.id_item_menu,
        "id_menu": command_detail.id_menu,
        "cantidad": command_detail.cantidad,
        "precio_total": str(command_detail.precio_total)  # Convertir a string para JSON
    } for command_detail in command_details])

# Obtener un detalle de comando por ID (Read)
@command_detail_routes.route('/command-details/<int:id>', methods=['GET'])
def get_command_detail(id):
    command_detail = command_detail_repo.find(id)
    if command_detail:
        return jsonify({
            "id": command_detail.id_detalles,
            "id_comanda": command_detail.id_comanda,
            "id_item_menu": command_detail.id_item_menu,
            "id_menu": command_detail.id_menu,
            "cantidad": command_detail.cantidad,
            "precio_total": str(command_detail.precio_total)  # Convertir a string para JSON
        })
    return jsonify({"error": "Command detail not found"}), 404

# Actualizar un detalle de comando existente (Update)
@command_detail_routes.route('/command-details/<int:id>', methods=['PUT'])
def update_command_detail(id):
    data = request.json
    command_detail = CommandDetail(
        id_comanda=data['id_comanda'],
        id_item_menu=data['id_item_menu'],
        id_menu=data['id_menu'],
        cantidad=data['cantidad'],
        precio_total=data['precio_total']
    )
    updated_command_detail = command_detail_repo.update(command_detail, id)
    if updated_command_detail:
        return jsonify({
            "id": updated_command_detail.id_detalles,
            "id_comanda": updated_command_detail.id_comanda,
            "id_item_menu": updated_command_detail.id_item_menu,
            "id_menu": updated_command_detail.id_menu,
            "cantidad": updated_command_detail.cantidad,
            "precio_total": str(updated_command_detail.precio_total)  # Convertir a string para JSON
        })
    return jsonify({"error": "Command detail not found"}), 404

# Eliminar un detalle de comando (Delete)
@command_detail_routes.route('/command-details/<int:id>', methods=['DELETE'])
def delete_command_detail(id):
    command_detail_repo.delete(id)
    return jsonify({"message": "Command detail deleted"}), 204
