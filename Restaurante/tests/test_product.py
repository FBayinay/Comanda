import unittest
import os
from app import create_app, db
from app.models import Product
from app.services import ProductService

product_service = ProductService()

class ProductServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Definir variables reutilizables para los tests
        self.product_data = {
            'nombre': 'Apple'
        }

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_create_product(self):
        product = product_service.create_product(**self.product_data)
        self.assertIsNotNone(product.id_producto)
        self.assertEqual(product.nombre, self.product_data['nombre'])

    def test_get_all_products(self):
        product_service.create_product(**self.product_data)
        products = product_service.get_all_products()
        self.assertGreaterEqual(len(products), 1)

    def test_get_product_by_id(self):
        product = product_service.create_product(**self.product_data)
        fetched_product = product_service.get_product_by_id(product.id_producto)
        self.assertEqual(fetched_product.id_producto, product.id_producto)
        self.assertEqual(fetched_product.nombre, self.product_data['nombre'])

    def test_update_product(self):
        product = product_service.create_product(**self.product_data)
        new_nombre = 'Orange'
        updated_product = product_service.update_product(product.id_producto, nombre=new_nombre)
        self.assertEqual(updated_product.nombre, new_nombre)

    def test_delete_product(self):
        product = product_service.create_product(**self.product_data)
        product_service.delete_product(product.id_producto)
        self.assertIsNone(product_service.get_product_by_id(product.id_producto))

if __name__ == '__main__':
    unittest.main()
