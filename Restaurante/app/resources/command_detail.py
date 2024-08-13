from flask import Blueprint, request
from app.mapping import CommandDetailSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.command_detail_services import CommandDetailService

command_detail_routes = Blueprint('command_detail_routes', __name__)
command_detail_schema = CommandDetailSchema()
response_schema = ResponseSchema()
command_detail_service = CommandDetailService()

@command_detail_routes.route('/command-details', methods=['GET'])
def index():
    return {"command_details": command_detail_schema.dump(command_detail_service.all(), many=True)}, 200

@command_detail_routes.route('/command-details/<int:id>', methods=['GET'])
def find(id: int):
    response_builder = ResponseBuilder()
    command_detail = command_detail_service.find(id)
    if command_detail:
        response_builder.add_message("Command detail found").add_status_code(100).add_data(command_detail_schema.dump(command_detail))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Command detail not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

@command_detail_routes.route('/command-details', methods=['POST'])
def post_command_detail():
    command_detail = command_detail_schema.load(request.json)
    saved_command_detail = command_detail_service.save(command_detail)
    return {"command_detail": command_detail_schema.dump(saved_command_detail)}, 201

@command_detail_routes.route('/command-details/<int:id>', methods=['PUT'])
def update_command_detail(id: int):
    command_detail = command_detail_schema.load(request.json)
    response_builder = ResponseBuilder()
    updated_command_detail = command_detail_service.update(command_detail, id)
    if updated_command_detail:
        response_builder.add_message("Command detail updated").add_status_code(100).add_data(command_detail_schema.dump(updated_command_detail))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Command detail not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

@command_detail_routes.route('/command-details/<int:id>', methods=['DELETE'])
def delete_command_detail(id: int):
    command_detail_service.delete(id)
    response_builder = ResponseBuilder()
    response_builder.add_message("Command detail deleted").add_status_code(100).add_data({'id': id})
    return response_schema.dump(response_builder.build()), 200
