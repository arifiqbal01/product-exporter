from __future__ import annotations

from typing import Any

import requests

from src.configs import WixConfig
from src.exporters.base import BaseExporter
from src.exporters.queries.wix import (
    GET_FILTERED_PRODUCTS,
    GET_PRODUCT_BY_SLUG,
)


class WixB2BExporter(BaseExporter):
    """Extract raw products from a Wix B2B storefront."""

    def __init__(self, config: WixConfig):
        self.config = config

        self.url = (
            f"{config.store_url.rstrip('/')}"
            "/_api/wix-ecommerce-storefront-web/api"
        )

        self.session = requests.Session()

        headers = {
            "authorization": config.authorization,
            "x-xsrf-token": config.xsrf_token,
            "content-type": "application/json; charset=utf-8",
        }

        if config.linguist:
            headers["x-wix-linguist"] = config.linguist

        self.session.headers.update(headers)

    def fetch_page(self, page: int) -> list[dict[str, Any]]:
        """Fetch one page of raw Wix products."""

        offset = (page - 1) * self.config.limit

        response = self.session.post(
            self.url,
            json=self._build_payload(offset),
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()

        products = (
            data["data"]["catalog"]["category"]
            ["productsWithMetaData"]["list"]
        )

        enriched = []

        for product in products:
            try:
                detail = self._fetch_product_details(
                    product["urlPart"],
                )
                product.update(detail)

            except Exception as exc:
                print(
                    f"Failed to fetch details for "
                    f"{product['urlPart']}: {exc}"
                )

            enriched.append(product)

        return enriched

    def _fetch_product_details(
        self,
        slug: str,
    ) -> dict[str, Any]:
        """Fetch the complete product by slug."""

        response = self.session.post(
            self.url,
            json=self._build_detail_payload(slug),
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        return data["data"]["catalog"]["product"]

    def _build_payload(
        self,
        offset: int,
    ) -> dict[str, Any]:
        return {
            "operationName": "getFilteredProducts",
            "source": "WixStoresWebClient",
            "query": GET_FILTERED_PRODUCTS,
            "variables": {
                "mainCollectionId": self.config.collection_id,
                "offset": offset,
                "limit": self.config.limit,
                "sort": None,
                "filters": {
                    "and": [
                        {
                            "term": {
                                "field": "comparePrice",
                                "op": "GTE",
                                "values": ["1"],
                            }
                        }
                    ]
                },
                "withPriceRange": True,
            },
        }

    def _build_detail_payload(
        self,
        slug: str,
    ) -> dict[str, Any]:
        return {
            "operationName": "getProductBySlug",
            "source": "WixStoresWebClient",
            "query": GET_PRODUCT_BY_SLUG,
            "variables": {
                "externalId": "",
                "slug": slug,
                "withPriceRange": True,
            },
        }