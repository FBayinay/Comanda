from typing import List, Optional
from app.models import MenuItem
from app import db

class MenuItemRepository:
    # Guardar un nuevo ítem de menú en la base de datos
    def save(self, item: MenuItem) -> MenuItem:
        db.session.add(item)  # Añadir el objeto MenuItem a la sesión de base de datos
        db.session.commit()   # Confirmar (commit) la transacción para guardar los cambios
        return item           # Retornar el objeto MenuItem guardado

    # Actualizar un ítem de menú existente en la base de datos
    def update(self, item: MenuItem, id: int) -> Optional[MenuItem]:
        entity = self.find(id)  # Buscar el ítem existente por ID
        if entity is None:
            return None         # Si no se encuentra el ítem, retornar None
        entity.id_menu = item.id_menu
        entity.id_categoria = item.id_categoria
        entity.nombre = item.nombre
        entity.descripcion = item.descripcion
        entity.precio = item.precio
        db.session.commit()   # Confirmar los cambios
        return entity         # Retornar el ítem actualizado

    # Eliminar un ítem de menú de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  # Buscar el ítem existente por ID
        if entity:
            db.session.delete(entity)  # Eliminar el ítem de la sesión de base de datos
            db.session.commit()        # Confirmar la transacción

    # Obtener todos los ítems de menú de la base de datos
    def all(self) -> List[MenuItem]:
        return db.session.query(MenuItem).all()  # Obtener y retornar todos los ítems de menú

    # Buscar un ítem de menú por ID
    def find(self, id: int) -> Optional[MenuItem]:
        return db.session.query(MenuItem).filter(MenuItem.id_items == id).one_or_none()  
        # Buscar el ítem por ID y retornar uno o ninguno (si no se encuentra)
