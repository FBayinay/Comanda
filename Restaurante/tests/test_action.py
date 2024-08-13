import unittest
import os
from app import create_app, db
from app.models import Action
from app.services import ActionService

action_service = ActionService()

class ActionTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Definir variables reutilizables para los tests
        self.ACTION_NAME = 'LavarTest'

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_app(self):
        self.assertIsNotNone(self.app)

    def test_action(self):
        action = self.__get_action()
        self.assertEqual(action.nombre, self.ACTION_NAME)

    def test_action_save(self):
        action = self.__get_action()
        action_service.save(action)
        self.assertGreaterEqual(action.id_accion, 1)
        self.assertEqual(action.nombre, self.ACTION_NAME)

    def test_action_update(self):
        action = self.__get_action()
        action_service.save(action)
        action.nombre = 'Lavar Update'
        action_service.update(action, action.id_accion)
        self.assertEqual(action.nombre, 'Lavar Update')

    def test_action_delete(self):
        action = self.__get_action()
        action_service.save(action)
        action_service.delete(action.id_accion)
        self.assertIsNone(action_service.find(action.id_accion))

    def test_action_all(self):
        action = self.__get_action()
        action_service.save(action)
        actions = action_service.all()
        self.assertGreaterEqual(len(actions), 1)

    def test_action_find(self):
        action = self.__get_action()
        action_service.save(action)
        action_find = action_service.find(action.id_accion)
        self.assertEqual(action_find.nombre, self.ACTION_NAME)


    def __get_action(self) -> Action:
        action = Action()
        action.nombre = self.ACTION_NAME
        return action

if __name__ == '__main__':
    unittest.main()
