from typing import List,Optional
from app.models import Menu
from app.repositories import MenuRepository

repository = MenuRepository()

class MenuService:
    """
    MenuService class
    """
    def __init__(self):
        pass

    def create_menu(self, tipo: str, fecha_inicio: str, fecha_fin: Optional[str] = None) -> Menu:
        """
        Create a new menu entry
        :param tipo: str
        :param fecha_inicio: str
        :param fecha_fin: Optional[str]
        :return: Menu
        """
        menu = Menu(tipo=tipo, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        return repository.save(menu)

    def get_all_menus(self) -> List[Menu]:
        """
        Get all menu entries
        :return: List[Menu]
        """
        return repository.all()

    def get_menu_by_id(self, id: int) -> Optional[Menu]:
        """
        Get a menu entry by its ID
        :param id: int
        :return: Optional[Menu]
        """
        return repository.find(id)

    def update_menu(self, id: int, tipo: Optional[str] = None, 
                    fecha_inicio: Optional[str] = None, 
                    fecha_fin: Optional[str] = None) -> Optional[Menu]:
        """
        Update an existing menu entry
        :param id: int
        :param tipo: Optional[str]
        :param fecha_inicio: Optional[str]
        :param fecha_fin: Optional[str]
        :return: Optional[Menu]
        """
        menu = self.get_menu_by_id(id)
        if menu:
            if tipo is not None:
                menu.tipo = tipo
            if fecha_inicio is not None:
                menu.fecha_inicio = fecha_inicio
            if fecha_fin is not None:
                menu.fecha_fin = fecha_fin
            return repository.update(menu, id)
        return None

    def delete_menu(self, id: int) -> None:
        """
        Delete a menu entry by its ID
        :param id: int
        """
        repository.delete(id)
