from typing import Any

from src.models.product import Image, Product, Variant

from .base import BaseProductTransformer


class OdooPublicTransformer(BaseProductTransformer):
    """Transforms public Odoo products into normalized Product models."""

    def transform(self, product: dict[str, Any]) -> Product:
        images = [
            Image(
                src=image,
                position=index + 1,
            )
            for index, image in enumerate(product.get("images", []))
        ]

        return Product(
            id=str(product.get("id", "")),
            handle=product.get("slug", ""),
            title=product.get("title", ""),
            description=product.get("description", ""),
            vendor=product.get("vendor", ""),
            product_type=product.get("category", ""),
            tags=", ".join(product.get("tags", [])),
            published=True,
            option_names=product.get("option_names", []),
            images=images,
            variants=self.transform_variants(product),
        )

    def transform_variants(
        self,
        product: dict[str, Any],
    ) -> list[Variant]:
        variants = product.get("variants", [])

        if not variants:
            return [
                Variant(
                    price=product.get("price", ""),
                )
            ]

        return [
            self.transform_variant(variant)
            for variant in variants
        ]

    @staticmethod
    def transform_variant(
        variant: dict[str, Any],
    ) -> Variant:
        options = list(variant.get("options", []))
        options.extend(["", "", ""])

        return Variant(
            sku=variant.get("sku", ""),
            option1=options[0],
            option2=options[1],
            option3=options[2],
            price=variant.get("price", ""),
            compare_at_price=variant.get(
                "compare_at_price",
                "",
            ),
            grams=variant.get("grams", 0),
            weight_unit=variant.get("weight_unit", ""),
            inventory_quantity=variant.get(
                "inventory_quantity",
                0,
            ),
            inventory_tracker=variant.get(
                "inventory_tracker",
                "",
            ),
            inventory_policy=variant.get(
                "inventory_policy",
                "deny",
            ),
            fulfillment_service=variant.get(
                "fulfillment_service",
                "manual",
            ),
            barcode=variant.get("barcode", ""),
            taxable=variant.get("taxable", True),
            requires_shipping=variant.get(
                "requires_shipping",
                True,
            ),
        )