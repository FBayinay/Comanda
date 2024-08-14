from typing import List, Optional
from app.models import Menu
from app import db

class MenuRepository:
    # Guardar un nuevo menú en la base de datos
    def save(self, menu: Menu) -> Menu:
        db.session.add(menu)  
        db.session.commit()   
        return menu           

    # Actualizar un menú existente en la base de datos
    def update(self, menu: Menu, id: int) -> Optional[Menu]:
        entity = self.find(id)  
        if entity is None:
            return None         
        entity.tipo = menu.tipo  
        entity.fecha_inicio = menu.fecha_inicio
        entity.fecha_fin = menu.fecha_fin
        db.session.commit()     
        return entity           

    # Eliminar un menú de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  
        if entity:
            db.session.delete(entity)  
            db.session.commit()        

    # Obtener todos los menús de la base de datos
    def all(self) -> List[Menu]:
        return db.session.query(Menu).all()  

    # Buscar un menú por ID
    def find(self, id: int) -> Optional[Menu]:
        return db.session.query(Menu).filter(Menu.id_menu == id).one_or_none()  
        
