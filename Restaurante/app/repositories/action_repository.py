from typing import List, Optional
from app.models import Action
from app import db

class ActionRepository:
    # Guardar un nueva acción en la base de datos
    def save(self, action: Action) -> Action:
        db.session.add(action)  
        db.session.commit()   
        return action           

    # Actualizar una acción existente en la base de datos
    def update(self, action: Action, id: int) -> Optional[Action]:
        entity = self.find(id)  
        if entity is None:
            return None         
        entity.nombre = action.nombre  
        db.session.commit()          
        return entity                

    # Eliminar una acción de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  
        if entity:
            db.session.delete(entity)  
            db.session.commit()        

    # Obtener todos los actions de la base de datos
    def all(self) -> List[Action]:
        return db.session.query(Action).all()  

    # Buscar una acción por ID
    def find(self, id: int) -> Optional[Action]:
        return db.session.query(Action).filter(Action.id_accion == id).one_or_none()  
        
