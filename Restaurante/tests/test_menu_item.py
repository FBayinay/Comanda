import unittest
import os
from decimal import Decimal
from app import create_app, db
from app.models import Menu, MenuCategory, MenuItem
from app.services import MenuItemService

menu_item_service = MenuItemService()

class MenuItemServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Insertar datos de prueba para Menu y MenuCategory
        self.menu = Menu(tipo='Almuerzo', fecha_inicio='2024-01-01', fecha_fin='2024-12-31')
        self.category = MenuCategory(categoria='Principal', descripcion='Platos principales')
        db.session.add(self.menu)
        db.session.add(self.category)
        db.session.commit()

        # Definir variables reutilizables para los tests
        self.item_data = {
            'id_menu': self.menu.id_menu,
            'id_categoria': self.category.id_categoria,
            'nombre': 'Pizza',
            'precio': Decimal('9.99'),
            'descripcion': 'Delicious cheese pizza'
        }

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_create_item(self):
        item = menu_item_service.create_item(**self.item_data)
        self.assertIsNotNone(item.id_items)
        self.assertEqual(item.nombre, self.item_data['nombre'])
        self.assertEqual(item.precio, self.item_data['precio'])  # Comparar como Decimal

    def test_get_all_items(self):
        menu_item_service.create_item(**self.item_data)
        items = menu_item_service.get_all_items()
        self.assertGreaterEqual(len(items), 1)

    def test_get_item_by_id(self):
        item = menu_item_service.create_item(**self.item_data)
        fetched_item = menu_item_service.get_item_by_id(item.id_items)
        self.assertEqual(fetched_item.id_items, item.id_items)
        self.assertEqual(fetched_item.nombre, self.item_data['nombre'])

    def test_update_item(self):
        item = menu_item_service.create_item(**self.item_data)
        new_nombre = 'Vegan Pizza'
        new_precio = Decimal('11.99')  # Usar Decimal para comparar
        updated_item = menu_item_service.update_item(item.id_items, 
                                                     nombre=new_nombre, 
                                                     precio=new_precio)
        self.assertEqual(updated_item.nombre, new_nombre)
        self.assertEqual(updated_item.precio, new_precio)  # Comparar como Decimal

    def test_delete_item(self):
        item = menu_item_service.create_item(**self.item_data)
        menu_item_service.delete_item(item.id_items)
        self.assertIsNone(menu_item_service.get_item_by_id(item.id_items))

if __name__ == '__main__':
    unittest.main()
