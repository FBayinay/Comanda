from typing import List, Optional
from app.models import WarehouseMovement  # Importar desde movement/models
from app import db

class WarehouseMovementRepository:
    # Guardar un nuevo movimiento de almacén en la base de datos
    def save(self, movement: WarehouseMovement) -> WarehouseMovement:
        db.session.add(movement)  # Añadir el objeto WarehouseMovement a la sesión de base de datos
        db.session.commit()       # Confirmar (commit) la transacción para guardar los cambios
        return movement           # Retornar el objeto WarehouseMovement guardado

    # Actualizar un movimiento de almacén existente en la base de datos
    def update(self, movement: WarehouseMovement, id: int) -> Optional[WarehouseMovement]:
        entity = self.find(id)  # Buscar el movimiento existente por ID
        if entity is None:
            return None         # Si no se encuentra el movimiento, retornar None
        entity.id_usuario = movement.id_usuario
        entity.id_producto = movement.id_producto
        entity.cantidad = movement.cantidad
        entity.fecha = movement.fecha
        db.session.commit()   # Confirmar los cambios
        return entity         # Retornar el movimiento actualizado

    # Eliminar un movimiento de almacén de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  # Buscar el movimiento existente por ID
        if entity:
            db.session.delete(entity)  # Eliminar el movimiento de la sesión de base de datos
            db.session.commit()        # Confirmar la transacción

    # Obtener todos los movimientos de almacén de la base de datos
    def all(self) -> List[WarehouseMovement]:
        return db.session.query(WarehouseMovement).all()  # Obtener y retornar todos los movimientos

    # Buscar un movimiento de almacén por ID
    def find(self, id: int) -> Optional[WarehouseMovement]:
        return db.session.query(WarehouseMovement).filter(WarehouseMovement.id_movimiento == id).one_or_none()  
        # Buscar el movimiento por ID y retornar uno o ninguno (si no se encuentra)
