from flask import Blueprint, request
from app.mapping import CommandSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.command_services import CommandService

command_routes = Blueprint('command_routes', __name__)
command_schema = CommandSchema()
response_schema = ResponseSchema()
command_service = CommandService()

@command_routes.route('/commands', methods=['GET'])
def index():
    return {"commands": command_schema.dump(command_service.all(), many=True)}, 200

@command_routes.route('/commands/<int:id>', methods=['GET'])
def find(id: int):
    response_builder = ResponseBuilder()
    command = command_service.find(id)
    if command:
        response_builder.add_message("Command found").add_status_code(100).add_data(command_schema.dump(command))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Command not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

@command_routes.route('/commands', methods=['POST'])
def post_command():
    command = command_schema.load(request.json)
    saved_command = command_service.save(command)
    return {"command": command_schema.dump(saved_command)}, 201

@command_routes.route('/commands/<int:id>', methods=['PUT'])
def update_command(id: int):
    command = command_schema.load(request.json)
    response_builder = ResponseBuilder()
    updated_command = command_service.update(command, id)
    if updated_command:
        response_builder.add_message("Command updated").add_status_code(100).add_data(command_schema.dump(updated_command))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Command not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

@command_routes.route('/commands/<int:id>', methods=['DELETE'])
def delete_command(id: int):
    command_service.delete(id)
    response_builder = ResponseBuilder()
    response_builder.add_message("Command deleted").add_status_code(100).add_data({'id': id})
    return response_schema.dump(response_builder.build()), 200
