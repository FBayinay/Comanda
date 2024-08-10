from typing import List, Optional
from app.models import Role
from app import db

class RoleRepository:
    # Guardar un nuevo rol en la base de datos
    def save(self, role: Role) -> Role:
        db.session.add(role)  # Añadir el objeto Role a la sesión de base de datos
        db.session.commit()   # Confirmar (commit) la transacción para guardar los cambios
        return role           # Retornar el objeto Role guardado

    # Actualizar un rol existente en la base de datos
    def update(self, role: Role, id: int) -> Optional[Role]:
        entity = self.find(id)  # Buscar el rol existente por ID
        if entity is None:
            return None         # Si no se encuentra el rol, retornar None
        entity.nombre = role.nombre  # Actualizar el nombre del rol
        db.session.commit()          # Confirmar los cambios
        return entity                # Retornar el rol actualizado

    # Eliminar un rol de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  # Buscar el rol existente por ID
        if entity:
            db.session.delete(entity)  # Eliminar el rol de la sesión de base de datos
            db.session.commit()        # Confirmar la transacción

    # Obtener todos los roles de la base de datos
    def all(self) -> List[Role]:
        return db.session.query(Role).all()  # Obtener y retornar todos los roles

    # Buscar un rol por ID
    def find(self, id: int) -> Optional[Role]:
        return db.session.query(Role).filter(Role.id_rol == id).one_or_none()  
        # Buscar el rol por ID y retornar uno o ninguno (si no se encuentra)
