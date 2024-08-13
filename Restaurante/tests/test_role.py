import unittest
import os
from app import create_app, db
from app.models import Role
from app.services import RoleService

role_service = RoleService()

class RoleTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Definir variables reutilizables para los tests
        self.ROL_NAME = 'AdminTest'

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_app(self):
        self.assertIsNotNone(self.app)

    def test_role(self):
        role = self.__get_role()
        self.assertEqual(role.nombre, self.ROL_NAME)

    def test_role_save(self):
        role = self.__get_role()
        role_service.save(role)
        self.assertGreaterEqual(role.id_rol, 1)
        self.assertEqual(role.nombre, self.ROL_NAME)

    def test_role_update(self):
        role = self.__get_role()
        role_service.save(role)
        role.nombre = 'Admin Update'
        role_service.update(role, role.id_rol)
        self.assertEqual(role.nombre, 'Admin Update')

    def test_role_delete(self):
        role = self.__get_role()
        role_service.save(role)
        role_service.delete(role.id_rol)
        self.assertIsNone(role_service.find(role.id_rol))

    def test_role_all(self):
        role = self.__get_role()
        role_service.save(role)
        roles = role_service.all()
        self.assertGreaterEqual(len(roles), 1)

    def test_role_find(self):
        role = self.__get_role()
        role_service.save(role)
        role_find = role_service.find(role.id_rol)
        self.assertEqual(role_find.nombre, self.ROL_NAME)


    def __get_role(self) -> Role:
        role = Role()
        role.nombre = self.ROL_NAME
        return role

if __name__ == '__main__':
    unittest.main()
