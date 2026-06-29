# transformers/product/base.py

from abc import ABC, abstractmethod
from src.models.product import Product


class BaseProductTransformer(ABC):

    @abstractmethod
    def transform(self, raw_product: dict) -> Product:
        ...

    def transform_many(self, raw_products: list[dict]) -> list[Product]:
        return [self.transform(product) for product in raw_products]