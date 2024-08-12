from typing import List, Optional
from app.models import Product
from app.repositories import ProductRepository

repository = ProductRepository()

class ProductService:
    """
    ProductService class
    """
    def __init__(self):
        pass

    def create_product(self, nombre: str) -> Product:
        """
        Create a new product entry
        :param nombre: str
        :return: Product
        """
        product = Product(nombre=nombre)
        return repository.save(product)

    def get_all_products(self) -> List[Product]:
        """
        Get all product entries
        :return: List[Product]
        """
        return repository.all()

    def get_product_by_id(self, id: int) -> Optional[Product]:
        """
        Get a product entry by its ID
        :param id: int
        :return: Optional[Product]
        """
        return repository.find(id)

    def update_product(self, id: int, nombre: Optional[str] = None) -> Optional[Product]:
        """
        Update an existing product entry
        :param id: int
        :param nombre: Optional[str]
        :return: Optional[Product]
        """
        product = self.get_product_by_id(id)
        if product:
            if nombre is not None:
                product.nombre = nombre
            return repository.update(product, id)
        return None

    def delete_product(self, id: int) -> None:
        """
        Delete a product entry by its ID
        :param id: int
        """
        repository.delete(id)
