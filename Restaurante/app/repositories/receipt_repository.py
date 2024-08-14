from typing import List, Optional
from app.models import Receipt  
from app import db

class ReceiptRepository:
    # Guardar un nuevo recibo en la base de datos
    def save(self, receipt: Receipt) -> Receipt:
        db.session.add(receipt)  
        db.session.commit()    
        return receipt  

    # Actualizar un recibo existente en la base de datos
    def update(self, receipt: Receipt, id: int) -> Optional[Receipt]:
        entity = self.find(id)  
        if entity is None:
            return None         
        entity.id_comanda = receipt.id_comanda
        entity.fecha = receipt.fecha
        entity.total = receipt.total
        entity.estado_pago = receipt.estado_pago
        entity.detalles_comanda = receipt.detalles_comanda
        db.session.commit()   
        return entity         

    # Eliminar un recibo de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  
        if entity:
            db.session.delete(entity)  
            db.session.commit()        

    # Obtener todos los recibos de la base de datos
    def all(self) -> List[Receipt]:
        return db.session.query(Receipt).all()  # Obtener y retornar todos los recibos

    # Buscar un recibo por ID
    def find(self, id: int) -> Optional[Receipt]:
        return db.session.query(Receipt).filter(Receipt.id_recibo == id).one_or_none()  
        
