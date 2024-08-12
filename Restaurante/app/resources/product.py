from flask import Blueprint, request, jsonify
from app.repositories import ProductRepository
from app.models.product import Product

product_routes = Blueprint('product_routes', __name__)
product_repo = ProductRepository()

# Crear un nuevo producto (Create)
@product_routes.route('/productos', methods=['POST'])
def create_product():
    data = request.json
    if 'nombre' not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    new_product = Product(
        nombre=data['nombre']
    )
    
    saved_product = product_repo.save(new_product)
    return jsonify({
        "id": saved_product.id_producto,
        "nombre": saved_product.nombre
    }), 201

# Obtener todos los productos (Read)
@product_routes.route('/productos', methods=['GET'])
def get_products():
    products = product_repo.all()
    return jsonify([{
        "id": product.id_producto,
        "nombre": product.nombre
    } for product in products])

# Obtener un producto por ID (Read)
@product_routes.route('/productos/<int:id>', methods=['GET'])
def get_product(id):
    product = product_repo.find(id)
    if product:
        return jsonify({
            "id": product.id_producto,
            "nombre": product.nombre
        })
    return jsonify({"error": "Producto no encontrado"}), 404

# Actualizar un producto existente (Update)
@product_routes.route('/productos/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    if 'nombre' not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    product = Product(
        nombre=data['nombre']
    )
    
    updated_product = product_repo.update(product, id)
    if updated_product:
        return jsonify({
            "id": updated_product.id_producto,
            "nombre": updated_product.nombre
        })
    return jsonify({"error": "Producto no encontrado"}), 404

# Eliminar un producto (Delete)
@product_routes.route('/productos/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = product_repo.find(id)
    if product:
        product_repo.delete(id)
        return jsonify({"message": "Producto eliminado"}), 204
    return jsonify({"error": "Producto no encontrado"}), 404
