# comanda/login/role_authenticator.py

class RoleAuthenticator:
    @staticmethod
    def check_role(user_data, required_role_id):
        """
        Verifica si el usuario tiene el rol requerido.

        Args:
        - user_data: Tupla de datos del usuario (id_usuario, Nombre, Apellido, rol_id).
        - required_role_id: ID del rol requerido para acceder.

        Returns:
        - bool: True si el usuario tiene el rol requerido, False de lo contrario.
        """
        if user_data and user_data[3] == required_role_id:
            return True
        else:
            return False
