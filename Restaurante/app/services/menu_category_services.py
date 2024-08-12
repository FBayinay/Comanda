from typing import List, Optional
from app.models import MenuCategory
from app.repositories import MenuCategoryRepository

repository = MenuCategoryRepository()

class MenuCategoryService:
    """
    MenuCategoryService class
    """
    def __init__(self):
        pass

    def create_category(self, categoria: str, descripcion: str) -> MenuCategory:
        """
        Create a new menu category entry
        :param categoria: str
        :param descripcion: str
        :return: MenuCategory
        """
        category = MenuCategory(categoria=categoria, descripcion=descripcion)
        return repository.save(category)

    def get_all_categories(self) -> List[MenuCategory]:
        """
        Get all menu categories
        :return: List[MenuCategory]
        """
        return repository.all()

    def get_category_by_id(self, id: int) -> Optional[MenuCategory]:
        """
        Get a menu category by its ID
        :param id: int
        :return: Optional[MenuCategory]
        """
        return repository.find(id)

    def update_category(self, id: int, categoria: Optional[str] = None, 
                        descripcion: Optional[str] = None) -> Optional[MenuCategory]:
        """
        Update an existing menu category entry
        :param id: int
        :param categoria: Optional[str]
        :param descripcion: Optional[str]
        :return: Optional[MenuCategory]
        """
        category = self.get_category_by_id(id)
        if category:
            if categoria is not None:
                category.categoria = categoria
            if descripcion is not None:
                category.descripcion = descripcion
            return repository.update(category, id)
        return None

    def delete_category(self, id: int) -> None:
        """
        Delete a menu category by its ID
        :param id: int
        """
        repository.delete(id)
