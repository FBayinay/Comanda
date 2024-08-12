from typing import List, Optional
from app.models.product import Product
from app import db

class ProductRepository:
    # Guardar un nuevo producto en la base de datos
    def save(self, product: Product) -> Product:
        db.session.add(product)
        db.session.commit()
        return product

    # Actualizar un producto existente en la base de datos
    def update(self, product: Product, id: int) -> Optional[Product]:
        entity = self.find(id)
        if entity is None:
            return None
        entity.nombre = product.nombre
        db.session.commit()
        return entity

    # Eliminar un producto de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)
        if entity:
            db.session.delete(entity)
            db.session.commit()

    # Obtener todos los productos de la base de datos
    def all(self) -> List[Product]:
        return db.session.query(Product).all()

    # Buscar un producto por ID
    def find(self, id: int) -> Optional[Product]:
        return db.session.query(Product).filter(Product.id_producto == id).one_or_none()
