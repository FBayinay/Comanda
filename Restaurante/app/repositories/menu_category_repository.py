from typing import List, Optional
from app.models import MenuCategory
from app import db

class MenuCategoryRepository:
    # Guardar una nueva categoría de menú en la base de datos
    def save(self, category: MenuCategory) -> MenuCategory:
        db.session.add(category)  
        db.session.commit()       
        return category           

    # Actualizar una categoría de menú existente en la base de datos
    def update(self, category: MenuCategory, id: int) -> Optional[MenuCategory]:
        entity = self.find(id)  
        if entity is None:
            return None         
        entity.categoria = category.categoria  
        entity.descripcion = category.descripcion
        db.session.commit()   
        return entity         

    # Eliminar una categoría de menú de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  
        if entity:
            db.session.delete(entity)  
            db.session.commit()        

    # Obtener todas las categorías de menú de la base de datos
    def all(self) -> List[MenuCategory]:
        return db.session.query(MenuCategory).all()  

    # Buscar una categoría de menú por ID
    def find(self, id: int) -> Optional[MenuCategory]:
        return db.session.query(MenuCategory).filter(MenuCategory.id_categoria == id).one_or_none()  
        
