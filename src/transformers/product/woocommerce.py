from typing import Any

from src.models.product import Image, Product, Variant

from .base import BaseProductTransformer


class WooCommerceTransformer(BaseProductTransformer):
    """Transforms WooCommerce Store API products into normalized Product models."""

    def transform(self, product: dict[str, Any]) -> Product:
        images = [
            Image(
                src=image.get("src", ""),
                position=index + 1,
            )
            for index, image in enumerate(product.get("images", []))
        ]

        return Product(
            id=str(product.get("id", "")),
            handle=product.get("slug", ""),
            title=product.get("name", ""),
            description=product.get("description", ""),
            vendor=self.get_vendor(product),
            product_type=self.get_product_type(product),
            tags=self.get_tags(product),
            published=True,
            option_names=self.get_option_names(product),
            images=images,
            variants=self.transform_variants(product),
        )

    def transform_variants(
        self,
        product: dict[str, Any],
    ) -> list[Variant]:

        if product.get("type") == "simple":
            return [self.transform_variant(product)]

        return [
            self.transform_variant(variation)
            for variation in product.get("variations", [])
        ]

    @staticmethod
    def transform_variant(
        product: dict[str, Any],
    ) -> Variant:

        prices = product.get("prices", {})

        option_values = [
            attr.get("value", "")
            for attr in product.get("attributes", [])
        ]

        option_values.extend(["", "", ""])

        return Variant(
            sku=product.get("sku", ""),
            option1=option_values[0],
            option2=option_values[1],
            option3=option_values[2],
            price=WooCommerceTransformer.normalize_price(
                prices.get("price", ""),
                prices.get("currency_minor_unit", 2),
            ),
            compare_at_price=WooCommerceTransformer.normalize_price(
                prices.get("regular_price", ""),
                prices.get("currency_minor_unit", 2),
            ),
            inventory_quantity=0,
            inventory_tracker="",
            inventory_policy="deny",
            fulfillment_service="manual",
            barcode="",
            taxable=True,
            requires_shipping=True,
            grams=0,
            weight_unit="",
        )

    @staticmethod
    def normalize_price(
        value: str | int,
        decimals: int,
    ) -> str:
        if value in ("", None):
            return ""

        return f"{int(value) / (10 ** decimals):.{decimals}f}"

    @staticmethod
    def get_product_type(product: dict[str, Any]) -> str:
        categories = product.get("categories", [])

        if categories:
            return categories[0].get("name", "")

        return ""

    @staticmethod
    def get_tags(product: dict[str, Any]) -> str:
        return ", ".join(
            tag.get("name", "")
            for tag in product.get("tags", [])
        )

    @staticmethod
    def get_option_names(
        product: dict[str, Any],
    ) -> list[str]:
        return [
            attribute.get("name", "")
            for attribute in product.get("attributes", [])
            if attribute.get("has_variations")
        ]

    @staticmethod
    def get_vendor(product: dict[str, Any]) -> str:
        brands = product.get("brands", [])

        if brands:
            return brands[0].get("name", "")

        return ""