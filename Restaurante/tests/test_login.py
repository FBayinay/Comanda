import unittest
import os
from app import create_app, db
from app.models import User, Role, Action
from app.services import UserService

# Crear un servicio de usuarios
user_service = UserService()

class UserServiceTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración de pruebas
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Insertar datos de prueba para Role y Action
        self.role = Role(nombre='Administrador')
        self.action = Action(nombre='Login')
        db.session.add(self.role)
        db.session.add(self.action)
        db.session.commit()

        # Definir variables reutilizables para los tests
        self.user_data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'dni': '12345678',
            'email': 'juan.perez@example.com',
            'calle': 'Calle Falsa',
            'numero': 123,
            'id_accion': self.action.id_accion,
            'rol_id': self.role.id_rol
        }

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_create_user(self):
        user = user_service.create_user(**self.user_data)
        self.assertIsNotNone(user.id_usuario)
        self.assertEqual(user.nombre, self.user_data['nombre'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.rol_id, self.user_data['rol_id'])
        self.assertEqual(user.id_accion, self.user_data['id_accion'])

    def test_create_user_with_existing_email(self):
        user_service.create_user(**self.user_data)
        with self.assertRaises(ValueError) as context:
            user_service.create_user(nombre='Otro Nombre', apellido='Otro Apellido', 
                                     dni='87654321', email=self.user_data['email'], 
                                     calle='Otra Calle', numero=456, 
                                     id_accion=self.action.id_accion, rol_id=self.role.id_rol)
        self.assertEqual(str(context.exception), "El email ya existe")

    def test_create_user_with_existing_dni(self):
        user_service.create_user(**self.user_data)
        with self.assertRaises(ValueError) as context:
            user_service.create_user(nombre='Otro Nombre', apellido='Otro Apellido', 
                                     dni=self.user_data['dni'], email='otro.email@example.com', 
                                     calle='Otra Calle', numero=456, 
                                     id_accion=self.action.id_accion, rol_id=self.role.id_rol)
        self.assertEqual(str(context.exception), "El DNI ya existe")

    def test_get_all_users(self):
        user_service.create_user(**self.user_data)
        users = user_service.get_all_users()
        self.assertGreaterEqual(len(users), 1)

    def test_get_user_by_id(self):
        user = user_service.create_user(**self.user_data)
        fetched_user = user_service.get_user_by_id(user.id_usuario)
        self.assertEqual(fetched_user.id_usuario, user.id_usuario)
        self.assertEqual(fetched_user.email, self.user_data['email'])

    def test_update_user(self):
        user = user_service.create_user(**self.user_data)
        updated_email = 'nuevo.email@example.com'
        updated_user = user_service.update_user(user.id_usuario, email=updated_email)
        self.assertEqual(updated_user.email, updated_email)

    def test_update_user_with_existing_email(self):
        user_service.create_user(**self.user_data)
        other_user = user_service.create_user(nombre='Otro Nombre', apellido='Otro Apellido', 
                                              dni='87654321', email='otro.email@example.com', 
                                              calle='Otra Calle', numero=456, 
                                              id_accion=self.action.id_accion, rol_id=self.role.id_rol)
        with self.assertRaises(ValueError) as context:
            user_service.update_user(other_user.id_usuario, email=self.user_data['email'])
        self.assertEqual(str(context.exception), "El email ya existe")

    def test_update_user_with_existing_dni(self):
        user_service.create_user(**self.user_data)
        other_user = user_service.create_user(nombre='Otro Nombre', apellido='Otro Apellido', 
                                              dni='87654321', email='otro.email@example.com', 
                                              calle='Otra Calle', numero=456, 
                                              id_accion=self.action.id_accion, rol_id=self.role.id_rol)
        with self.assertRaises(ValueError) as context:
            user_service.update_user(other_user.id_usuario, dni=self.user_data['dni'])
        self.assertEqual(str(context.exception), "El DNI ya existe")

    def test_delete_user(self):
        user = user_service.create_user(**self.user_data)
        user_service.delete_user(user.id_usuario)
        self.assertIsNone(user_service.get_user_by_id(user.id_usuario))

if __name__ == '__main__':
    unittest.main()
