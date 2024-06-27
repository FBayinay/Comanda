from flask import Blueprint, request, jsonify
from .models import db, User, Role

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return "Bienvenido a la Comanda"

@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.first_name for user in users])

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        dni=data['dni'],
        email=data['email'],
        street=data['street'],
        number=data['number'],
        role_id=data['role_id'],
        action_id=data['action_id'],
        restaurant_id=data['restaurant_id']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuario creado con éxito'})
