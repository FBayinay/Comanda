from flask import Blueprint, request, jsonify
from app.mapping import UserSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.user_services import UserService

user_routes = Blueprint('user_routes', __name__)
user_schema = UserSchema()
response_schema = ResponseSchema()
user_service = UserService()

# Crear un nuevo usuario (Create)
@user_routes.route('/usuarios', methods=['POST'])
def create_user():
    data = request.json
    response_builder = ResponseBuilder()

    if not all(key in data for key in ('nombre', 'apellido', 'dni', 'email', 'calle', 'numero', 'rol_id', 'id_accion')):
        response_builder.add_message("Datos incompletos").add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

    try:
        new_user = user_service.create_user(
            nombre=data['nombre'],
            apellido=data['apellido'],
            dni=data['dni'],
            email=data['email'],
            calle=data['calle'],
            numero=data['numero'],
            rol_id=data['rol_id'],
            id_accion=data['id_accion']
        )
        response_builder.add_message("Usuario creado").add_status_code(100).add_data(user_schema.dump(new_user))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Obtener todos los usuarios (Read)
@user_routes.route('/usuarios', methods=['GET'])
def index():
    return {"users": user_schema.dump(user_service.get_all_users(), many=True)}, 200

# Obtener un usuario por ID (Read)
@user_routes.route('/usuarios/<int:id>', methods=['GET'])
def get_user(id: int):
    response_builder = ResponseBuilder()
    user = user_service.get_user_by_id(id)
    if user:
        response_builder.add_message("Usuario encontrado").add_status_code(100).add_data(user_schema.dump(user))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Usuario no encontrado").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

# Actualizar un usuario existente (Update)
@user_routes.route('/usuarios/<int:id>', methods=['PUT'])
def update_user(id: int):
    data = request.json
    response_builder = ResponseBuilder()

    if not any(key in data for key in ('nombre', 'apellido', 'dni', 'email', 'calle', 'numero', 'rol_id', 'id_accion')):
        response_builder.add_message("Datos incompletos").add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

    try:
        updated_user = user_service.update_user(
            id,
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            dni=data.get('dni'),
            email=data.get('email'),
            calle=data.get('calle'),
            numero=data.get('numero'),
            rol_id=data.get('rol_id'),
            id_accion=data.get('id_accion')
        )
        if updated_user:
            response_builder.add_message("Usuario actualizado").add_status_code(100).add_data(user_schema.dump(updated_user))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Usuario no encontrado").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Eliminar un usuario (Delete)
@user_routes.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    response_builder = ResponseBuilder()
    user = user_service.get_user_by_id(id)
    if user:
        user_service.delete_user(id)
        response_builder.add_message("Usuario eliminado").add_status_code(100).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 204
    else:
        response_builder.add_message("Usuario no encontrado").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404
