from typing import List, Optional
from app.models import Order  
from app import db

class OrderRepository:
    # Guardar un nuevo pedido en la base de datos
    def save(self, order: Order) -> Order:
        db.session.add(order)  
        db.session.commit()    
        return order           

    # Actualizar un pedido existente en la base de datos
    def update(self, order: Order, id: int) -> Optional[Order]:
        entity = self.find(id)  
        if entity is None:
            return None         
        entity.id_usuario = order.id_usuario
        entity.id_producto = order.id_producto
        entity.id_proveedor = order.id_proveedor
        entity.cantidad = order.cantidad
        entity.precio_unitario = order.precio_unitario
        entity.precio_total = order.precio_total
        entity.fecha = order.fecha
        db.session.commit()   
        return entity         

    # Eliminar un pedido de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  
        if entity:
            db.session.delete(entity)  
            db.session.commit()        

    # Obtener todos los pedidos de la base de datos
    def all(self) -> List[Order]:
        return db.session.query(Order).all()  

    # Buscar un pedido por ID
    def find(self, id: int) -> Optional[Order]:
        return db.session.query(Order).filter(Order.id_pedido == id).one_or_none()  
        
