from flask import Blueprint, request, jsonify
from app.mapping import RoleSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.role_services import RoleService
from app.models import Role

role_routes = Blueprint('role_routes', __name__)
role_schema = RoleSchema()
response_schema = ResponseSchema()
role_service = RoleService()

@role_routes.route('/roles', methods=['GET'])
def index():
    return {"roles": role_schema.dump(role_service.all(), many=True)}, 200

# Crear un nuevo rol (Create)
@role_routes.route('/roles', methods=['POST'])
def create_role():
    data = request.json
    response_builder = ResponseBuilder()

    try:
        new_role = role_service.save(Role(nombre=data['nombre']))
        response_builder.add_message("Role created").add_status_code(100).add_data(role_schema.dump(new_role))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400


# Obtener un rol por ID (Read)
@role_routes.route('/roles/<int:id>', methods=['GET'])
def get_role(id: int):
    response_builder = ResponseBuilder()
    role = role_service.find(id)
    if role:
        response_builder.add_message("Role found").add_status_code(100).add_data(role_schema.dump(role))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Role not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

# Actualizar un rol existente (Update)
@role_routes.route('/roles/<int:id>', methods=['PUT'])
def update_role(id: int):
    data = request.json
    response_builder = ResponseBuilder()

    try:
        updated_role = role_service.update(Role(nombre=data['nombre']), id)
        if updated_role:
            response_builder.add_message("Role updated").add_status_code(100).add_data(role_schema.dump(updated_role))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Role not found").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Eliminar un rol (Delete)
@role_routes.route('/roles/<int:id>', methods=['DELETE'])
def delete_role(id: int):
    response_builder = ResponseBuilder()
    role = role_service.find(id)
    if role:
        role_service.delete(id)
        response_builder.add_message("Role deleted").add_status_code(100).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 204
    else:
        response_builder.add_message("Role not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404
