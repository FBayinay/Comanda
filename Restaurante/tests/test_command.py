import unittest
import os
from app import create_app, db
from app.models import Command
from app.services import CommandService

command_service = CommandService()

class CommandTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()  # Usa la configuración por defecto
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

        # Definir variables reutilizables para los tests
        self.COMMAND_ID_MESA = 1
        self.COMMAND_ID_USUARIO = 1
        self.COMMAND_ESTADO = 'En Proceso'
        self.command = self.__get_command()

    def tearDown(self):
        db.session.remove()  # Elimina la sesión de la base de datos
        db.drop_all()  # Elimina todas las tablas
        self.app_context.pop()  # Elimina el contexto de la aplicación

    def test_app(self):
        self.assertIsNotNone(self.app)

    def test_command_save(self):
        saved_command = command_service.save(self.command)
        self.assertGreaterEqual(saved_command.id_comanda, 1)
        self.assertEqual(saved_command.id_mesa, self.COMMAND_ID_MESA)
        self.assertEqual(saved_command.id_usuario, self.COMMAND_ID_USUARIO)
        self.assertEqual(saved_command.estado, self.COMMAND_ESTADO)

    def test_command_update(self):
        saved_command = command_service.save(self.command)
        saved_command.estado = 'Finalizado'
        updated_command = command_service.update(saved_command, saved_command.id_comanda)
        self.assertEqual(updated_command.estado, 'Finalizado')

    def test_command_delete(self):
        saved_command = command_service.save(self.command)
        command_service.delete(saved_command.id_comanda)
        self.assertIsNone(command_service.find(saved_command.id_comanda))

    def test_command_all(self):
        command_service.save(self.command)
        commands = command_service.all()
        self.assertGreaterEqual(len(commands), 1)

    def test_command_find(self):
        saved_command = command_service.save(self.command)
        found_command = command_service.find(saved_command.id_comanda)
        self.assertEqual(found_command.id_comanda, saved_command.id_comanda)
        self.assertEqual(found_command.id_mesa, self.COMMAND_ID_MESA)
        self.assertEqual(found_command.id_usuario, self.COMMAND_ID_USUARIO)
        self.assertEqual(found_command.estado, self.COMMAND_ESTADO)

    def __get_command(self) -> Command:
        command = Command()
        command.id_mesa = self.COMMAND_ID_MESA
        command.id_usuario = self.COMMAND_ID_USUARIO
        command.estado = self.COMMAND_ESTADO
        return command

if __name__ == '__main__':
    unittest.main()
