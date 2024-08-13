from flask import Blueprint, request, jsonify
from app.mapping import WarehouseMovementSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.warehouse_movement_services import MovementService

movement_routes = Blueprint('movement_routes', __name__)
movement_schema = WarehouseMovementSchema()
response_schema = ResponseSchema()
movement_service = MovementService()

# Crear un nuevo movimiento de almacén (Create)
@movement_routes.route('/warehouse-movements', methods=['POST'])
def create_warehouse_movement():
    data = request.json
    response_builder = ResponseBuilder()

    try:
        new_movement = movement_service.create_movement(
            id_usuario=data['id_usuario'],
            id_producto=data['id_producto'],
            cantidad=data['cantidad'],
            fecha=data.get('fecha')  # Fecha puede ser opcional
        )
        response_builder.add_message("Movimiento de almacén creado").add_status_code(100).add_data(movement_schema.dump(new_movement))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Obtener todos los movimientos de almacén (Read)
@movement_routes.route('/warehouse-movements', methods=['GET'])
def get_warehouse_movements():
    response_builder = ResponseBuilder()
    movements = movement_service.get_all_movements()
    response_builder.add_message("Movimientos de almacén recuperados").add_status_code(100).add_data([movement_schema.dump(movement) for movement in movements])
    return response_schema.dump(response_builder.build()), 200

# Obtener un movimiento de almacén por ID (Read)
@movement_routes.route('/warehouse-movements/<int:id>', methods=['GET'])
def get_warehouse_movement(id: int):
    response_builder = ResponseBuilder()
    movement = movement_service.get_movement_by_id(id)
    if movement:
        response_builder.add_message("Movimiento de almacén encontrado").add_status_code(100).add_data(movement_schema.dump(movement))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Movimiento de almacén no encontrado").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

# Actualizar un movimiento de almacén existente (Update)
@movement_routes.route('/warehouse-movements/<int:id>', methods=['PUT'])
def update_warehouse_movement(id: int):
    data = request.json
    response_builder = ResponseBuilder()

    try:
        updated_movement = movement_service.update_movement(
            id,
            id_usuario=data.get('id_usuario'),
            id_producto=data.get('id_producto'),
            cantidad=data.get('cantidad'),
            fecha=data.get('fecha')
        )
        if updated_movement:
            response_builder.add_message("Movimiento de almacén actualizado").add_status_code(100).add_data(movement_schema.dump(updated_movement))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Movimiento de almacén no encontrado").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Eliminar un movimiento de almacén (Delete)
@movement_routes.route('/warehouse-movements/<int:id>', methods=['DELETE'])
def delete_warehouse_movement(id: int):
    response_builder = ResponseBuilder()
    movement = movement_service.get_movement_by_id(id)
    if movement:
        movement_service.delete_movement(id)
        response_builder.add_message("Movimiento de almacén eliminado").add_status_code(100).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 204
    else:
        response_builder.add_message("Movimiento de almacén no encontrado").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404
