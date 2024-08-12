from flask import Blueprint, request, jsonify
from app.repositories import SupplierRepository
from app.models import Supplier

supplier_routes = Blueprint('supplier_routes', __name__)
supplier_repo = SupplierRepository()

# Crear un nuevo proveedor (Create)
@supplier_routes.route('/proveedores', methods=['POST'])
def create_supplier():
    data = request.json
    if not all(key in data for key in ('nombre', 'contacto')):
        return jsonify({"error": "Datos incompletos"}), 400

    new_supplier = Supplier(
        nombre=data['nombre'],
        contacto=data['contacto']
    )
    
    saved_supplier = supplier_repo.save(new_supplier)
    return jsonify({
        "id": saved_supplier.id_proveedor,
        "nombre": saved_supplier.nombre,
        "contacto": saved_supplier.contacto
    }), 201

# Obtener todos los proveedores (Read)
@supplier_routes.route('/proveedores', methods=['GET'])
def get_suppliers():
    suppliers = supplier_repo.all()
    return jsonify([{
        "id": supplier.id_proveedor,
        "nombre": supplier.nombre,
        "contacto": supplier.contacto
    } for supplier in suppliers])

# Obtener un proveedor por ID (Read)
@supplier_routes.route('/proveedores/<int:id>', methods=['GET'])
def get_supplier(id):
    supplier = supplier_repo.find(id)
    if supplier:
        return jsonify({
            "id": supplier.id_proveedor,
            "nombre": supplier.nombre,
            "contacto": supplier.contacto
        })
    return jsonify({"error": "Proveedor no encontrado"}), 404

# Actualizar un proveedor existente (Update)
@supplier_routes.route('/proveedores/<int:id>', methods=['PUT'])
def update_supplier(id):
    data = request.json
    if not all(key in data for key in ('nombre', 'contacto')):
        return jsonify({"error": "Datos incompletos"}), 400

    supplier = Supplier(
        nombre=data['nombre'],
        contacto=data['contacto']
    )
    
    updated_supplier = supplier_repo.update(supplier, id)
    if updated_supplier:
        return jsonify({
            "id": updated_supplier.id_proveedor,
            "nombre": updated_supplier.nombre,
            "contacto": updated_supplier.contacto
        })
    return jsonify({"error": "Proveedor no encontrado"}), 404

# Eliminar un proveedor (Delete)
@supplier_routes.route('/proveedores/<int:id>', methods=['DELETE'])
def delete_supplier(id):
    supplier = supplier_repo.find(id)
    if supplier:
        supplier_repo.delete(id)
        return jsonify({"message": "Proveedor eliminado"}), 204
    return jsonify({"error": "Proveedor no encontrado"}), 404
