from typing import List, Optional
from app.models import Stock
from app.repositories import StockRepository

repository = StockRepository()

class StockService:
    """
    StockService class
    """
    def __init__(self):
        pass

    def create_stock(self, id_producto: int, cantidad: int) -> Stock:
        """
        Create a new stock entry
        :param id_producto: int
        :param cantidad: int
        :return: Stock
        :raises ValueError: If the product does not exist
        """
        # Verificar si el producto existe antes de crear el stock
        if not repository._product_exists(id_producto):
            raise ValueError("El producto no existe en la base de datos")
        
        stock = Stock(id_producto=id_producto, cantidad=cantidad)
        return repository.save(stock)

    def get_all_stocks(self) -> List[Stock]:
        """
        Get all stock entries
        :return: List[Stock]
        """
        return repository.all()

    def get_stock_by_id(self, id: int) -> Optional[Stock]:
        """
        Get a stock entry by its ID
        :param id: int
        :return: Optional[Stock]
        """
        return repository.find(id)

    def update_stock(self, id: int, id_producto: Optional[int] = None, cantidad: Optional[int] = None) -> Optional[Stock]:
        """
        Update an existing stock entry
        :param id: int
        :param id_producto: Optional[int]
        :param cantidad: Optional[int]
        :return: Optional[Stock]
        :raises ValueError: If the product does not exist
        """
        stock = self.get_stock_by_id(id)
        if stock:
            if id_producto is not None:
                if not repository._product_exists(id_producto):
                    raise ValueError("El producto no existe en la base de datos")
                stock.id_producto = id_producto
            if cantidad is not None:
                stock.cantidad = cantidad
            return repository.update(stock, id)
        return None

    def delete_stock(self, id: int) -> None:
        """
        Delete a stock entry by its ID
        :param id: int
        """
        repository.delete(id)
