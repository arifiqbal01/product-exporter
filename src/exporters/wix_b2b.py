from __future__ import annotations

from typing import Any

import requests

from src.configs import WixConfig

from .base import BaseExporter


class WixB2BExporter(BaseExporter):
    """Extract raw products from a Wix B2B storefront."""

    GRAPHQL_QUERY = """
    query getFilteredProducts(
      $mainCollectionId: String!,
      $filters: ProductFilters,
      $sort: ProductSort,
      $offset: Int,
      $limit: Int,
      $withPriceRange: Boolean = false
    ) {
      catalog {
        category(categoryId: $mainCollectionId) {
          productsWithMetaData(
            filters: $filters,
            limit: $limit,
            sort: $sort,
            offset: $offset,
            onlyVisible: true
          ) {
            totalCount

            list {
              id
              name
              sku

              price
              formattedPrice

              comparePrice
              formattedComparePrice

              isInStock
              urlPart
              ribbon
              productType
              currency

              media {
                url
                fullUrl
                width
                height
                altText
              }

              inventory {
                status
                quantity
              }

              priceRange(withSubscriptionPriceRange: true)
                @include(if: $withPriceRange) {
                fromPrice
                fromPriceFormatted
              }
            }
          }
        }
      }
    }
    """

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

        payload = {
            "operationName": "getFilteredProducts",
            "source": "WixStoresWebClient",
            "query": self.GRAPHQL_QUERY,
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

        response = self.session.post(self.url, json=payload)
        response.raise_for_status()

        data = response.json()

        return (
            data["data"]["catalog"]["category"]["productsWithMetaData"]["list"]
        )