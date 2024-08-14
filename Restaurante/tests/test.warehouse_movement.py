import unittest
import os
from datetime import datetime
from app import create_app, db
from app.models import WarehouseMovement
from app.services import MovementService

# Crear un servicio de movimientos de almacén
movement_service = MovementService()

class MovementServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración de pruebas
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Definir variables reutilizables para los tests
        self.movement_data = {
            'id_usuario': 1,
            'id_producto': 1,
            'cantidad': 10,
            'fecha': datetime(2024, 8, 13, 10, 0, 0)
        }

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_create_movement(self):
        movement = movement_service.create_movement(**self.movement_data)
        self.assertIsNotNone(movement.id_movimiento)
        self.assertEqual(movement.id_usuario, self.movement_data['id_usuario'])
        self.assertEqual(movement.id_producto, self.movement_data['id_producto'])
        self.assertEqual(movement.cantidad, self.movement_data['cantidad'])
        self.assertEqual(movement.fecha, self.movement_data['fecha'])

    def test_get_all_movements(self):
        movement_service.create_movement(**self.movement_data)
        movements = movement_service.get_all_movements()
        self.assertGreaterEqual(len(movements), 1)

    def test_get_movement_by_id(self):
        movement = movement_service.create_movement(**self.movement_data)
        fetched_movement = movement_service.get_movement_by_id(movement.id_movimiento)
        self.assertEqual(fetched_movement.id_movimiento, movement.id_movimiento)
        self.assertEqual(fetched_movement.id_usuario, self.movement_data['id_usuario'])

    def test_update_movement(self):
        movement = movement_service.create_movement(**self.movement_data)
        updated_cantidad = 20
        updated_movement = movement_service.update_movement(movement.id_movimiento, cantidad=updated_cantidad)
        self.assertEqual(updated_movement.cantidad, updated_cantidad)

    def test_update_movement_with_invalid_id(self):
        movement = movement_service.create_movement(**self.movement_data)
        invalid_id = movement.id_movimiento + 1
        updated_movement = movement_service.update_movement(invalid_id, cantidad=20)
        self.assertIsNone(updated_movement)

    def test_delete_movement(self):
        movement = movement_service.create_movement(**self.movement_data)
        movement_service.delete_movement(movement.id_movimiento)
        self.assertIsNone(movement_service.get_movement_by_id(movement.id_movimiento))

if __name__ == '__main__':
    unittest.main()
