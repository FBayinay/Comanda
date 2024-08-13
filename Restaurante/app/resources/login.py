from flask import Blueprint, request, jsonify
from app.mapping import LoginSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.login_services import LoginService

login_routes = Blueprint('login_routes', __name__)
login_schema = LoginSchema()
response_schema = ResponseSchema()
login_service = LoginService()

@login_routes.route('/logins', methods=['POST'])
def create_login():
    data = request.json
    if not all(key in data for key in ('id_usuario', 'username', 'password_hash')):
        return jsonify({"error": "Datos incompletos"}), 400

    response_builder = ResponseBuilder()
    try:
        new_login = login_service.create_login(data['id_usuario'], data['username'], data['password_hash'])
        response_builder.add_message("Login created").add_status_code(100).add_data(login_schema.dump(new_login))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

@login_routes.route('/logins/<int:id>', methods=['GET'])
def get_login(id: int):
    response_builder = ResponseBuilder()
    login = login_service.get_login_by_id(id)
    if login:
        response_builder.add_message("Login found").add_status_code(100).add_data(login_schema.dump(login))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Login not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

@login_routes.route('/logins/username/<string:username>', methods=['GET'])
def get_login_by_username(username: str):
    response_builder = ResponseBuilder()
    login = login_service.get_login_by_username(username)
    if login:
        response_builder.add_message("Login found").add_status_code(100).add_data(login_schema.dump(login))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Login not found").add_status_code(300).add_data({'username': username})
        return response_schema.dump(response_builder.build()), 404

@login_routes.route('/logins/<int:id>', methods=['PUT'])
def update_login(id: int):
    data = request.json
    response_builder = ResponseBuilder()
    try:
        updated_login = login_service.update_login(
            id,
            id_usuario=data.get('id_usuario'),
            username=data.get('username'),
            password_hash=data.get('password_hash')
        )
        if updated_login:
            response_builder.add_message("Login updated").add_status_code(100).add_data(login_schema.dump(updated_login))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Login not found").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

@login_routes.route('/logins/<int:id>', methods=['DELETE'])
def delete_login(id: int):
    response_builder = ResponseBuilder()
    deleted_login = login_service.delete_login(id)
    if deleted_login:
        response_builder.add_message("Login deleted").add_status_code(100).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 204
    else:
        response_builder.add_message("Login not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404
