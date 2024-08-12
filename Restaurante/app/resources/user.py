from flask import Blueprint, request, jsonify
from app.repositories import UserRepository
from app.models import User
user_routes = Blueprint('user_routes', __name__)
user_repo = UserRepository()

# Crear un nuevo usuario (Create)
@user_routes.route('/usuarios', methods=['POST'])
def create_user():
    data = request.json
    # Verificar que los datos de entrada sean válidos
    if not all(key in data for key in ('nombre', 'apellido', 'dni', 'email', 'calle', 'numero', 'rol_id', 'id_accion')):
        return jsonify({"error": "Datos incompletos"}), 400

    # Verificar que el rol y la acción existen
    if not user_repo._role_exists(data['rol_id']) or not user_repo._action_exists(data['id_accion']):
        return jsonify({"error": "Rol o acción no válida"}), 400
   
    # Verificar que el email y el dni sean únicos
    if user_repo.email_exists(data['email']) or user_repo.dni_exists(data['dni']): 
        return jsonify({"error": "El Email o DNI ya está en uso"}), 400
    

    new_user = User(
        nombre=data['nombre'],
        apellido=data['apellido'],
        dni=data['dni'],
        email=data['email'],
        calle=data['calle'],
        numero=data['numero'],
        rol_id=data['rol_id'],
        id_accion=data['id_accion']
    )
    
    saved_user = user_repo.save(new_user)
    if saved_user:
        return jsonify({
            "id": saved_user.id_usuario,
            "nombre": saved_user.nombre,
            "apellido": saved_user.apellido,
            "dni": saved_user.dni,
            "email": saved_user.email,
            "calle": saved_user.calle,
            "numero": saved_user.numero,
            "rol_id": saved_user.rol_id,
            "id_accion": saved_user.id_accion
        }), 201
    return jsonify({"error": "No se pudo guardar el usuario"}), 500

# Obtener todos los usuarios (Read)
@user_routes.route('/usuarios', methods=['GET'])
def get_users():
    users = user_repo.all()
    return jsonify([{
        "id": user.id_usuario,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "dni": user.dni,
        "email": user.email,
        "calle": user.calle,
        "numero": user.numero,
        "rol_id": user.rol_id,
        "id_accion": user.id_accion
    } for user in users])

# Obtener un usuario por ID (Read)
@user_routes.route('/usuarios/<int:id>', methods=['GET'])
def get_user(id):
    user = user_repo.find(id)
    if user:
        return jsonify({
            "id": user.id_usuario,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "dni": user.dni,
            "email": user.email,
            "calle": user.calle,
            "numero": user.numero,
            "rol_id": user.rol_id,
            "id_accion": user.id_accion
        })
    return jsonify({"error": "Usuario no encontrado"}), 404

# Actualizar un usuario existente (Update)
@user_routes.route('/usuarios/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    if not all(key in data for key in ('nombre', 'apellido', 'dni', 'email', 'calle', 'numero', 'rol_id', 'id_accion')):
        return jsonify({"error": "Datos incompletos"}), 400

    # Verificar que el rol y la acción existen
    if not user_repo._role_exists(data['rol_id']) or not user_repo._action_exists(data['id_accion']):
        return jsonify({"error": "Rol o acción no válida"}), 400

    user = User(
        nombre=data['nombre'],
        apellido=data['apellido'],
        dni=data['dni'],
        email=data['email'],
        calle=data['calle'],
        numero=data['numero'],
        rol_id=data['rol_id'],
        id_accion=data['id_accion']
    )
    
    updated_user = user_repo.update(user, id)
    if updated_user:
        return jsonify({
            "id": updated_user.id_usuario,
            "nombre": updated_user.nombre,
            "apellido": updated_user.apellido,
            "dni": updated_user.dni,
            "email": updated_user.email,
            "calle": updated_user.calle,
            "numero": updated_user.numero,
            "rol_id": updated_user.rol_id,
            "id_accion": updated_user.id_accion
        })
    return jsonify({"error": "Usuario no encontrado"}), 404

# Eliminar un usuario (Delete)
@user_routes.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = user_repo.find(id)
    if user:
        user_repo.delete(id)
        return jsonify({"message": "Usuario eliminado"}), 204
    return jsonify({"error": "Usuario no encontrado"}), 404
