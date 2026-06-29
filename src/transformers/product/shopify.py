from typing import Any

from src.models.product import Product, Variant, Image


class ShopifyTransformer:
    """Transforms raw Shopify products into normalized Product models."""

    @staticmethod
    def transform(products: list[dict[str, Any]]) -> list[Product]:
        return [ShopifyTransformer.transform_product(product) for product in products]

    @staticmethod
    def transform_product(product: dict[str, Any]) -> Product:
        options = product.get("options", [])

        images = [
            Image(
                src=image.get("src", ""),
                position=index + 1,
            )
            for index, image in enumerate(product.get("images", []))
        ]

        variants = [
            ShopifyTransformer.transform_variant(variant)
            for variant in product.get("variants", [])
        ]

        return Product(
            id=str(product.get("id", "")),
            handle=product.get("handle", ""),
            title=product.get("title", ""),
            description=product.get("body_html", ""),
            vendor=product.get("vendor", ""),
            product_type=product.get("product_type", ""),
            tags=product.get("tags", ""),
            published=bool(product.get("published_at")),
            option_names=[
                option.get("name", "")
                for option in options
            ],
            images=images,
            variants=variants,
        )

    @staticmethod
    def transform_variant(variant: dict[str, Any]) -> Variant:
        return Variant(
            sku=variant.get("sku", ""),
            option1=variant.get("option1", ""),
            option2=variant.get("option2", ""),
            option3=variant.get("option3", ""),
            price=str(variant.get("price", "")),
            compare_at_price=str(
                variant.get("compare_at_price") or ""
            ),
            grams=variant.get("grams", 0),
            weight_unit=variant.get("weight_unit", ""),
            inventory_quantity=variant.get(
                "inventory_quantity", 0
            ),
            inventory_tracker=variant.get(
                "inventory_management", ""
            ),
            inventory_policy=variant.get(
                "inventory_policy", "deny"
            ),
            fulfillment_service=variant.get(
                "fulfillment_service", "manual"
            ),
            barcode=variant.get("barcode", ""),
            taxable=bool(variant.get("taxable", True)),
            requires_shipping=bool(
                variant.get("requires_shipping", True)
            ),
        )