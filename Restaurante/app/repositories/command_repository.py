from typing import List, Optional
from app.models import Command  
from app import db

class CommandRepository:
    # Guardar un nuevo comando en la base de datos
    def save(self, command: Command) -> Command:
        db.session.add(command)  
        db.session.commit()    
        return command         

    # Actualizar un comando existente en la base de datos
    def update(self, command: Command, id: int) -> Optional[Command]:
        entity = self.find(id)  
        if entity is None:
            return None         
        entity.id_mesa = command.id_mesa
        entity.id_usuario = command.id_usuario
        entity.fecha_inicio = command.fecha_inicio
        entity.fecha_fin = command.fecha_fin
        entity.estado = command.estado
        db.session.commit()   
        return entity         

    # Eliminar un comando de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)  
        if entity:
            db.session.delete(entity)  
            db.session.commit()        

    # Obtener todos los comandos de la base de datos
    def all(self) -> List[Command]:
        return db.session.query(Command).all()  

    # Buscar un comando por ID
    def find(self, id: int) -> Optional[Command]:
        return db.session.query(Command).filter(Command.id_comanda == id).one_or_none()  
        
