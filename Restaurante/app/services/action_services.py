from typing import List, Optional
from app.models import Action
from app.repositories import ActionRepository

repository = ActionRepository()

class ActionService:
    """
    ActionService class
    """
    def __init__(self):
        pass

    def save(self, action: Action) -> Action:
        """
        Save a new action
        :param action: Action
        :return: Action
        """
        return repository.save(action)

    def update(self, action: Action, id: int) -> Optional[Action]:
        """
        Update an existing action
        :param action: Action
        :param id: int
        :return: Optional[Action]
        """
        return repository.update(action, id)

    def delete(self, id: int) -> None:
        """
        Delete an action by id
        :param id: int
        """
        repository.delete(id)

    def all(self) -> List[Action]:
        """
        Get all actions
        :return: List[Action]
        """
        return repository.all()

    def find(self, id: int) -> Optional[Action]:
        """
        Find an action by id
        :param id: int
        :return: Optional[Action]
        """
        return repository.find(id)
