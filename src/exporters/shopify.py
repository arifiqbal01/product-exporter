from typing import Any

import requests

from src.configs import ShopifyConfig
from src.exporters.base import BaseExporter


class ShopifyExporter(BaseExporter):
    """Fetches raw product data from a public Shopify store."""

    def __init__(self, config: ShopifyConfig):
        self.config = config

    def fetch_page(self, page: int) -> list[dict[str, Any]]:
        url = (
            f"{self.config.store_url.rstrip('/')}/products.json"
            f"?limit={self.config.limit}&page={page}"
        )

        print(f"Fetching page {page}")

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        products = response.json().get("products", [])

        print(f"Fetched {len(products)} products")

        return products