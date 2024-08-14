from typing import List, Optional
from app.models import CommandDetail  
from app import db

class CommandDetailRepository:
    # Guardar un nuevo detalle de comando en la base de datos
    def save(self, command_detail: CommandDetail) -> CommandDetail:
        db.session.add(command_detail)  
        db.session.commit()    
        return command_detail  

    # Actualizar un detalle de comando existente en la base de datos
    def update(self, command_detail: CommandDetail, id: int) -> Optional[CommandDetail]:
        entity = self.find(id)  
        if entity is None:
            return None         
        entity.id_comanda = command_detail.id_comanda
        entity.id_item_menu = command_detail.id_item_menu
        entity.id_menu = command_detail.id_menu
        entity.cantidad = command_detail.cantidad
        entity.precio_total = command_detail.precio_total
        db.session.commit()   
        return entity         

    # Eliminar un detalle de comando de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  
        if entity:
            db.session.delete(entity)  
            db.session.commit()       

    # Obtener todos los detalles de comando de la base de datos
    def all(self) -> List[CommandDetail]:
        return db.session.query(CommandDetail).all()  

    # Buscar un detalle de comando por ID
    def find(self, id: int) -> Optional[CommandDetail]:
        return db.session.query(CommandDetail).filter(CommandDetail.id_detalles == id).one_or_none()  
        
