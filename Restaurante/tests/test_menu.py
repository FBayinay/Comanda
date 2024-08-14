import unittest
import os
from app import create_app, db
from app.models import Menu
from app.services import MenuService

menu_service = MenuService()

class MenuServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Definir variables reutilizables para los tests
        self.menu_data = {
            'tipo': 'Lunch',
            'fecha_inicio': '2024-08-01',
            'fecha_fin': '2024-08-31'
        }

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_create_menu(self):
        menu = menu_service.create_menu(**self.menu_data)
        self.assertIsNotNone(menu.id_menu)
        self.assertEqual(menu.tipo, self.menu_data['tipo'])
        self.assertEqual(menu.fecha_inicio, self.menu_data['fecha_inicio'])

    def test_get_all_menus(self):
        menu_service.create_menu(**self.menu_data)
        menus = menu_service.get_all_menus()
        self.assertGreaterEqual(len(menus), 1)

    def test_get_menu_by_id(self):
        menu = menu_service.create_menu(**self.menu_data)
        fetched_menu = menu_service.get_menu_by_id(menu.id_menu)
        self.assertEqual(fetched_menu.id_menu, menu.id_menu)
        self.assertEqual(fetched_menu.tipo, self.menu_data['tipo'])

    def test_update_menu(self):
        menu = menu_service.create_menu(**self.menu_data)
        new_tipo = 'Dinner'
        new_fecha_fin = '2024-09-30'
        updated_menu = menu_service.update_menu(menu.id_menu, 
                                                tipo=new_tipo, 
                                                fecha_fin=new_fecha_fin)
        self.assertEqual(updated_menu.tipo, new_tipo)
        self.assertEqual(updated_menu.fecha_fin, new_fecha_fin)

    def test_delete_menu(self):
        menu = menu_service.create_menu(**self.menu_data)
        menu_service.delete_menu(menu.id_menu)
        self.assertIsNone(menu_service.get_menu_by_id(menu.id_menu))

if __name__ == '__main__':
    unittest.main()
