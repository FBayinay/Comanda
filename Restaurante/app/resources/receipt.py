from flask import Blueprint, request, jsonify
from app.repositories import ReceiptRepository
from app.models import Receipt  # Importar desde app/models

receipt_routes = Blueprint('receipt_routes', __name__)
receipt_repo = ReceiptRepository()

# Crear un nuevo recibo (Create)
@receipt_routes.route('/receipts', methods=['POST'])
def create_receipt():
    data = request.json
    new_receipt = Receipt(
        id_comanda=data['id_comanda'],
        fecha=data.get('fecha', None),  # Si no se proporciona, se usa la fecha actual
        total=data['total'],
        estado_pago=data.get('estado_pago', 'Pendiente'),
        detalles_comanda=data.get('detalles_comanda', None)
    )
    saved_receipt = receipt_repo.save(new_receipt)
    return jsonify({
        "id": saved_receipt.id_recibo,
        "id_comanda": saved_receipt.id_comanda,
        "fecha": saved_receipt.fecha.isoformat(),  # Convertir a formato ISO para JSON
        "total": str(saved_receipt.total),  # Convertir a string para JSON
        "estado_pago": saved_receipt.estado_pago,
        "detalles_comanda": saved_receipt.detalles_comanda
    }), 201

# Obtener todos los recibos (Read)
@receipt_routes.route('/receipts', methods=['GET'])
def get_receipts():
    receipts = receipt_repo.all()
    return jsonify([{
        "id": receipt.id_recibo,
        "id_comanda": receipt.id_comanda,
        "fecha": receipt.fecha.isoformat(),  # Convertir a formato ISO para JSON
        "total": str(receipt.total),  # Convertir a string para JSON
        "estado_pago": receipt.estado_pago,
        "detalles_comanda": receipt.detalles_comanda
    } for receipt in receipts])

# Obtener un recibo por ID (Read)
@receipt_routes.route('/receipts/<int:id>', methods=['GET'])
def get_receipt(id):
    receipt = receipt_repo.find(id)
    if receipt:
        return jsonify({
            "id": receipt.id_recibo,
            "id_comanda": receipt.id_comanda,
            "fecha": receipt.fecha.isoformat(),  # Convertir a formato ISO para JSON
            "total": str(receipt.total),  # Convertir a string para JSON
            "estado_pago": receipt.estado_pago,
            "detalles_comanda": receipt.detalles_comanda
        })
    return jsonify({"error": "Receipt not found"}), 404

# Actualizar un recibo existente (Update)
@receipt_routes.route('/receipts/<int:id>', methods=['PUT'])
def update_receipt(id):
    data = request.json
    receipt = Receipt(
        id_comanda=data['id_comanda'],
        fecha=data.get('fecha', None),  # Si no se proporciona, se usa la fecha actual
        total=data['total'],
        estado_pago=data.get('estado_pago', 'Pendiente'),
        detalles_comanda=data.get('detalles_comanda', None)
    )
    updated_receipt = receipt_repo.update(receipt, id)
    if updated_receipt:
        return jsonify({
            "id": updated_receipt.id_recibo,
            "id_comanda": updated_receipt.id_comanda,
            "fecha": updated_receipt.fecha.isoformat(),  # Convertir a formato ISO para JSON
            "total": str(updated_receipt.total),  # Convertir a string para JSON
            "estado_pago": updated_receipt.estado_pago,
            "detalles_comanda": updated_receipt.detalles_comanda
        })
    return jsonify({"error": "Receipt not found"}), 404

# Eliminar un recibo (Delete)
@receipt_routes.route('/receipts/<int:id>', methods=['DELETE'])
def delete_receipt(id):
    receipt_repo.delete(id)
    return
