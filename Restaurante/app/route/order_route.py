from flask import Blueprint, request, jsonify
from app.repositories.order_repository import OrderRepository
from app.models import Order  # Importar desde app/models

order_routes = Blueprint('order_routes', __name__)
order_repo = OrderRepository()

# Crear un nuevo pedido (Create)
@order_routes.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(
        id_usuario=data['id_usuario'],
        id_producto=data['id_producto'],
        id_proveedor=data['id_proveedor'],
        cantidad=data['cantidad'],
        precio_unitario=data['precio_unitario'],
        precio_total=data['precio_total'],
        fecha=data.get('fecha')  # Fecha puede ser opcional; si no se proporciona, se asignará la actual
    )
    saved_order = order_repo.save(new_order)
    return jsonify({
        "id": saved_order.id_pedido,
        "id_usuario": saved_order.id_usuario,
        "id_producto": saved_order.id_producto,
        "id_proveedor": saved_order.id_proveedor,
        "cantidad": saved_order.cantidad,
        "precio_unitario": saved_order.precio_unitario,
        "precio_total": saved_order.precio_total,
        "fecha": saved_order.fecha.isoformat()  # Convertir a string para JSON
    }), 201

# Obtener todos los pedidos (Read)
@order_routes.route('/orders', methods=['GET'])
def get_orders():
    orders = order_repo.all()
    return jsonify([{
        "id": order.id_pedido,
        "id_usuario": order.id_usuario,
        "id_producto": order.id_producto,
        "id_proveedor": order.id_proveedor,
        "cantidad": order.cantidad,
        "precio_unitario": order.precio_unitario,
        "precio_total": order.precio_total,
        "fecha": order.fecha.isoformat()  # Convertir a string para JSON
    } for order in orders])

# Obtener un pedido por ID (Read)
@order_routes.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = order_repo.find(id)
    if order:
        return jsonify({
            "id": order.id_pedido,
            "id_usuario": order.id_usuario,
            "id_producto": order.id_producto,
            "id_proveedor": order.id_proveedor,
            "cantidad": order.cantidad,
            "precio_unitario": order.precio_unitario,
            "precio_total": order.precio_total,
            "fecha": order.fecha.isoformat()  # Convertir a string para JSON
        })
    return jsonify({"error": "Order not found"}), 404

# Actualizar un pedido existente (Update)
@order_routes.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    data = request.json
    order = Order(
        id_usuario=data['id_usuario'],
        id_producto=data['id_producto'],
        id_proveedor=data['id_proveedor'],
        cantidad=data['cantidad'],
        precio_unitario=data['precio_unitario'],
        precio_total=data['precio_total'],
        fecha=data.get('fecha')  # Fecha puede ser opcional; si no se proporciona, se asignará la actual
    )
    updated_order = order_repo.update(order, id)
    if updated_order:
        return jsonify({
            "id": updated_order.id_pedido,
            "id_usuario": updated_order.id_usuario,
            "id_producto": updated_order.id_producto,
            "id_proveedor": updated_order.id_proveedor,
            "cantidad": updated_order.cantidad,
            "precio_unitario": updated_order.precio_unitario,
            "precio_total": updated_order.precio_total,
            "fecha": updated_order.fecha.isoformat()  # Convertir a string para JSON
        })
    return jsonify({"error": "Order not found"}), 404

# Eliminar un pedido (Delete)
@order_routes.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order_repo.delete(id)
    return jsonify({"message": "Order deleted"}), 204
