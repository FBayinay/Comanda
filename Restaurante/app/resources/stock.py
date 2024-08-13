from flask import Blueprint, request, jsonify
from app.mapping import StockSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.stock_services import StockService

stock_routes = Blueprint('stock_routes', __name__)
stock_schema = StockSchema()
response_schema = ResponseSchema()
stock_service = StockService()

# Crear un nuevo stock (Create)
@stock_routes.route('/stock', methods=['POST'])
def create_stock():
    data = request.json
    response_builder = ResponseBuilder()

    if not all(key in data for key in ('id_producto', 'cantidad')):
        response_builder.add_message("Datos incompletos").add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

    try:
        new_stock = stock_service.create_stock(data['id_producto'], data['cantidad'])
        response_builder.add_message("Stock creado").add_status_code(100).add_data(stock_schema.dump(new_stock))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Obtener todos los stocks (Read)
@stock_routes.route('/stock', methods=['GET'])
def get_stocks():
    response_builder = ResponseBuilder()
    stocks = stock_service.get_all_stocks()
    response_builder.add_message("Stocks recuperados").add_status_code(100).add_data([stock_schema.dump(stock) for stock in stocks])
    return response_schema.dump(response_builder.build()), 200

# Obtener un stock por ID (Read)
@stock_routes.route('/stock/<int:id>', methods=['GET'])
def get_stock(id: int):
    response_builder = ResponseBuilder()
    stock = stock_service.get_stock_by_id(id)
    if stock:
        response_builder.add_message("Stock encontrado").add_status_code(100).add_data(stock_schema.dump(stock))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Stock no encontrado").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

# Actualizar un stock existente (Update)
@stock_routes.route('/stock/<int:id>', methods=['PUT'])
def update_stock(id: int):
    data = request.json
    response_builder = ResponseBuilder()

    if not any(key in data for key in ('id_producto', 'cantidad')):
        response_builder.add_message("Datos incompletos").add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

    try:
        updated_stock = stock_service.update_stock(id, data.get('id_producto'), data.get('cantidad'))
        if updated_stock:
            response_builder.add_message("Stock actualizado").add_status_code(100).add_data(stock_schema.dump(updated_stock))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Stock no encontrado").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Eliminar un stock (Delete)
@stock_routes.route('/stock/<int:id>', methods=['DELETE'])
def delete_stock(id: int):
    response_builder = ResponseBuilder()
    stock = stock_service.get_stock_by_id(id)
    if stock:
        stock_service.delete_stock(id)
        response_builder.add_message("Stock eliminado").add_status_code(100).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 204
    else:
        response_builder.add_message("Stock no encontrado").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404
