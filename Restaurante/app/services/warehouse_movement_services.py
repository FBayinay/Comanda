from typing import List, Optional
from datetime import datetime
from app.models import WarehouseMovement
from app.repositories import WarehouseMovementRepository

repository = WarehouseMovementRepository()

class MovementService:
    """
    MovementService class
    """
    def __init__(self):
        pass

    def create_movement(self, id_usuario: int, id_producto: int, 
                        cantidad: int, fecha: Optional[datetime] = None) -> WarehouseMovement:
        """
        Create a new warehouse movement entry
        :param id_usuario: int
        :param id_producto: int
        :param cantidad: int
        :param fecha: Optional[datetime]
        :return: WarehouseMovement
        """
        movement = WarehouseMovement(
            id_usuario=id_usuario,
            id_producto=id_producto,
            cantidad=cantidad,
            fecha=fecha
        )
        return repository.save(movement)

    def get_all_movements(self) -> List[WarehouseMovement]:
        """
        Get all warehouse movement entries
        :return: List[WarehouseMovement]
        """
        return repository.all()

    def get_movement_by_id(self, id: int) -> Optional[WarehouseMovement]:
        """
        Get a warehouse movement entry by its ID
        :param id: int
        :return: Optional[WarehouseMovement]
        """
        return repository.find(id)

    def update_movement(self, id: int, id_usuario: Optional[int] = None, 
                        id_producto: Optional[int] = None, cantidad: Optional[int] = None, 
                        fecha: Optional[datetime] = None) -> Optional[WarehouseMovement]:
        """
        Update an existing warehouse movement entry
        :param id: int
        :param id_usuario: Optional[int]
        :param id_producto: Optional[int]
        :param cantidad: Optional[int]
        :param fecha: Optional[datetime]
        :return: Optional[WarehouseMovement]
        """
        movement = self.get_movement_by_id(id)
        if movement:
            if id_usuario is not None:
                movement.id_usuario = id_usuario
            if id_producto is not None:
                movement.id_producto = id_producto
            if cantidad is not None:
                movement.cantidad = cantidad
            if fecha is not None:
                movement.fecha = fecha
            return repository.update(movement, id)
        return None

    def delete_movement(self, id: int) -> None:
        """
        Delete a warehouse movement entry by its ID
        :param id: int
        """
        repository.delete(id)
