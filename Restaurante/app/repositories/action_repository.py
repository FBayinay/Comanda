from typing import List, Optional
from app.models import action
from app import db

class ActionRepository:
    # Guardar un nuevo rol en la base de datos
    def save(self, action: action) -> action:
        db.session.add(action)  # Añadir el objeto action a la sesión de base de datos
        db.session.commit()   # Confirmar (commit) la transacción para guardar los cambios
        return action           # Retornar el objeto action guardado

    # Actualizar un rol existente en la base de datos
    def update(self, action: action, id: int) -> Optional[action]:
        entity = self.find(id)  # Buscar el rol existente por ID
        if entity is None:
            return None         # Si no se encuentra el rol, retornar None
        entity.nombre = action.nombre  # Actualizar el nombre del rol
        db.session.commit()          # Confirmar los cambios
        return entity                # Retornar el rol actualizado

    # Eliminar un rol de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  # Buscar el rol existente por ID
        if entity:
            db.session.delete(entity)  # Eliminar el rol de la sesión de base de datos
            db.session.commit()        # Confirmar la transacción

    # Obtener todos los actions de la base de datos
    def all(self) -> List[action]:
        return db.session.query(action).all()  # Obtener y retornar todos los actions

    # Buscar un rol por ID
    def find(self, id: int) -> Optional[action]:
        return db.session.query(action).filter(action.id_accion == id).one_or_none()  
        # Buscar el rol por ID y retornar uno o ninguno (si no se encuentra)
