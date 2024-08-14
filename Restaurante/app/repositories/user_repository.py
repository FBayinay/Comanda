from typing import List, Optional
from app.models import User, Role, Action
from app import db

class UserRepository:
    # Guardar un nuevo usuario en la base de datos
    def save(self, user: User) -> Optional[User]:
        if not self._role_exists(user.rol_id) or not self._action_exists(user.id_accion):
            return None  
        
        db.session.add(user)  
        db.session.commit()   
        return user           

    # Actualizar un usuario existente en la base de datos
    def update(self, user: User, id: int) -> Optional[User]:
        entity = self.find(id) 
        if entity is None:
            return None  
        
        if not self._role_exists(user.rol_id) or not self._action_exists(user.id_accion):
            return None  
        
        entity.nombre = user.nombre
        entity.apellido = user.apellido
        entity.dni = user.dni
        entity.email = user.email
        entity.calle = user.calle
        entity.numero = user.numero
        entity.rol_id = user.rol_id
        entity.id_accion = user.id_accion
        db.session.commit()     
        return entity           

    # Eliminar un usuario de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  
        if entity:
            db.session.delete(entity)  
            db.session.commit()        

    # Obtener todos los usuarios de la base de datos
    def all(self) -> List[User]:
        return db.session.query(User).all()  

    # Buscar un usuario por ID
    def find(self, id: int) -> Optional[User]:
        return db.session.query(User).filter(User.id_usuario == id).one_or_none()  
        

    # Verificar si un rol existe
    def _role_exists(self, rol_id: int) -> bool:
        return db.session.query(Role).filter(Role.id_rol == rol_id).scalar() is not None

    # Verificar si una acción existe
    def _action_exists(self, id_accion: int) -> bool:
        return db.session.query(Action).filter(Action.id_accion == id_accion).scalar() is not None
    # Verificar si el email ya existe
    def email_exists(self, email: str) -> bool:
        return db.session.query(User).filter(User.email == email).scalar() is not None

    # Verificar si el DNI ya existe
    def dni_exists(self, dni: str) -> bool:
        return db.session.query(User).filter(User.dni == dni).scalar() is not None