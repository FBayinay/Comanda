from flask import Blueprint, request, jsonify
from app.repositories import StockRepository
from app.models import Stock

stock_routes = Blueprint('stock_routes', __name__)
stock_repo = StockRepository()

# Crear un nuevo stock (Create)
@stock_routes.route('/stock', methods=['POST'])
def create_stock():
    data = request.json
    if not all(key in data for key in ('id_producto', 'cantidad')):
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        new_stock = Stock(
            id_producto=data['id_producto'],
            cantidad=data['cantidad']
        )
        saved_stock = stock_repo.save(new_stock)
        return jsonify({
            "id": saved_stock.id_stock,
            "id_producto": saved_stock.id_producto,
            "cantidad": saved_stock.cantidad
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener todos los stocks (Read)
@stock_routes.route('/stock', methods=['GET'])
def get_stocks():
    stocks = stock_repo.all()
    return jsonify([{
        "id": stock.id_stock,
        "id_producto": stock.id_producto,
        "cantidad": stock.cantidad
    } for stock in stocks])

# Obtener un stock por ID (Read)
@stock_routes.route('/stock/<int:id>', methods=['GET'])
def get_stock(id):
    stock = stock_repo.find(id)
    if stock:
        return jsonify({
            "id": stock.id_stock,
            "id_producto": stock.id_producto,
            "cantidad": stock.cantidad
        })
    return jsonify({"error": "Stock no encontrado"}), 404

# Actualizar un stock existente (Update)
@stock_routes.route('/stock/<int:id>', methods=['PUT'])
def update_stock(id):
    data = request.json
    if not all(key in data for key in ('id_producto', 'cantidad')):
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        stock = Stock(
            id_producto=data['id_producto'],
            cantidad=data['cantidad']
        )
        updated_stock = stock_repo.update(stock, id)
        if updated_stock:
            return jsonify({
                "id": updated_stock.id_stock,
                "id_producto": updated_stock.id_producto,
                "cantidad": updated_stock.cantidad
            })
        return jsonify({"error": "Stock no encontrado"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Eliminar un stock (Delete)
@stock_routes.route('/stock/<int:id>', methods=['DELETE'])
def delete_stock(id):
    stock = stock_repo.find(id)
    if stock:
        stock_repo.delete(id)
        return jsonify({"message": "Stock eliminado"}), 204
    return jsonify({"error": "Stock no encontrado"}), 404
