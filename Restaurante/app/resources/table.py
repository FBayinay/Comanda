from flask import Blueprint, request, jsonify
from app.mapping import TableSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.table_services import TableService

table_routes = Blueprint('table_routes', __name__)
table_schema = TableSchema()
response_schema = ResponseSchema()
table_service = TableService()

# Crear una nueva mesa (Create)
@table_routes.route('/mesas', methods=['POST'])
def create_table():
    data = request.json
    response_builder = ResponseBuilder()

    if not all(key in data for key in ('numero_mesa', 'capacidad', 'estado')):
        response_builder.add_message("Datos incompletos").add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

    try:
        new_table = table_service.create_table(data['numero_mesa'], data['capacidad'], data['estado'])
        response_builder.add_message("Mesa creada").add_status_code(100).add_data(table_schema.dump(new_table))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Obtener todas las mesas (Read)
@table_routes.route('/mesas', methods=['GET'])
def get_tables():
    response_builder = ResponseBuilder()
    tables = table_service.get_all_tables()
    response_builder.add_message("Mesas recuperadas").add_status_code(100).add_data([table_schema.dump(table) for table in tables])
    return response_schema.dump(response_builder.build()), 200

# Obtener una mesa por ID (Read)
@table_routes.route('/mesas/<int:id>', methods=['GET'])
def get_table(id: int):
    response_builder = ResponseBuilder()
    table = table_service.get_table_by_id(id)
    if table:
        response_builder.add_message("Mesa encontrada").add_status_code(100).add_data(table_schema.dump(table))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Mesa no encontrada").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

# Actualizar una mesa existente (Update)
@table_routes.route('/mesas/<int:id>', methods=['PUT'])
def update_table(id: int):
    data = request.json
    response_builder = ResponseBuilder()

    if not any(key in data for key in ('numero_mesa', 'capacidad', 'estado')):
        response_builder.add_message("Datos incompletos").add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

    try:
        updated_table = table_service.update_table(id, data.get('numero_mesa'), data.get('capacidad'), data.get('estado'))
        if updated_table:
            response_builder.add_message("Mesa actualizada").add_status_code(100).add_data(table_schema.dump(updated_table))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Mesa no encontrada").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Eliminar una mesa (Delete)
@table_routes.route('/mesas/<int:id>', methods=['DELETE'])
def delete_table(id: int):
    response_builder = ResponseBuilder()
    table = table_service.get_table_by_id(id)
    if table:
        table_service.delete_table(id)
        response_builder.add_message("Mesa eliminada").add_status_code(100).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 204
    else:
        response_builder.add_message("Mesa no encontrada").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404
