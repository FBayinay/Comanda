import unittest
import os
from app import create_app, db
from app.repositories import RoleRepository
from app.models import Role

class TestRoleRepository(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()
        self.repo = RoleRepository()


    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_save_role(self):
        role = Role(nombre="Test Role")
        saved_role = self.repo.save(role)
        self.assertIsNotNone(saved_role.id_rol)
        self.assertEqual(saved_role.nombre, "Test Role")

if __name__ == '__main__':
    unittest.main()
