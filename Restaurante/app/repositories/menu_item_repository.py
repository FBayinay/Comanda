from typing import List, Optional
from app.models import MenuItem
from app import db

class MenuItemRepository:
    # Guardar un nuevo ítem de menú en la base de datos
    def save(self, item: MenuItem) -> MenuItem:
        db.session.add(item)  
        db.session.commit()   
        return item           

    # Actualizar un ítem de menú existente en la base de datos
    def update(self, item: MenuItem, id: int) -> Optional[MenuItem]:
        entity = self.find(id)  
        if entity is None:
            return None         
        entity.id_menu = item.id_menu
        entity.id_categoria = item.id_categoria
        entity.nombre = item.nombre
        entity.descripcion = item.descripcion
        entity.precio = item.precio
        db.session.commit()   
        return entity         

    # Eliminar un ítem de menú de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  
        if entity:
            db.session.delete(entity)  
            db.session.commit()        

    # Obtener todos los ítems de menú de la base de datos
    def all(self) -> List[MenuItem]:
        return db.session.query(MenuItem).all()  

    # Buscar un ítem de menú por ID
    def find(self, id: int) -> Optional[MenuItem]:
        return db.session.query(MenuItem).filter(MenuItem.id_items == id).one_or_none()  
        
