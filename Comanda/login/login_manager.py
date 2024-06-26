# comanda/login/login_manager.py
import psycopg2
from comanda.connection.connection import conectar_bd, cerrar_conexion
from comanda.login.password_utils import hash_password, check_password

class LoginManager:
    def __init__(self):
        self.connection, self.cursor = conectar_bd()

    def authenticate_user(self, username, password):
        try:
            query = "SELECT u.id_usuario, u.Nombre, u.Apellido, u.Rol_ID, l.password_hash FROM login l JOIN usuarios u ON l.id_usuario = u.id_usuario WHERE l.username = %s"
            self.cursor.execute(query, (username,))
            user = self.cursor.fetchone()
            
            if user:
                stored_hash = user[4]
                if check_password(password, stored_hash):
                    return user[:-1]  # Devuelve todos los campos menos el hash
                else:
                    return None
            else:
                return None
        except (Exception, psycopg2.Error) as error:
            print("Error en la autenticación:", error)
            return None

    def close_connection(self):
        cerrar_conexion(self.connection, self.cursor)
