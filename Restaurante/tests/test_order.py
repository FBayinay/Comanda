import unittest
import os
from datetime import datetime
from app import create_app, db
from app.models import Order
from app.services import OrderService

order_service = OrderService()

class OrderServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Definir variables reutilizables para los tests
        self.order_data = {
            'id_usuario': 1,
            'id_producto': 1,
            'id_proveedor': 1,
            'cantidad': 10,
            'precio_unitario': 15.50,
            'precio_total': 155.00
        }

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_create_order(self):
        order = order_service.create_order(**self.order_data)
        self.assertIsNotNone(order.id_pedido)
        self.assertEqual(order.id_usuario, self.order_data['id_usuario'])
        self.assertEqual(order.precio_total, self.order_data['precio_total'])

    def test_get_all_orders(self):
        order_service.create_order(**self.order_data)
        orders = order_service.get_all_orders()
        self.assertGreaterEqual(len(orders), 1)

    def test_get_order_by_id(self):
        order = order_service.create_order(**self.order_data)
        fetched_order = order_service.get_order_by_id(order.id_pedido)
        self.assertEqual(fetched_order.id_pedido, order.id_pedido)
        self.assertEqual(fetched_order.id_usuario, self.order_data['id_usuario'])

    def test_update_order(self):
        order = order_service.create_order(**self.order_data)
        new_precio_unitario = 20.00
        new_precio_total = 200.00
        updated_order = order_service.update_order(order.id_pedido, 
                                                   precio_unitario=new_precio_unitario, 
                                                   precio_total=new_precio_total)
        self.assertEqual(updated_order.precio_unitario, new_precio_unitario)
        self.assertEqual(updated_order.precio_total, new_precio_total)

    def test_delete_order(self):
        order = order_service.create_order(**self.order_data)
        order_service.delete_order(order.id_pedido)
        self.assertIsNone(order_service.get_order_by_id(order.id_pedido))

if __name__ == '__main__':
    unittest.main()
