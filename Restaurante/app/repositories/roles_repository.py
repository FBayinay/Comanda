from typing import List, Optional
from app.models import Role
from app import db

class RoleRepository:
    # Guardar un nuevo rol en la base de datos
    def save(self, role: Role) -> Role:
        db.session.add(role)  
        db.session.commit()   
        return role           

    # Actualizar un rol existente en la base de datos
    def update(self, role: Role, id: int) -> Optional[Role]:
        entity = self.find(id)  
        if entity is None:
            return None         
        entity.nombre = role.nombre  
        db.session.commit()          
        return entity                

    # Eliminar un rol de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  
        if entity:
            db.session.delete(entity)  
            db.session.commit()        

    # Obtener todos los roles de la base de datos
    def all(self) -> List[Role]:
        return db.session.query(Role).all()  

    # Buscar un rol por ID
    def find(self, id: int) -> Optional[Role]:
        return db.session.query(Role).filter(Role.id_rol == id).one_or_none()  
        
