from typing import List, Optional
from app.models import User, Role, Action
from app import db

class UserRepository:
    # Guardar un nuevo usuario en la base de datos
    def save(self, user: User) -> Optional[User]:
        if not self._role_exists(user.rol_id) or not self._action_exists(user.id_accion):
            return None  # Retornar None si el rol o acción no existe
        
        db.session.add(user)  # Añadir el objeto User a la sesión de base de datos
        db.session.commit()   # Confirmar (commit) la transacción para guardar los cambios
        return user           # Retornar el objeto User guardado

    # Actualizar un usuario existente en la base de datos
    def update(self, user: User, id: int) -> Optional[User]:
        entity = self.find(id)  # Buscar el usuario existente por ID
        if entity is None:
            return None  # Si no se encuentra el usuario, retornar None
        
        if not self._role_exists(user.rol_id) or not self._action_exists(user.id_accion):
            return None  # Retornar None si el rol o acción no existe
        
        entity.nombre = user.nombre
        entity.apellido = user.apellido
        entity.dni = user.dni
        entity.email = user.email
        entity.calle = user.calle
        entity.numero = user.numero
        entity.rol_id = user.rol_id
        entity.id_accion = user.id_accion
        db.session.commit()     # Confirmar los cambios
        return entity           # Retornar el usuario actualizado

    # Eliminar un usuario de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  # Buscar el usuario existente por ID
        if entity:
            db.session.delete(entity)  # Eliminar el usuario de la sesión de base de datos
            db.session.commit()        # Confirmar la transacción

    # Obtener todos los usuarios de la base de datos
    def all(self) -> List[User]:
        return db.session.query(User).all()  # Obtener y retornar todos los usuarios

    # Buscar un usuario por ID
    def find(self, id: int) -> Optional[User]:
        return db.session.query(User).filter(User.id_usuario == id).one_or_none()  
        # Buscar el usuario por ID y retornar uno o ninguno (si no se encuentra)

    # Verificar si un rol existe
    def _role_exists(self, rol_id: int) -> bool:
        return db.session.query(Role).filter(Role.id_rol == rol_id).scalar() is not None

    # Verificar si una acción existe
    def _action_exists(self, id_accion: int) -> bool:
        return db.session.query(Action).filter(Action.id_accion == id_accion).scalar() is not None
