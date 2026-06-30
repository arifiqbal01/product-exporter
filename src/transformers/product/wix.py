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
            description=raw_product.get("description", ""),
            vendor=raw_product.get("brand", ""),
            product_type=raw_product.get("productType", ""),
            tags=raw_product.get("ribbon") or "",
            published=raw_product.get("isVisible", True),
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

        # Variants
        product_items = raw_product.get("productItems", [])

        if product_items:
            option_titles = [
                option.get("title", "")
                for option in raw_product.get("options", [])
            ]

            product.option_names = option_titles

            for item in product_items:
                selections = item.get("optionsSelections", [])

                option_values = ["", "", ""]

                for option_index, selection_id in enumerate(selections):
                    if option_index >= len(raw_product.get("options", [])):
                        continue

                    option = raw_product["options"][option_index]

                    selection = next(
                        (
                            s
                            for s in option.get("selections", [])
                            if s["id"] == selection_id
                        ),
                        None,
                    )

                    if selection:
                        option_values[option_index] = selection.get(
                            "value",
                            "",
                        )

                inventory = item.get("inventory") or {}

                product.variants.append(
                    Variant(
                        sku=item.get("sku") or "",
                        option1=option_values[0],
                        option2=option_values[1],
                        option3=option_values[2],
                        price=str(item.get("price") or ""),
                        compare_at_price=str(
                            item.get("comparePrice") or ""
                        ),
                        grams=int((item.get("weight") or 0) * 1000),
                        weight_unit="g",
                        inventory_quantity=inventory.get("quantity") or 0,
                        inventory_tracker="shopify",
                        inventory_policy="deny",
                        fulfillment_service="manual",
                        taxable=True,
                        requires_shipping=True,
                    )
                )

        else:
            inventory = raw_product.get("inventory") or {}

            product.variants.append(
                Variant(
                    sku=raw_product.get("sku", ""),
                    price=str(raw_product.get("price") or ""),
                    compare_at_price=str(
                        raw_product.get("comparePrice") or ""
                    ),
                    inventory_quantity=inventory.get("quantity") or 0,
                    inventory_tracker="shopify",
                    inventory_policy="deny",
                    fulfillment_service="manual",
                    taxable=True,
                    requires_shipping=True,
                )
            )

        return product