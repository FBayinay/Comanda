from typing import List, Optional
from app.models import MenuItem
from app.repositories import MenuItemRepository

repository = MenuItemRepository()

class MenuItemService:
    """
    MenuItemService class
    """
    def __init__(self):
        pass

    def create_item(self, id_menu: int, id_categoria: int, nombre: str, 
                    precio: float, descripcion: Optional[str] = None) -> MenuItem:
        """
        Create a new menu item entry
        :param id_menu: int
        :param id_categoria: int
        :param nombre: str
        :param precio: float
        :param descripcion: Optional[str]
        :return: MenuItem
        """
        item = MenuItem(id_menu=id_menu, id_categoria=id_categoria, nombre=nombre, 
                        descripcion=descripcion, precio=precio)
        return repository.save(item)

    def get_all_items(self) -> List[MenuItem]:
        """
        Get all menu items
        :return: List[MenuItem]
        """
        return repository.all()

    def get_item_by_id(self, id: int) -> Optional[MenuItem]:
        """
        Get a menu item by its ID
        :param id: int
        :return: Optional[MenuItem]
        """
        return repository.find(id)

    def update_item(self, id: int, id_menu: Optional[int] = None, 
                    id_categoria: Optional[int] = None, nombre: Optional[str] = None, 
                    descripcion: Optional[str] = None, precio: Optional[float] = None) -> Optional[MenuItem]:
        """
        Update an existing menu item entry
        :param id: int
        :param id_menu: Optional[int]
        :param id_categoria: Optional[int]
        :param nombre: Optional[str]
        :param descripcion: Optional[str]
        :param precio: Optional[float]
        :return: Optional[MenuItem]
        """
        item = self.get_item_by_id(id)
        if item:
            if id_menu is not None:
                item.id_menu = id_menu
            if id_categoria is not None:
                item.id_categoria = id_categoria
            if nombre is not None:
                item.nombre = nombre
            if descripcion is not None:
                item.descripcion = descripcion
            if precio is not None:
                item.precio = precio
            return repository.update(item, id)
        return None

    def delete_item(self, id: int) -> None:
        """
        Delete a menu item by its ID
        :param id: int
        """
        repository.delete(id)
