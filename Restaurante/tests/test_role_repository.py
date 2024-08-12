import unittest
import os
from dotenv import load_dotenv
from app import create_app, db
from app.repositories import RoleRepository
from app.models import Role

class TestRoleRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv(dotenv_path='../docker/.env')  # Asegúrate de que esta ruta es correcta

    def setUp(self):
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DATABASE_URI')
        
        print(f"SQLALCHEMY_DATABASE_URI: {self.app.config['SQLALCHEMY_DATABASE_URI']}")
        
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
