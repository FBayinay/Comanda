import unittest
import os
from app import create_app, db
from app.models import Table
from app.services import TableService

# Crear un servicio de mesas
table_service = TableService()

class TableServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Definir variables reutilizables para los tests
        self.table_data = {
            'numero_mesa': 5,
            'capacidad': 4,
            'estado': 'Disponible'
        }

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_create_table(self):
        table = table_service.create_table(**self.table_data)
        self.assertIsNotNone(table.id_mesa)
        self.assertEqual(table.numero_mesa, self.table_data['numero_mesa'])
        self.assertEqual(table.capacidad, self.table_data['capacidad'])
        self.assertEqual(table.estado, self.table_data['estado'])

    def test_get_all_tables(self):
        table_service.create_table(**self.table_data)
        tables = table_service.get_all_tables()
        self.assertGreaterEqual(len(tables), 1)

    def test_get_table_by_id(self):
        table = table_service.create_table(**self.table_data)
        fetched_table = table_service.get_table_by_id(table.id_mesa)
        self.assertEqual(fetched_table.id_mesa, table.id_mesa)
        self.assertEqual(fetched_table.numero_mesa, self.table_data['numero_mesa'])

    def test_update_table(self):
        table = table_service.create_table(**self.table_data)
        new_numero_mesa = 6
        new_capacidad = 6
        new_estado = 'Ocupado'
        updated_table = table_service.update_table(table.id_mesa, 
                                                   numero_mesa=new_numero_mesa, 
                                                   capacidad=new_capacidad, 
                                                   estado=new_estado)
        self.assertEqual(updated_table.numero_mesa, new_numero_mesa)
        self.assertEqual(updated_table.capacidad, new_capacidad)
        self.assertEqual(updated_table.estado, new_estado)

    def test_delete_table(self):
        table = table_service.create_table(**self.table_data)
        table_service.delete_table(table.id_mesa)
        self.assertIsNone(table_service.get_table_by_id(table.id_mesa))

if __name__ == '__main__':
    unittest.main()
