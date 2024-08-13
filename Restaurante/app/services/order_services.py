from typing import List, Optional
from datetime import datetime
from app.models import Order
from app.repositories import OrderRepository

repository = OrderRepository()

class OrderService:
    """
    OrderService class
    """
    def __init__(self):
        pass

    def create_order(self, id_usuario: int, id_producto: int, id_proveedor: int, 
                     cantidad: int, precio_unitario: float, precio_total: float) -> Order:
        """
        Create a new order entry
        :param id_usuario: int
        :param id_producto: int
        :param id_proveedor: int
        :param cantidad: int
        :param precio_unitario: float
        :param precio_total: float
        :return: Order
        """
        order = Order(
            id_usuario=id_usuario,
            id_producto=id_producto,
            id_proveedor=id_proveedor,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            precio_total=precio_total
        )
        return repository.save(order)

    def get_all_orders(self) -> List[Order]:
        """
        Get all order entries
        :return: List[Order]
        """
        return repository.all()

    def get_order_by_id(self, id: int) -> Optional[Order]:
        """
        Get an order entry by its ID
        :param id: int
        :return: Optional[Order]
        """
        return repository.find(id)

    def update_order(self, id: int, id_usuario: Optional[int] = None, 
                     id_producto: Optional[int] = None, id_proveedor: Optional[int] = None,
                     cantidad: Optional[int] = None, precio_unitario: Optional[float] = None, 
                     precio_total: Optional[float] = None, fecha: Optional[datetime] = None) -> Optional[Order]:
        """
        Update an existing order entry
        :param id: int
        :param id_usuario: Optional[int]
        :param id_producto: Optional[int]
        :param id_proveedor: Optional[int]
        :param cantidad: Optional[int]
        :param precio_unitario: Optional[float]
        :param precio_total: Optional[float]
        :param fecha: Optional[datetime]
        :return: Optional[Order]
        """
        order = self.get_order_by_id(id)
        if order:
            if id_usuario is not None:
                order.id_usuario = id_usuario
            if id_producto is not None:
                order.id_producto = id_producto
            if id_proveedor is not None:
                order.id_proveedor = id_proveedor
            if cantidad is not None:
                order.cantidad = cantidad
            if precio_unitario is not None:
                order.precio_unitario = precio_unitario
            if precio_total is not None:
                order.precio_total = precio_total
            if fecha is not None:
                order.fecha = fecha
            return repository.update(order, id)
        return None

    def delete_order(self, id: int) -> None:
        """
        Delete an order entry by its ID
        :param id: int
        """
        repository.delete(id)
