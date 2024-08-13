from flask import Blueprint, request
from app.mapping import ActionSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.action_services import ActionService

action_routes = Blueprint('action_routes', __name__)
action_schema = ActionSchema()
response_schema = ResponseSchema()
action_service = ActionService()

@action_routes.route('/actions', methods=['GET'])
def index():
    return {"actions": action_schema.dump(action_service.all(), many=True)}, 200

@action_routes.route('/actions/<int:id>', methods=['GET'])
def find(id: int):
    response_builder = ResponseBuilder()
    action = action_service.find(id)
    if action:
        response_builder.add_message("Action found").add_status_code(100).add_data(action_schema.dump(action))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Action not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

@action_routes.route('/actions', methods=['POST'])
def post_action():
    action = action_schema.load(request.json)
    saved_action = action_service.save(action)
    return {"action": action_schema.dump(saved_action)}, 201

@action_routes.route('/actions/<int:id>', methods=['PUT'])
def update_action(id: int):
    action = action_schema.load(request.json)
    response_builder = ResponseBuilder()
    updated_action = action_service.update(action, id)
    if updated_action:
        response_builder.add_message("Action updated").add_status_code(100).add_data(action_schema.dump(updated_action))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Action not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

@action_routes.route('/actions/<int:id>', methods=['DELETE'])
def delete_action(id: int):
    action_service.delete(id)
    response_builder = ResponseBuilder()
    response_builder.add_message("Action deleted").add_status_code(100).add_data({'id': id})
    return response_schema.dump(response_builder.build()), 200
