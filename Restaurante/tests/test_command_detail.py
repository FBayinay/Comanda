import unittest
import os
from app import create_app, db
from app.models import CommandDetail
from app.services import CommandDetailService

command_detail_service = CommandDetailService()

class CommandDetailTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Definir variables reutilizables para los tests
        self.command_detail = self.__get_command_detail()

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_app(self):
        self.assertIsNotNone(self.app)

    def test_command_detail_save(self):
        saved_command_detail = command_detail_service.save(self.command_detail)
        self.assertGreaterEqual(saved_command_detail.id_detalles, 1)
        self.assertEqual(saved_command_detail.id_comanda, self.command_detail.id_comanda)
        self.assertEqual(saved_command_detail.id_item_menu, self.command_detail.id_item_menu)
        self.assertEqual(saved_command_detail.id_menu, self.command_detail.id_menu)
        self.assertEqual(saved_command_detail.cantidad, self.command_detail.cantidad)
        self.assertEqual(saved_command_detail.precio_total, self.command_detail.precio_total)

    def test_command_detail_update(self):
        saved_command_detail = command_detail_service.save(self.command_detail)
        saved_command_detail.cantidad = 10
        updated_command_detail = command_detail_service.update(saved_command_detail, saved_command_detail.id_detalles)
        self.assertEqual(updated_command_detail.cantidad, 10)

    def test_command_detail_delete(self):
        saved_command_detail = command_detail_service.save(self.command_detail)
        command_detail_service.delete(saved_command_detail.id_detalles)
        self.assertIsNone(command_detail_service.find(saved_command_detail.id_detalles))

    def test_command_detail_all(self):
        command_detail_service.save(self.command_detail)
        command_details = command_detail_service.all()
        self.assertGreaterEqual(len(command_details), 1)

    def test_command_detail_find(self):
        saved_command_detail = command_detail_service.save(self.command_detail)
        found_command_detail = command_detail_service.find(saved_command_detail.id_detalles)
        self.assertEqual(found_command_detail.id_detalles, saved_command_detail.id_detalles)
        self.assertEqual(found_command_detail.id_comanda, self.command_detail.id_comanda)
        self.assertEqual(found_command_detail.id_item_menu, self.command_detail.id_item_menu)
        self.assertEqual(found_command_detail.id_menu, self.command_detail.id_menu)
        self.assertEqual(found_command_detail.cantidad, self.command_detail.cantidad)
        self.assertEqual(found_command_detail.precio_total, self.command_detail.precio_total)

    def __get_command_detail(self) -> CommandDetail:
        command_detail = CommandDetail()
        command_detail.id_comanda = 1
        command_detail.id_item_menu = 1
        command_detail.id_menu = 1
        command_detail.cantidad = 5
        command_detail.precio_total = 100.00
        return command_detail

if __name__ == '__main__':
    unittest.main()
