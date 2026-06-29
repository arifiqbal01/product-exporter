from abc import ABC, abstractmethod
from typing import Any


class BaseExporter(ABC):
    """Base class for all e-commerce exporters."""

    @abstractmethod
    def fetch_page(self, page: int) -> list[dict[str, Any]]:
        """
        Fetch a single page of raw products.

        Returns an empty list when there are no more products.
        """
        raise NotImplementedError