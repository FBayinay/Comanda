from typing import Optional
from app.models import Login
from app.repositories import LoginRepository
import bcrypt

repository = LoginRepository()

class LoginService:
    """
    LoginService class
    """
    def __init__(self):
        pass

    def hash_password(self, password: str) -> str:
        """
        Hash a password for storing.
        :param password: str
        :return: str
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str, hashed: str) -> bool:
        """
        Verify a stored password against one provided by user.
        :param password: str
        :param hashed: str
        :return: bool
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def create_login(self, id_usuario: int, username: str, password: str) -> Login:
        """
        Create a new login entry
        :param id_usuario: int
        :param username: str
        :param password: str
        :return: Login
        """
        password = self.hash_password(password)
        return repository.create_login(id_usuario, username, password)

    def get_login_by_id(self, login_id: int) -> Optional[Login]:
        """
        Get a login entry by its ID
        :param login_id: int
        :return: Optional[Login]
        """
        return repository.get_login_by_id(login_id)

    def get_login_by_username(self, username: str) -> Optional[Login]:
        """
        Get a login entry by username
        :param username: str
        :return: Optional[Login]
        """
        return repository.get_login_by_username(username)

    def update_login(self, login_id: int, id_usuario: Optional[int] = None, 
                     username: Optional[str] = None, 
                     password_hash: Optional[str] = None) -> Optional[Login]:
        """
        Update an existing login entry
        :param login_id: int
        :param id_usuario: Optional[int]
        :param username: Optional[str]
        :param password_hash: Optional[str]
        :return: Optional[Login]
        """
        return repository.update_login(login_id, id_usuario, username, password_hash)

    def delete_login(self, login_id: int) -> Optional[Login]:
        """
        Delete a login entry by its ID
        :param login_id: int
        :return: Optional[Login]
        """
        return repository.delete_login(login_id)
