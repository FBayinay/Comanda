from typing import List, Optional
from app.models import CommandDetail
from app.repositories import CommandDetailRepository

repository = CommandDetailRepository()

class CommandDetailService:
    """
    CommandDetailService class
    """
    def __init__(self):
        pass

    def save(self, command_detail: CommandDetail) -> CommandDetail:
        """
        Save a new command detail
        :param command_detail: CommandDetail
        :return: CommandDetail
        """
        return repository.save(command_detail)

    def update(self, command_detail: CommandDetail, id: int) -> Optional[CommandDetail]:
        """
        Update an existing command detail
        :param command_detail: CommandDetail
        :param id: int
        :return: Optional[CommandDetail]
        """
        return repository.update(command_detail, id)

    def delete(self, id: int) -> None:
        """
        Delete a command detail by id
        :param id: int
        """
        repository.delete(id)

    def all(self) -> List[CommandDetail]:
        """
        Get all command details
        :return: List[CommandDetail]
        """
        return repository.all()

    def find(self, id: int) -> Optional[CommandDetail]:
        """
        Find a command detail by id
        :param id: int
        :return: Optional[CommandDetail]
        """
        return repository.find(id)
