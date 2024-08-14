import unittest
import os
from app import create_app, db
from app.models import Stock, Product
from app.services import StockService

# Crear un servicio de stock
stock_service = StockService()

class StockServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Agregar un producto para que pueda ser referenciado en las pruebas
        self.product = Product(nombre='Apple')
        db.session.add(self.product)
        db.session.commit()

        # Definir variables reutilizables para los tests
        self.stock_data = {
            'id_producto': self.product.id_producto,
            'cantidad': 100
        }

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_create_stock(self):
        stock = stock_service.create_stock(**self.stock_data)
        self.assertIsNotNone(stock.id_stock)
        self.assertEqual(stock.id_producto, self.stock_data['id_producto'])
        self.assertEqual(stock.cantidad, self.stock_data['cantidad'])

    def test_create_stock_invalid_product(self):
        with self.assertRaises(ValueError) as context:
            stock_service.create_stock(id_producto=999, cantidad=50)
        self.assertEqual(str(context.exception), "El producto no existe en la base de datos")

    def test_get_all_stocks(self):
        stock_service.create_stock(**self.stock_data)
        stocks = stock_service.get_all_stocks()
        self.assertGreaterEqual(len(stocks), 1)

    def test_get_stock_by_id(self):
        stock = stock_service.create_stock(**self.stock_data)
        fetched_stock = stock_service.get_stock_by_id(stock.id_stock)
        self.assertEqual(fetched_stock.id_stock, stock.id_stock)
        self.assertEqual(fetched_stock.id_producto, self.stock_data['id_producto'])

    def test_update_stock(self):
        stock = stock_service.create_stock(**self.stock_data)
        new_cantidad = 200
        updated_stock = stock_service.update_stock(stock.id_stock, cantidad=new_cantidad)
        self.assertEqual(updated_stock.cantidad, new_cantidad)

    def test_update_stock_invalid_product(self):
        stock = stock_service.create_stock(**self.stock_data)
        with self.assertRaises(ValueError) as context:
            stock_service.update_stock(stock.id_stock, id_producto=999)
        self.assertEqual(str(context.exception), "El producto no existe en la base de datos")

    def test_delete_stock(self):
        stock = stock_service.create_stock(**self.stock_data)
        stock_service.delete_stock(stock.id_stock)
        self.assertIsNone(stock_service.get_stock_by_id(stock.id_stock))

if __name__ == '__main__':
    unittest.main()
