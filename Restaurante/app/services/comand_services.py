from typing import List, Optional
from app.models import Command
from app.repositories import CommandRepository

repository = CommandRepository()

class CommandService:
    """
    CommandService class
    """
    def __init__(self):
        pass

    def save(self, command: Command) -> Command:
        """
        Save a new command
        :param command: Command
        :return: Command
        """
        return repository.save(command)

    def update(self, command: Command, id: int) -> Optional[Command]:
        """
        Update an existing command
        :param command: Command
        :param id: int
        :return: Optional[Command]
        """
        return repository.update(command, id)

    def delete(self, id: int) -> None:
        """
        Delete a command by id
        :param id: int
        """
        repository.delete(id)

    def all(self) -> List[Command]:
        """
        Get all commands
        :return: List[Command]
        """
        return repository.all()

    def find(self, id: int) -> Optional[Command]:
        """
        Find a command by id
        :param id: int
        :return: Optional[Command]
        """
        return repository.find(id)
