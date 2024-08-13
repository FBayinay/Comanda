from flask import Blueprint, request, jsonify
from app.mapping import ReceiptSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.receipt_services import ReceiptService

receipt_routes = Blueprint('receipt_routes', __name__)
receipt_schema = ReceiptSchema()
response_schema = ResponseSchema()
receipt_service = ReceiptService()

# Crear un nuevo recibo (Create)
@receipt_routes.route('/receipts', methods=['POST'])
def create_receipt():
    data = request.json
    response_builder = ResponseBuilder()

    try:
        new_receipt = receipt_service.create_receipt(
            id_comanda=data['id_comanda'],
            total=data['total'],
            estado_pago=data.get('estado_pago', 'Pendiente'),
            detalles_comanda=data.get('detalles_comanda', None)
        )
        response_builder.add_message("Receipt created").add_status_code(100).add_data(receipt_schema.dump(new_receipt))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Obtener todos los recibos (Read)
@receipt_routes.route('/receipts', methods=['GET'])
def get_receipts():
    response_builder = ResponseBuilder()
    receipts = receipt_service.get_all_receipts()
    response_builder.add_message("Receipts retrieved").add_status_code(100).add_data([receipt_schema.dump(receipt) for receipt in receipts])
    return response_schema.dump(response_builder.build()), 200

# Obtener un recibo por ID (Read)
@receipt_routes.route('/receipts/<int:id>', methods=['GET'])
def get_receipt(id: int):
    response_builder = ResponseBuilder()
    receipt = receipt_service.get_receipt_by_id(id)
    if receipt:
        response_builder.add_message("Receipt found").add_status_code(100).add_data(receipt_schema.dump(receipt))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Receipt not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

# Actualizar un recibo existente (Update)
@receipt_routes.route('/receipts/<int:id>', methods=['PUT'])
def update_receipt(id: int):
    data = request.json
    response_builder = ResponseBuilder()

    try:
        updated_receipt = receipt_service.update_receipt(
            id=id,
            id_comanda=data.get('id_comanda', None),
            fecha=data.get('fecha', None),
            total=data.get('total', None),
            estado_pago=data.get('estado_pago', None),
            detalles_comanda=data.get('detalles_comanda', None)
        )
        if updated_receipt:
            response_builder.add_message("Receipt updated").add_status_code(100).add_data(receipt_schema.dump(updated_receipt))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Receipt not found").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Eliminar un recibo (Delete)
@receipt_routes.route('/receipts/<int:id>', methods=['DELETE'])
def delete_receipt(id: int):
    response_builder = ResponseBuilder()
    receipt = receipt_service.get_receipt_by_id(id)
    if receipt:
        receipt_service.delete_receipt(id)
        response_builder.add_message("Receipt deleted").add_status_code(100).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 204
    else:
        response_builder.add_message("Receipt not found").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404
