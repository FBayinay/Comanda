from flask import Blueprint, request, jsonify
from app.repositories import CommandRepository
from app.models import Command  # Importar desde app/models

command_routes = Blueprint('command_routes', __name__)
command_repo = CommandRepository()

# Crear un nuevo comando (Create)
@command_routes.route('/commands', methods=['POST'])
def create_command():
    data = request.json
    new_command = Command(
        id_mesa=data['id_mesa'],
        id_usuario=data['id_usuario'],
        fecha_inicio=data.get('fecha_inicio'),
        fecha_fin=data.get('fecha_fin'),
        estado=data.get('estado', 'En Proceso')  # Estado por defecto si no se proporciona
    )
    saved_command = command_repo.save(new_command)
    return jsonify({
        "id": saved_command.id_comanda,
        "id_mesa": saved_command.id_mesa,
        "id_usuario": saved_command.id_usuario,
        "fecha_inicio": saved_command.fecha_inicio.isoformat(),  # Convertir a string para JSON
        "fecha_fin": saved_command.fecha_fin.isoformat() if saved_command.fecha_fin else None,
        "estado": saved_command.estado
    }), 201

# Obtener todos los comandos (Read)
@command_routes.route('/commands', methods=['GET'])
def get_commands():
    commands = command_repo.all()
    return jsonify([{
        "id": command.id_comanda,
        "id_mesa": command.id_mesa,
        "id_usuario": command.id_usuario,
        "fecha_inicio": command.fecha_inicio.isoformat(),  # Convertir a string para JSON
        "fecha_fin": command.fecha_fin.isoformat() if command.fecha_fin else None,
        "estado": command.estado
    } for command in commands])

# Obtener un comando por ID (Read)
@command_routes.route('/commands/<int:id>', methods=['GET'])
def get_command(id):
    command = command_repo.find(id)
    if command:
        return jsonify({
            "id": command.id_comanda,
            "id_mesa": command.id_mesa,
            "id_usuario": command.id_usuario,
            "fecha_inicio": command.fecha_inicio.isoformat(),  # Convertir a string para JSON
            "fecha_fin": command.fecha_fin.isoformat() if command.fecha_fin else None,
            "estado": command.estado
        })
    return jsonify({"error": "Command not found"}), 404

# Actualizar un comando existente (Update)
@command_routes.route('/commands/<int:id>', methods=['PUT'])
def update_command(id):
    data = request.json
    command = Command(
        id_mesa=data['id_mesa'],
        id_usuario=data['id_usuario'],
        fecha_inicio=data.get('fecha_inicio'),
        fecha_fin=data.get('fecha_fin'),
        estado=data.get('estado', 'En Proceso')  # Estado por defecto si no se proporciona
    )
    updated_command = command_repo.update(command, id)
    if updated_command:
        return jsonify({
            "id": updated_command.id_comanda,
            "id_mesa": updated_command.id_mesa,
            "id_usuario": updated_command.id_usuario,
            "fecha_inicio": updated_command.fecha_inicio.isoformat(),  # Convertir a string para JSON
            "fecha_fin": updated_command.fecha_fin.isoformat() if updated_command.fecha_fin else None,
            "estado": updated_command.estado
        })
    return jsonify({"error": "Command not found"}), 404

# Eliminar un comando (Delete)
@command_routes.route('/commands/<int:id>', methods=['DELETE'])
def delete_command(id):
    command_repo.delete(id)
    return jsonify({"message": "Command deleted"}), 204
