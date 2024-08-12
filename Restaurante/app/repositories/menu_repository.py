from typing import List, Optional
from app.models import Menu
from app import db

class MenuRepository:
    # Guardar un nuevo menú en la base de datos
    def save(self, menu: Menu) -> Menu:
        db.session.add(menu)  # Añadir el objeto Menu a la sesión de base de datos
        db.session.commit()   # Confirmar (commit) la transacción para guardar los cambios
        return menu           # Retornar el objeto Menu guardado

    # Actualizar un menú existente en la base de datos
    def update(self, menu: Menu, id: int) -> Optional[Menu]:
        entity = self.find(id)  # Buscar el menú existente por ID
        if entity is None:
            return None         # Si no se encuentra el menú, retornar None
        entity.tipo = menu.tipo  # Actualizar el tipo del menú
        entity.fecha_inicio = menu.fecha_inicio
        entity.fecha_fin = menu.fecha_fin
        db.session.commit()     # Confirmar los cambios
        return entity           # Retornar el menú actualizado

    # Eliminar un menú de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  # Buscar el menú existente por ID
        if entity:
            db.session.delete(entity)  # Eliminar el menú de la sesión de base de datos
            db.session.commit()        # Confirmar la transacción

    # Obtener todos los menús de la base de datos
    def all(self) -> List[Menu]:
        return db.session.query(Menu).all()  # Obtener y retornar todos los menús

    # Buscar un menú por ID
    def find(self, id: int) -> Optional[Menu]:
        return db.session.query(Menu).filter(Menu.id_menu == id).one_or_none()  
        # Buscar el menú por ID y retornar uno o ninguno (si no se encuentra)
