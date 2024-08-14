import unittest
import os
from app import create_app, db
from app.models import Supplier
from app.services import SupplierService

# Crear un servicio de proveedores
supplier_service = SupplierService()

class SupplierServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Definir variables reutilizables para los tests
        self.supplier_data = {
            'nombre': 'Proveedor Test',
            'contacto': '1234567890'
        }

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_create_supplier(self):
        supplier = supplier_service.create_supplier(**self.supplier_data)
        self.assertIsNotNone(supplier.id_proveedor)
        self.assertEqual(supplier.nombre, self.supplier_data['nombre'])
        self.assertEqual(supplier.contacto, self.supplier_data['contacto'])

    def test_get_all_suppliers(self):
        supplier_service.create_supplier(**self.supplier_data)
        suppliers = supplier_service.get_all_suppliers()
        self.assertGreaterEqual(len(suppliers), 1)

    def test_get_supplier_by_id(self):
        supplier = supplier_service.create_supplier(**self.supplier_data)
        fetched_supplier = supplier_service.get_supplier_by_id(supplier.id_proveedor)
        self.assertEqual(fetched_supplier.id_proveedor, supplier.id_proveedor)
        self.assertEqual(fetched_supplier.nombre, self.supplier_data['nombre'])

    def test_update_supplier(self):
        supplier = supplier_service.create_supplier(**self.supplier_data)
        new_nombre = 'Proveedor Actualizado'
        new_contacto = '0987654321'
        updated_supplier = supplier_service.update_supplier(supplier.id_proveedor, nombre=new_nombre, contacto=new_contacto)
        self.assertEqual(updated_supplier.nombre, new_nombre)
        self.assertEqual(updated_supplier.contacto, new_contacto)

    def test_delete_supplier(self):
        supplier = supplier_service.create_supplier(**self.supplier_data)
        supplier_service.delete_supplier(supplier.id_proveedor)
        self.assertIsNone(supplier_service.get_supplier_by_id(supplier.id_proveedor))

if __name__ == '__main__':
    unittest.main()
