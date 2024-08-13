from flask import Blueprint, request, jsonify
from app.mapping import ProductSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.product_services import ProductService

product_routes = Blueprint('product_routes', __name__)
product_schema = ProductSchema()
response_schema = ResponseSchema()
product_service = ProductService()

@product_routes.route('/productos', methods=['POST'])
def create_product():
    data = request.json
    if 'nombre' not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    response_builder = ResponseBuilder()
    try:
        new_product = product_service.create_product(nombre=data['nombre'])
        response_builder.add_message("Product created").add_status_code(100).add_data(product_schema.dump(new_product))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

@product_routes.route('/productos', methods=['GET'])
def get_products():
    response_builder = ResponseBuilder()
    products = product_service.get_all_products()
    response_builder.add_message("Products retrieved").add_status_code(100).add_data([product_schema.dump(product) for product in products])
    return response_schema.dump(response_builder.build()), 200

@product_routes.route('/productos/<int:id>', methods=['GET'])
def get_product(id: int):
    response_builder = ResponseBuilder()
    product = product_service.get_product_by_id(id)
    if product:
        response_builder.add_message("Product found").add_status_code(100).add_data(product_schema.dump(product))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Product not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

@product_routes.route('/productos/<int:id>', methods=['PUT'])
def update_product(id: int):
    data = request.json
    if 'nombre' not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    response_builder = ResponseBuilder()
    try:
        updated_product = product_service.update_product(id, nombre=data['nombre'])
        if updated_product:
            response_builder.add_message("Product updated").add_status_code(100).add_data(product_schema.dump(updated_product))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Product not found").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

@product_routes.route('/productos/<int:id>', methods=['DELETE'])
def delete_product(id: int):
    response_builder = ResponseBuilder()
    product = product_service.get_product_by_id(id)
    if product:
        product_service.delete_product(id)
        response_builder.add_message("Product deleted").add_status_code(100).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 204
    else:
        response_builder.add_message("Product not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404
