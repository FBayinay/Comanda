from flask import Blueprint, request, jsonify
from app.repositories import RoleRepository
from app.models import Role

role_routes = Blueprint('role_routes', __name__)
role_repo = RoleRepository()

# Crear un nuevo rol (Create)
@role_routes.route('/roles', methods=['POST'])
def create_role():
    data = request.json
    new_role = Role(nombre=data['nombre'])
    saved_role = role_repo.save(new_role)
    return jsonify({"id": saved_role.id_rol, "nombre": saved_role.nombre}), 201

# Obtener todos los roles (Read)
@role_routes.route('/roles', methods=['GET'])
def get_roles():
    roles = role_repo.all()
    return jsonify([{"id": role.id_rol, "nombre": role.nombre} for role in roles])

# Obtener un rol por ID (Read)
@role_routes.route('/roles/<int:id>', methods=['GET'])
def get_role(id):
    role = role_repo.find(id)
    if role:
        return jsonify({"id": role.id_rol, "nombre": role.nombre})
    return jsonify({"error": "Role not found"}), 404

# Actualizar un rol existente (Update)
@role_routes.route('/roles/<int:id>', methods=['PUT'])
def update_role(id):
    data = request.json
    role = Role(nombre=data['nombre'])
    updated_role = role_repo.update(role, id)
    if updated_role:
        return jsonify({"id": updated_role.id_rol, "nombre": updated_role.nombre})
    return jsonify({"error": "Role not found"}), 404

# Eliminar un rol (Delete)
@role_routes.route('/roles/<int:id>', methods=['DELETE'])
def delete_role(id):
    role_repo.delete(id)
    return jsonify({"message": "Role deleted"}), 204
