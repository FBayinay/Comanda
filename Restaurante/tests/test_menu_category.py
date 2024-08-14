import unittest
import os
from app import create_app, db
from app.models import MenuCategory
from app.services import MenuCategoryService

menu_category_service = MenuCategoryService()

class MenuCategoryServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Definir variables reutilizables para los tests
        self.category_data = {
            'categoria': 'Beverages',
            'descripcion': 'Drinks and beverages'
        }

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_create_category(self):
        category = menu_category_service.create_category(**self.category_data)
        self.assertIsNotNone(category.id_categoria)
        self.assertEqual(category.categoria, self.category_data['categoria'])
        self.assertEqual(category.descripcion, self.category_data['descripcion'])

    def test_get_all_categories(self):
        menu_category_service.create_category(**self.category_data)
        categories = menu_category_service.get_all_categories()
        self.assertGreaterEqual(len(categories), 1)

    def test_get_category_by_id(self):
        category = menu_category_service.create_category(**self.category_data)
        fetched_category = menu_category_service.get_category_by_id(category.id_categoria)
        self.assertEqual(fetched_category.id_categoria, category.id_categoria)
        self.assertEqual(fetched_category.categoria, self.category_data['categoria'])

    def test_update_category(self):
        category = menu_category_service.create_category(**self.category_data)
        new_categoria = 'Desserts'
        new_descripcion = 'Sweet dishes'
        updated_category = menu_category_service.update_category(category.id_categoria, 
                                                                 categoria=new_categoria, 
                                                                 descripcion=new_descripcion)
        self.assertEqual(updated_category.categoria, new_categoria)
        self.assertEqual(updated_category.descripcion, new_descripcion)

    def test_delete_category(self):
        category = menu_category_service.create_category(**self.category_data)
        menu_category_service.delete_category(category.id_categoria)
        self.assertIsNone(menu_category_service.get_category_by_id(category.id_categoria))

if __name__ == '__main__':
    unittest.main()
