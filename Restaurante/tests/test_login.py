import unittest
import os
from app import create_app, db
from app.models import User, Role, Action,Login
from app.services import LoginService

# Crear un servicio de login
login_service = LoginService()

class LoginServiceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['FLASK_CONTEXT'] = 'testing'
        cls.app = create_app() 
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.login_service = LoginService()
        # Crear roles y acciones de prueba
        self.role = Role(nombre='admin')
        db.session.add(self.role)
        self.action = Action(nombre='manage_users')
        db.session.add(self.action)
        db.session.commit()

        # Crear usuario de prueba
        self.user = User(
            nombre='Federico',
            apellido='Garcia',
            dni='12345678',
            email='fede@example.com',
            calle='Av. Siempre Viva',
            numero=742,
            rol_id=self.role.id_rol,
            id_accion=self.action.id_accion
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        Login.query.delete()
        User.query.delete()
        Role.query.delete()
        Action.query.delete()
        db.session.commit()

    def test_create_login(self):
        # Test para crear un nuevo login
        login = self.login_service.create_login(
            id_usuario=self.user.id_usuario,
            username='fedex',
            password='password123'
        )

        self.assertIsNotNone(login)
        self.assertEqual(login.id_usuario, self.user.id_usuario)
        self.assertTrue(self.login_service.check_password('password123', login.password_hash))

    def test_get_login_by_id(self):
        # Crear un login de prueba
        login = self.login_service.create_login(
            id_usuario=self.user.id_usuario,
            username='fedex',
            password='password123'
        )
        retrieved_login = self.login_service.get_login_by_id(login.id_login)
        self.assertIsNotNone(retrieved_login)
        self.assertEqual(retrieved_login.username, 'fedex')

    def test_get_login_by_username(self):
        # Crear un login de prueba
        login = self.login_service.create_login(
            id_usuario=self.user.id_usuario,
            username='fedex',
            password='password123'
        )
        retrieved_login = self.login_service.get_login_by_username('fedex')
        self.assertIsNotNone(retrieved_login)
        self.assertEqual(retrieved_login.id_login, login.id_login)

    def test_update_login(self):
        # Crear un login de prueba
        login = self.login_service.create_login(
            id_usuario=self.user.id_usuario,
            username='fedex',
            password='password123'
        )
        updated_login = self.login_service.update_login(
            login_id=login.id_login,
            username='fedex_updated'
        )
        self.assertIsNotNone(updated_login)
        self.assertEqual(updated_login.username, 'fedex_updated')

    def test_delete_login(self):
        # Crear un login de prueba
        login = self.login_service.create_login(
            id_usuario=self.user.id_usuario,
            username='fedex',
            password='password123'
        )
        deleted_login = self.login_service.delete_login(login.id_login)
        self.assertIsNotNone(deleted_login)
        self.assertIsNone(self.login_service.get_login_by_id(login.id_login))

if __name__ == '__main__':
    unittest.main()