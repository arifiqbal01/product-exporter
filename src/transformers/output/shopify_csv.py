# app/transformers/output/shopify_csv.py
from src.models.product import Product


class ShopifyCSVTransformer:
    """Transforms normalized Product models into Shopify CSV rows."""

    @staticmethod
    def transform(products: list[Product]) -> list[dict]:
        rows: list[dict] = []

        for product in products:
            option_names = product.option_names + ["", "", ""]
            images = product.images

            # Write variant rows
            for index, variant in enumerate(product.variants):
                image = images[index] if index < len(images) else None

                rows.append(
                    {
                        "Handle": product.handle,
                        "Title": product.title,
                        "Body (HTML)": product.description,
                        "Vendor": product.vendor,
                        "Type": product.product_type,
                        "Tags": product.tags,
                        "Published": "TRUE" if product.published else "FALSE",

                        "Option1 Name": option_names[0],
                        "Option1 Value": variant.option1,

                        "Option2 Name": option_names[1],
                        "Option2 Value": variant.option2,

                        "Option3 Name": option_names[2],
                        "Option3 Value": variant.option3,

                        "Variant SKU": variant.sku,
                        "Variant Grams": variant.grams,

                        "Variant Inventory Tracker": variant.inventory_tracker,
                        "Variant Inventory Qty": variant.inventory_quantity,
                        "Variant Inventory Policy": variant.inventory_policy,

                        "Variant Fulfillment Service": variant.fulfillment_service,

                        "Variant Price": variant.price,
                        "Variant Compare at Price": variant.compare_at_price,

                        "Variant Requires Shipping": (
                            "TRUE" if variant.requires_shipping else "FALSE"
                        ),
                        "Variant Taxable": (
                            "TRUE" if variant.taxable else "FALSE"
                        ),

                        "Variant Barcode": variant.barcode,

                        "Image Src": image.src if image else "",
                        "Image Position": image.position if image else "",

                        "Gift Card": "FALSE",

                        "SEO Title": "",
                        "SEO Description": "",

                        "Google Shopping / Google Product Category": "",
                        "Google Shopping / Gender": "",
                        "Google Shopping / Age Group": "",
                        "Google Shopping / MPN": "",
                        "Google Shopping / AdWords Grouping": "",
                        "Google Shopping / AdWords Labels": "",
                        "Google Shopping / Condition": "",
                        "Google Shopping / Custom Product": "",
                        "Google Shopping / Custom Label 0": "",
                        "Google Shopping / Custom Label 1": "",
                        "Google Shopping / Custom Label 2": "",
                        "Google Shopping / Custom Label 3": "",
                        "Google Shopping / Custom Label 4": "",

                        "Variant Image": "",
                        "Variant Weight Unit": variant.weight_unit,

                        "Variant Tax Code": "",
                        "Cost per item": "",
                    }
                )

            # Write additional image rows
            start = max(len(product.variants), 1)

            for image in images[start:]:
                rows.append(
                    {
                        "Handle": product.handle,
                        "Title": "",
                        "Body (HTML)": "",
                        "Vendor": "",
                        "Type": "",
                        "Tags": "",
                        "Published": "",

                        "Option1 Name": "",
                        "Option1 Value": "",

                        "Option2 Name": "",
                        "Option2 Value": "",

                        "Option3 Name": "",
                        "Option3 Value": "",

                        "Variant SKU": "",
                        "Variant Grams": "",

                        "Variant Inventory Tracker": "",
                        "Variant Inventory Qty": "",
                        "Variant Inventory Policy": "",

                        "Variant Fulfillment Service": "",

                        "Variant Price": "",
                        "Variant Compare at Price": "",

                        "Variant Requires Shipping": "",
                        "Variant Taxable": "",

                        "Variant Barcode": "",

                        "Image Src": image.src,
                        "Image Position": image.position,

                        "Gift Card": "",

                        "SEO Title": "",
                        "SEO Description": "",

                        "Google Shopping / Google Product Category": "",
                        "Google Shopping / Gender": "",
                        "Google Shopping / Age Group": "",
                        "Google Shopping / MPN": "",
                        "Google Shopping / AdWords Grouping": "",
                        "Google Shopping / AdWords Labels": "",
                        "Google Shopping / Condition": "",
                        "Google Shopping / Custom Product": "",
                        "Google Shopping / Custom Label 0": "",
                        "Google Shopping / Custom Label 1": "",
                        "Google Shopping / Custom Label 2": "",
                        "Google Shopping / Custom Label 3": "",
                        "Google Shopping / Custom Label 4": "",

                        "Variant Image": "",
                        "Variant Weight Unit": "",

                        "Variant Tax Code": "",
                        "Cost per item": "",
                    }
                )

        return rows