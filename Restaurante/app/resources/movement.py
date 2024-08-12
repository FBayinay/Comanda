from flask import Blueprint, request, jsonify
from app.repositories.movement_repository import WarehouseMovementRepository
from app.models import WarehouseMovement  # Importar desde movement/models

movement_routes = Blueprint('movement_routes', __name__)
movement_repo = WarehouseMovementRepository()

# Crear un nuevo movimiento de almacén (Create)
@movement_routes.route('/warehouse-movements', methods=['POST'])
def create_warehouse_movement():
    data = request.json
    new_movement = WarehouseMovement(
        id_usuario=data['id_usuario'],
        id_producto=data['id_producto'],
        cantidad=data['cantidad'],
        fecha=data.get('fecha')  # Fecha puede ser opcional; si no se proporciona, se asignará la actual
    )
    saved_movement = movement_repo.save(new_movement)
    return jsonify({
        "id": saved_movement.id_movimiento,
        "id_usuario": saved_movement.id_usuario,
        "id_producto": saved_movement.id_producto,
        "cantidad": saved_movement.cantidad,
        "fecha": saved_movement.fecha.isoformat()  # Convertir a string para JSON
    }), 201

# Obtener todos los movimientos de almacén (Read)
@movement_routes.route('/warehouse-movements', methods=['GET'])
def get_warehouse_movements():
    movements = movement_repo.all()
    return jsonify([{
        "id": movement.id_movimiento,
        "id_usuario": movement.id_usuario,
        "id_producto": movement.id_producto,
        "cantidad": movement.cantidad,
        "fecha": movement.fecha.isoformat()  # Convertir a string para JSON
    } for movement in movements])

# Obtener un movimiento de almacén por ID (Read)
@movement_routes.route('/warehouse-movements/<int:id>', methods=['GET'])
def get_warehouse_movement(id):
    movement = movement_repo.find(id)
    if movement:
        return jsonify({
            "id": movement.id_movimiento,
            "id_usuario": movement.id_usuario,
            "id_producto": movement.id_producto,
            "cantidad": movement.cantidad,
            "fecha": movement.fecha.isoformat()  # Convertir a string para JSON
        })
    return jsonify({"error": "WarehouseMovement not found"}), 404

# Actualizar un movimiento de almacén existente (Update)
@movement_routes.route('/warehouse-movements/<int:id>', methods=['PUT'])
def update_warehouse_movement(id):
    data = request.json
    movement = WarehouseMovement(
        id_usuario=data['id_usuario'],
        id_producto=data['id_producto'],
        cantidad=data['cantidad'],
        fecha=data.get('fecha')  # Fecha puede ser opcional; si no se proporciona, se asignará la actual
    )
    updated_movement = movement_repo.update(movement, id)
    if updated_movement:
        return jsonify({
            "id": updated_movement.id_movimiento,
            "id_usuario": updated_movement.id_usuario,
            "id_producto": updated_movement.id_producto,
            "cantidad": updated_movement.cantidad,
            "fecha": updated_movement.fecha.isoformat()  # Convertir a string para JSON
        })
    return jsonify({"error": "WarehouseMovement not found"}), 404

# Eliminar un movimiento de almacén (Delete)
@movement_routes.route('/warehouse-movements/<int:id>', methods=['DELETE'])
def delete_warehouse_movement(id):
    movement_repo.delete(id)
    return jsonify({"message": "WarehouseMovement deleted"}), 204
