from flask import Blueprint, request, jsonify
from app.mapping import SupplierSchema, ResponseSchema
from app.services.response_message_services import ResponseBuilder
from app.services.supplier_services import SupplierService

supplier_routes = Blueprint('supplier_routes', __name__)
supplier_schema = SupplierSchema()
response_schema = ResponseSchema()
supplier_service = SupplierService()

# Crear un nuevo proveedor (Create)
@supplier_routes.route('/proveedores', methods=['POST'])
def create_supplier():
    data = request.json
    response_builder = ResponseBuilder()

    if not all(key in data for key in ('nombre', 'contacto')):
        response_builder.add_message("Datos incompletos").add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

    try:
        new_supplier = supplier_service.create_supplier(data['nombre'], data['contacto'])
        response_builder.add_message("Proveedor creado").add_status_code(100).add_data(supplier_schema.dump(new_supplier))
        return response_schema.dump(response_builder.build()), 201
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Obtener todos los proveedores (Read)
@supplier_routes.route('/proveedores', methods=['GET'])
def get_suppliers():
    response_builder = ResponseBuilder()
    suppliers = supplier_service.get_all_suppliers()
    response_builder.add_message("Proveedores recuperados").add_status_code(100).add_data([supplier_schema.dump(supplier) for supplier in suppliers])
    return response_schema.dump(response_builder.build()), 200

# Obtener un proveedor por ID (Read)
@supplier_routes.route('/proveedores/<int:id>', methods=['GET'])
def get_supplier(id: int):
    response_builder = ResponseBuilder()
    supplier = supplier_service.get_supplier_by_id(id)
    if supplier:
        response_builder.add_message("Proveedor encontrado").add_status_code(100).add_data(supplier_schema.dump(supplier))
        return response_schema.dump(response_builder.build()), 200
    else:
        response_builder.add_message("Proveedor no encontrado").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404

# Actualizar un proveedor existente (Update)
@supplier_routes.route('/proveedores/<int:id>', methods=['PUT'])
def update_supplier(id: int):
    data = request.json
    response_builder = ResponseBuilder()

    if not any(key in data for key in ('nombre', 'contacto')):
        response_builder.add_message("Datos incompletos").add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

    try:
        updated_supplier = supplier_service.update_supplier(id, data.get('nombre'), data.get('contacto'))
        if updated_supplier:
            response_builder.add_message("Proveedor actualizado").add_status_code(100).add_data(supplier_schema.dump(updated_supplier))
            return response_schema.dump(response_builder.build()), 200
        else:
            response_builder.add_message("Proveedor no encontrado").add_status_code(300).add_data({'id': id})
            return response_schema.dump(response_builder.build()), 404
    except ValueError as e:
        response_builder.add_message(str(e)).add_status_code(300)
        return response_schema.dump(response_builder.build()), 400

# Eliminar un proveedor (Delete)
@supplier_routes.route('/proveedores/<int:id>', methods=['DELETE'])
def delete_supplier(id: int):
    response_builder = ResponseBuilder()
    supplier = supplier_service.get_supplier_by_id(id)
    if supplier:
        supplier_service.delete_supplier(id)
        response_builder.add_message("Proveedor eliminado").add_status_code(100).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 204
    else:
        response_builder.add_message("Proveedor no encontrado").add_status_code(300).add_data({'id': id})
        return response_schema.dump(response_builder.build()), 404
