from typing import List, Optional
from app.models import WarehouseMovement 
from app import db

class WarehouseMovementRepository:
    # Guardar un nuevo movimiento de almacén en la base de datos
    def save(self, movement: WarehouseMovement) -> WarehouseMovement:
        db.session.add(movement)  
        db.session.commit()       
        return movement           

    # Actualizar un movimiento de almacén existente en la base de datos
    def update(self, movement: WarehouseMovement, id: int) -> Optional[WarehouseMovement]:
        entity = self.find(id)  
        if entity is None:
            return None         
        entity.id_usuario = movement.id_usuario
        entity.id_producto = movement.id_producto
        entity.cantidad = movement.cantidad
        entity.fecha = movement.fecha
        db.session.commit()   
        return entity         

    # Eliminar un movimiento de almacén de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  
        if entity:
            db.session.delete(entity)  
            db.session.commit()        

    # Obtener todos los movimientos de almacén de la base de datos
    def all(self) -> List[WarehouseMovement]:
        return db.session.query(WarehouseMovement).all()  

    # Buscar un movimiento de almacén por ID
    def find(self, id: int) -> Optional[WarehouseMovement]:
        return db.session.query(WarehouseMovement).filter(WarehouseMovement.id_movimiento == id).one_or_none()  
        
