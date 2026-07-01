from typing import Any

import requests

from src.configs.woocommerce import WooCommerceConfig
from src.exporters.base import BaseExporter


class WooCommerceExporter(BaseExporter):
    """Fetches raw product data from a WooCommerce Store API."""

    def __init__(self, config: WooCommerceConfig):
        self.config = config
        self.session = requests.Session()

    def fetch_page(self, page: int) -> list[dict[str, Any]]:
        print(f"Fetching page {page}")

        summaries = self.fetch_product_list(page)

        if not summaries:
            print("Fetched 0 products")
            return []

        products = [
            self.enrich_product(
                self.fetch_product(summary["id"])
            )
            for summary in summaries
        ]

        print(f"Fetched {len(products)} products")

        return products

    def fetch_product_list(
        self,
        page: int,
    ) -> list[dict[str, Any]]:
        url = (
            f"{self.config.store_url.rstrip('/')}"
            "/wp-json/wc/store/v1/products"
        )

        response = self.session.get(
            url,
            params={
                "page": page,
                "per_page": self.config.limit,
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def fetch_product(
        self,
        product_id: int,
    ) -> dict[str, Any]:
        url = (
            f"{self.config.store_url.rstrip('/')}"
            f"/wp-json/wc/store/v1/products/{product_id}"
        )

        response = self.session.get(
            url,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def enrich_product(
            self,
            product: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Enrich a product with complete variation data.

        The Store API returns lightweight variation references.
        Replace them with complete variation objects while
        preserving their selected attributes.
        """

        if product.get("type") != "variable":
            return product

        variations = []

        for summary in product.get("variations", []):
            detail = self.fetch_product(summary["id"])
            detail["attributes"] = summary.get("attributes", [])
            detail.setdefault(
                "is_in_stock",
                product.get("is_in_stock", True),
            )
            variations.append(detail)

        product["variations"] = variations

        return product