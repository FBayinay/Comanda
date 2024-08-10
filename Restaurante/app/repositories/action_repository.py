from typing import List, Optional
from app.models import Action
from app import db

class ActionRepository:
    # Guardar un nueva acción en la base de datos
    def save(self, action: Action) -> Action:
        db.session.add(action)  # Añadir el objeto action a la sesión de base de datos
        db.session.commit()   # Confirmar (commit) la transacción para guardar los cambios
        return action           # Retornar el objeto action guardado

    # Actualizar una acción existente en la base de datos
    def update(self, action: Action, id: int) -> Optional[Action]:
        entity = self.find(id)  # Buscar la acción existente por ID
        if entity is None:
            return None         # Si no se encuentra la acción, retornar None
        entity.nombre = action.nombre  # Actualizar el nombre del la acción
        db.session.commit()          # Confirmar los cambios
        return entity                # Retornar la acción actualizado

    # Eliminar una acción de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  # Buscar la acción existente por ID
        if entity:
            db.session.delete(entity)  # Eliminar la acción de la sesión de base de datos
            db.session.commit()        # Confirmar la transacción

    # Obtener todos los actions de la base de datos
    def all(self) -> List[Action]:
        return db.session.query(Action).all()  # Obtener y retornar todos los actions

    # Buscar una acción por ID
    def find(self, id: int) -> Optional[Action]:
        return db.session.query(Action).filter(Action.id_accion == id).one_or_none()  
        # Buscar la acción por ID y retornar una o ninguna (si no se encuentra)
