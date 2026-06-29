from __future__ import annotations

from src.models.product import Image, Product, Variant

from .base import BaseProductTransformer


class WixProductTransformer(BaseProductTransformer):
    """Transform raw Wix GraphQL products into normalized Product models."""

    def transform(self, raw_product: dict) -> Product:
        product = Product(
            id=raw_product["id"],
            handle=raw_product.get("urlPart", ""),
            title=raw_product.get("name", ""),
            description="",
            vendor="",
            product_type=raw_product.get("productType", ""),
            tags=raw_product.get("ribbon") or "",
            published=True,
        )

        # Images
        for index, media in enumerate(raw_product.get("media", []), start=1):
            image_url = media.get("fullUrl") or media.get("url")

            if image_url:
                product.images.append(
                    Image(
                        src=image_url,
                        position=index,
                    )
                )

        # Wix B2B exposes a single product variant.
        inventory = raw_product.get("inventory") or {}

        product.variants.append(
            Variant(
                sku=raw_product.get("sku", ""),
                price=str(raw_product.get("price") or ""),
                compare_at_price=str(raw_product.get("comparePrice") or ""),
                inventory_quantity=inventory.get("quantity") or 0,
                inventory_tracker="shopify",
                inventory_policy="deny",
                fulfillment_service="manual",
                taxable=True,
                requires_shipping=True,
            )
        )

        return product