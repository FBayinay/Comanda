from typing import List, Optional
from app.models.stock import Stock
from app.models.product import Product
from app import db

class StockRepository:
    # Guardar un nuevo stock en la base de datos
    def save(self, stock: Stock) -> Stock:
        # Verificar si el producto existe
        if not self._product_exists(stock.id_producto):
            raise ValueError("El producto no existe en la base de datos")
        
        db.session.add(stock)
        db.session.commit()
        return stock

    # Actualizar un stock existente en la base de datos
    def update(self, stock: Stock, id: int) -> Optional[Stock]:
        entity = self.find(id)
        if entity is None:
            return None
        if not self._product_exists(stock.id_producto):
            raise ValueError("El producto no existe en la base de datos")
        
        entity.id_producto = stock.id_producto
        entity.cantidad = stock.cantidad
        db.session.commit()
        return entity

    # Eliminar un stock de la base de datos
    def delete(self, id: int) -> None:
        entity = self.find(id)
        if entity:
            db.session.delete(entity)
            db.session.commit()

    # Obtener todos los stocks de la base de datos
    def all(self) -> List[Stock]:
        return db.session.query(Stock).all()

    # Buscar un stock por ID
    def find(self, id: int) -> Optional[Stock]:
        return db.session.query(Stock).filter(Stock.id_stock == id).one_or_none()

    # Verificar si un producto existe
    def _product_exists(self, id_producto: int) -> bool:
        return db.session.query(Product).filter(Product.id_producto == id_producto).scalar() is not None
