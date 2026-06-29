from typing import Any

import requests

from src.exporters.base import BaseExporter


class ShopifyExporter(BaseExporter):
    """Fetches raw product data from a public Shopify store."""

    def __init__(
        self,
        store_url: str,
        limit: int = 250,
    ):
        self.store_url = store_url.rstrip("/")
        self.limit = limit

    def fetch_page(self, page: int) -> list[dict[str, Any]]:
        url = (
            f"{self.store_url}/products.json"
            f"?limit={self.limit}&page={page}"
        )

        print(f"Fetching page {page}")

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        products = response.json().get("products", [])

        print(f"Fetched {len(products)} products")

        return products