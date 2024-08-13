from flask import Blueprint, request, jsonify
from app.mapping import OrderSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.order_services import OrderService

order_routes = Blueprint('order_routes', __name__)
order_schema = OrderSchema()
response_schema = ResponseSchema()
order_service = OrderService()

@order_routes.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    required_fields = ['id_usuario', 'id_producto', 'id_proveedor', 'cantidad', 'precio_unitario', 'precio_total']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Datos incompletos"}), 400

    response_builder = ResponseBuilder()
    try:
        new_order = order_service.create_order(
            id_usuario=data['id_usuario'],
            id_producto=data['id_producto'],
            id_proveedor=data['id_proveedor'],
            cantidad=data['cantidad'],
            precio_unitario=data['precio_unitario'],
            precio_total=data['precio_total']
        )
        response_builder.add_message("Order created").add_status_code(100).add_data(order_schema.dump(new_order))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

@order_routes.route('/orders', methods=['GET'])
def get_orders():
    response_builder = ResponseBuilder()
    orders = order_service.get_all_orders()
    response_builder.add_message("Orders retrieved").add_status_code(100).add_data([order_schema.dump(order) for order in orders])
    return response_schema.dump(response_builder.build()), 200

@order_routes.route('/orders/<int:id>', methods=['GET'])
def get_order(id: int):
    response_builder = ResponseBuilder()
    order = order_service.get_order_by_id(id)
    if order:
        response_builder.add_message("Order found").add_status_code(100).add_data(order_schema.dump(order))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Order not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

@order_routes.route('/orders/<int:id>', methods=['PUT'])
def update_order(id: int):
    data = request.json
    response_builder = ResponseBuilder()
    try:
        updated_order = order_service.update_order(
            id,
            id_usuario=data.get('id_usuario'),
            id_producto=data.get('id_producto'),
            id_proveedor=data.get('id_proveedor'),
            cantidad=data.get('cantidad'),
            precio_unitario=data.get('precio_unitario'),
            precio_total=data.get('precio_total'),
            fecha=data.get('fecha')  # Asegúrate de manejar la conversión a datetime si es necesario
        )
        if updated_order:
            response_builder.add_message("Order updated").add_status_code(100).add_data(order_schema.dump(updated_order))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Order not found").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

@order_routes.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id: int):
    response_builder = ResponseBuilder()
    order_service.delete_order(id)
    response_builder.add_message("Order deleted").add_status_code(100).add_data({'id': id})
    return response_schema.dump(response_builder.build()), 204
