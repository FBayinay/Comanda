from flask import Blueprint, request, jsonify
from app.repositories import TableRepository
from app.models import Table

table_routes = Blueprint('table_routes', __name__)
table_repo = TableRepository()

# Crear una nueva mesa (Create)
@table_routes.route('/mesas', methods=['POST'])
def create_table():
    data = request.json
    if not all(key in data for key in ('numero_mesa', 'capacidad', 'estado')):
        return jsonify({"error": "Datos incompletos"}), 400

    new_table = Table(
        numero_mesa=data['numero_mesa'],
        capacidad=data['capacidad'],
        estado=data['estado']
    )
    
    saved_table = table_repo.save(new_table)
    return jsonify({
        "id": saved_table.id_mesa,
        "numero_mesa": saved_table.numero_mesa,
        "capacidad": saved_table.capacidad,
        "estado": saved_table.estado
    }), 201

# Obtener todas las mesas (Read)
@table_routes.route('/mesas', methods=['GET'])
def get_tables():
    tables = table_repo.all()
    return jsonify([{
        "id": table.id_mesa,
        "numero_mesa": table.numero_mesa,
        "capacidad": table.capacidad,
        "estado": table.estado
    } for table in tables])

# Obtener una mesa por ID (Read)
@table_routes.route('/mesas/<int:id>', methods=['GET'])
def get_table(id):
    table = table_repo.find(id)
    if table:
        return jsonify({
            "id": table.id_mesa,
            "numero_mesa": table.numero_mesa,
            "capacidad": table.capacidad,
            "estado": table.estado
        })
    return jsonify({"error": "Mesa no encontrada"}), 404

# Actualizar una mesa existente (Update)
@table_routes.route('/mesas/<int:id>', methods=['PUT'])
def update_table(id):
    data = request.json
    if not all(key in data for key in ('numero_mesa', 'capacidad', 'estado')):
        return jsonify({"error": "Datos incompletos"}), 400

    table = Table(
        numero_mesa=data['numero_mesa'],
        capacidad=data['capacidad'],
        estado=data['estado']
    )
    
    updated_table = table_repo.update(table, id)
    if updated_table:
        return jsonify({
            "id": updated_table.id_mesa,
            "numero_mesa": updated_table.numero_mesa,
            "capacidad": updated_table.capacidad,
            "estado": updated_table.estado
        })
    return jsonify({"error": "Mesa no encontrada"}), 404

# Eliminar una mesa (Delete)
@table_routes.route('/mesas/<int:id>', methods=['DELETE'])
def delete_table(id):
    table = table_repo.find(id)
    if table:
        table_repo.delete(id)
        return jsonify({"message": "Mesa eliminada"}), 204
    return jsonify({"error": "Mesa no encontrada"}), 404
