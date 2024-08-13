from typing import List, Optional
from app.models import User
from app.repositories import UserRepository

repository = UserRepository()

class UserService:
    """
    UserService class
    """
    def __init__(self):
        pass

    def create_user(self, nombre: str, apellido: str, dni: str, email: str, calle: str, 
                    numero: int,id_accion: int, rol_id: Optional[int] = None) -> Optional[User]:
        """
        Create a new user entry
        :param nombre: str
        :param apellido: str
        :param dni: str
        :param email: str
        :param calle: str
        :param numero: int
        :param id_accion: int
        :param rol_id: Optional[int]
        :return: Optional[User]
        """
        if repository.email_exists(email):
            raise ValueError("El email ya existe")
        if repository.dni_exists(dni):
            raise ValueError("El DNI ya existe")
        
        user = User(nombre=nombre, apellido=apellido, dni=dni, email=email, calle=calle, 
                    numero=numero, rol_id=rol_id, id_accion=id_accion)
        return repository.save(user)

    def get_all_users(self) -> List[User]:
        """
        Get all user entries
        :return: List[User]
        """
        return repository.all()

    def get_user_by_id(self, id: int) -> Optional[User]:
        """
        Get a user entry by its ID
        :param id: int
        :return: Optional[User]
        """
        return repository.find(id)

    def update_user(self, id: int, nombre: Optional[str] = None, apellido: Optional[str] = None, 
                    dni: Optional[str] = None, email: Optional[str] = None, calle: Optional[str] = None, 
                    numero: Optional[int] = None, rol_id: Optional[int] = None, 
                    id_accion: Optional[int] = None) -> Optional[User]:
        """
        Update an existing user entry
        :param id: int
        :param nombre: Optional[str]
        :param apellido: Optional[str]
        :param dni: Optional[str]
        :param email: Optional[str]
        :param calle: Optional[str]
        :param numero: Optional[int]
        :param rol_id: Optional[int]
        :param id_accion: Optional[int]
        :return: Optional[User]
        """
        user = self.get_user_by_id(id)
        if user:
            if nombre is not None:
                user.nombre = nombre
            if apellido is not None:
                user.apellido = apellido
            if dni is not None:
                if repository.dni_exists(dni) and dni != user.dni:
                    raise ValueError("El DNI ya existe")
                user.dni = dni
            if email is not None:
                if repository.email_exists(email) and email != user.email:
                    raise ValueError("El email ya existe")
                user.email = email
            if calle is not None:
                user.calle = calle
            if numero is not None:
                user.numero = numero
            if rol_id is not None:
                if not repository._role_exists(rol_id):
                    raise ValueError("El rol no existe")
                user.rol_id = rol_id
            if id_accion is not None:
                if not repository._action_exists(id_accion):
                    raise ValueError("La acción no existe")
                user.id_accion = id_accion
            return repository.update(user, id)
        return None

    def delete_user(self, id: int) -> None:
        """
        Delete a user entry by its ID
        :param id: int
        """
        repository.delete(id)
