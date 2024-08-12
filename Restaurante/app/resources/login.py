from flask import Blueprint, request, jsonify
from app.repositories import LoginRepository
from app.models import Login
from app.models  import User

login_routes = Blueprint('login_routes', __name__)
login_repo = LoginRepository()

# Crear un nuevo login (Create)
@login_routes.route('/logins', methods=['POST'])
def create_login():
    data = request.json
    # Verificar que los datos de entrada sean válidos
    if not all(key in data for key in ('id_usuario', 'username', 'password_hash')):
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        new_login = login_repo.create_login(data['id_usuario'], data['username'], data['password_hash'])
        return jsonify({
            "id": new_login.id_login,
            "id_usuario": new_login.id_usuario,
            "username": new_login.username,
            "password_hash": new_login.password_hash
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener un login por ID (Read)
@login_routes.route('/logins/<int:id>', methods=['GET'])
def get_login(id):
    login = login_repo.get_login_by_id(id)
    if login:
        return jsonify({
            "id": login.id_login,
            "id_usuario": login.id_usuario,
            "username": login.username,
            "password_hash": login.password_hash
        })
    return jsonify({"error": "Login no encontrado"}), 404

# Obtener un login por nombre de usuario (Read)
@login_routes.route('/logins/username/<string:username>', methods=['GET'])
def get_login_by_username(username):
    login = login_repo.get_login_by_username(username)
    if login:
        return jsonify({
            "id": login.id_login,
            "id_usuario": login.id_usuario,
            "username": login.username,
            "password_hash": login.password_hash
        })
    return jsonify({"error": "Login no encontrado"}), 404

# Actualizar un login existente (Update)
@login_routes.route('/logins/<int:id>', methods=['PUT'])
def update_login(id):
    data = request.json
    try:
        updated_login = login_repo.update_login(
            id,
            id_usuario=data.get('id_usuario'),
            username=data.get('username'),
            password_hash=data.get('password_hash')
        )
        if updated_login:
            return jsonify({
                "id": updated_login.id_login,
                "id_usuario": updated_login.id_usuario,
                "username": updated_login.username,
                "password_hash": updated_login.password_hash
            })
        return jsonify({"error": "Login no encontrado"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Eliminar un login (Delete)
@login_routes.route('/logins/<int:id>', methods=['DELETE'])
def delete_login(id):
    login = login_repo.delete_login(id)
    if login:
        return jsonify({"message": "Login eliminado"}), 204
    return jsonify({"error": "Login no encontrado"}), 404
