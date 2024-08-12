from typing import List, Optional
from app.models.supplier import Supplier
from app import db

class SupplierRepository:
    # Guardar un nuevo proveedor en la base de datos
    def save(self, supplier: Supplier) -> Supplier:
        db.session.add(supplier)
        db.session.commit()
        return supplier

    # Actualizar un proveedor existente en la base de datos
    def update(self, supplier: Supplier, id: int) -> Optional[Supplier]:
        entity = self.find(id)
        if entity is None:
            return None
        entity.nombre = supplier.nombre
        entity.contacto = supplier.contacto
        db.session.commit()
        return entity

    # Eliminar un proveedor de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)
        if entity:
            db.session.delete(entity)
            db.session.commit()

    # Obtener todos los proveedores de la base de datos
    def all(self) -> List[Supplier]:
        return db.session.query(Supplier).all()

    # Buscar un proveedor por ID
    def find(self, id: int) -> Optional[Supplier]:
        return db.session.query(Supplier).filter(Supplier.id_proveedor == id).one_or_none()
