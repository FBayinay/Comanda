from typing import List, Optional
from app.models import MenuCategory
from app import db

class MenuCategoryRepository:
    # Guardar una nueva categoría de menú en la base de datos
    def save(self, category: MenuCategory) -> MenuCategory:
        db.session.add(category)  # Añadir el objeto MenuCategory a la sesión de base de datos
        db.session.commit()       # Confirmar (commit) la transacción para guardar los cambios
        return category           # Retornar el objeto MenuCategory guardado

    # Actualizar una categoría de menú existente en la base de datos
    def update(self, category: MenuCategory, id: int) -> Optional[MenuCategory]:
        entity = self.find(id)  # Buscar la categoría existente por ID
        if entity is None:
            return None         # Si no se encuentra la categoría, retornar None
        entity.categoria = category.categoria  # Actualizar la categoría
        entity.descripcion = category.descripcion
        db.session.commit()   # Confirmar los cambios
        return entity         # Retornar la categoría actualizada

    # Eliminar una categoría de menú de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  # Buscar la categoría existente por ID
        if entity:
            db.session.delete(entity)  # Eliminar la categoría de la sesión de base de datos
            db.session.commit()        # Confirmar la transacción

    # Obtener todas las categorías de menú de la base de datos
    def all(self) -> List[MenuCategory]:
        return db.session.query(MenuCategory).all()  # Obtener y retornar todas las categorías de menú

    # Buscar una categoría de menú por ID
    def find(self, id: int) -> Optional[MenuCategory]:
        return db.session.query(MenuCategory).filter(MenuCategory.id_categoria == id).one_or_none()  
        # Buscar la categoría por ID y retornar uno o ninguno (si no se encuentra)
