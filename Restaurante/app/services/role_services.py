from typing import List, Optional
from app.models import Role
from app.repositories import RoleRepository

repository = RoleRepository()

class RoleService:
    """
    RoleService class
    """
    def __init__(self):
        pass

    def save(self, role: Role) -> Role:
        """
        Save a role
        :param role: Role
        :return: Role
        """
        repository.save(role)
        return role

    def update(self, role: Role, id: int) -> Optional[Role]:
        """
        Update a role
        :param role: Role
        :param id: int
        :return: Role
        """
        return repository.update(role, id)

    def delete(self, id: int) -> None:
        """
        Delete a role
        :param id: int
        """
        repository.delete(id)

    def all(self) -> List[Role]:
        """
        Get all roles
        :return: List[Role]
        """
        return repository.all()

    def find(self, id: int) -> Optional[Role]:
        """
        Get a role by id
        :param id: int
        :return: Optional[Role]
        """
        return repository.find(id)
