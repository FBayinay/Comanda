from flask import Blueprint, request, jsonify
from app.repositories import ActionRepository
from app.models import Action

action_routes = Blueprint('action_routes', __name__)
action_repo = ActionRepository()

# Crear un nuevo rol (Create)
@action_routes.route('/actions', methods=['POST'])
def create_action():
    data = request.json
    new_action = Action(nombre=data['nombre'])
    saved_action = action_repo.save(new_action)
    return jsonify({"id": saved_action.id_accion, "nombre": saved_action.nombre}), 201

# Obtener todos los actions (Read)
@action_routes.route('/actions', methods=['GET'])
def get_actions():
    actions = action_repo.all()
    return jsonify([{"id": action.id_accion, "nombre": action.nombre} for action in actions])

# Obtener un rol por ID (Read)
@action_routes.route('/actions/<int:id>', methods=['GET'])
def get_action(id):
    action = action_repo.find(id)
    if action:
        return jsonify({"id": action.id_accion, "nombre": action.nombre})
    return jsonify({"error": "Action not found"}), 404

# Actualizar un rol existente (Update)
@action_routes.route('/actions/<int:id>', methods=['PUT'])
def update_action(id):
    data = request.json
    action = Action(nombre=data['nombre'])
    updated_action = action_repo.update(action, id)
    if updated_action:
        return jsonify({"id": updated_action.id_accion, "nombre": updated_action.nombre})
    return jsonify({"error": "Action not found"}), 404

# Eliminar un rol (Delete)
@action_routes.route('/actions/<int:id>', methods=['DELETE'])
def delete_action(id):
    action_repo.delete(id)
    return jsonify({"message": "Action deleted"}), 204
