import csv
import time
from pathlib import Path
from typing import Any, Dict, List

import requests


CSV_FIELDS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published",
    "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value",
    "Option3 Name", "Option3 Value", "Variant SKU", "Variant Grams",
    "Variant Inventory Tracker", "Variant Inventory Qty",
    "Variant Inventory Policy", "Variant Fulfillment Service",
    "Variant Price", "Variant Compare at Price",
    "Variant Requires Shipping", "Variant Taxable",
    "Variant Barcode", "Image Src", "Image Position",
    "Gift Card", "SEO Title", "SEO Description",
    "Google Shopping / Google Product Category",
    "Google Shopping / Gender",
    "Google Shopping / Age Group",
    "Google Shopping / MPN",
    "Google Shopping / AdWords Grouping",
    "Google Shopping / AdWords Labels",
    "Google Shopping / Condition",
    "Google Shopping / Custom Product",
    "Google Shopping / Custom Label 0",
    "Google Shopping / Custom Label 1",
    "Google Shopping / Custom Label 2",
    "Google Shopping / Custom Label 3",
    "Google Shopping / Custom Label 4",
    "Variant Image", "Variant Weight Unit",
    "Variant Tax Code", "Cost per item"
]


class ShopifyProductExporter:
    def __init__(
        self,
        store_url: str,
        output_csv: str = "output/shopify_products.csv",
        start_page: int = 1,
        end_page: int | None = None,
        limit: int = 25,
        delay: float = 1.0,
    ) -> None:
        self.store_url = store_url.rstrip("/")
        self.output_csv = output_csv
        self.start_page = start_page
        self.end_page = end_page
        self.limit = limit
        self.delay = delay

    def fetch_products_page(self, page: int) -> List[Dict[str, Any]]:
        url = f"{self.store_url}/products.json?limit={self.limit}&page={page}"
        print(f"Fetching page {page}: {url}")

        response = requests.get(url, timeout=15)
        response.raise_for_status()

        return response.json().get("products", [])

    def transform_products_to_rows(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []

        for product in products:
            handle = product.get("handle", "")
            title = product.get("title", "")
            body_html = product.get("body_html", "")
            vendor = product.get("vendor", "")
            product_type = product.get("product_type", "")
            tags = product.get("tags", "")
            published = "TRUE" if product.get("published_at") else "FALSE"

            options = product.get("options", [])
            option1_name = options[0]["name"] if len(options) > 0 else ""
            option2_name = options[1]["name"] if len(options) > 1 else ""
            option3_name = options[2]["name"] if len(options) > 2 else ""

            images = product.get("images", [])
            variants = product.get("variants", [])

            for idx, variant in enumerate(variants):
                row = {
                    "Handle": handle,
                    "Title": title,
                    "Body (HTML)": body_html,
                    "Vendor": vendor,
                    "Type": product_type,
                    "Tags": tags,
                    "Published": published,

                    "Option1 Name": option1_name,
                    "Option1 Value": variant.get("option1", ""),
                    "Option2 Name": option2_name,
                    "Option2 Value": variant.get("option2", ""),
                    "Option3 Name": option3_name,
                    "Option3 Value": variant.get("option3", ""),

                    "Variant SKU": variant.get("sku", ""),
                    "Variant Grams": variant.get("grams", 0),
                    "Variant Inventory Tracker": variant.get("inventory_management", ""),
                    "Variant Inventory Qty": variant.get("inventory_quantity", 0),
                    "Variant Inventory Policy": variant.get("inventory_policy") or "deny",
                    "Variant Fulfillment Service": variant.get("fulfillment_service") or "manual",
                    "Variant Price": variant.get("price", ""),
                    "Variant Compare at Price": variant.get("compare_at_price", ""),
                    "Variant Requires Shipping": "TRUE" if variant.get("requires_shipping", True) else "FALSE",
                    "Variant Taxable": "TRUE" if variant.get("taxable", True) else "FALSE",
                    "Variant Barcode": variant.get("barcode", ""),

                    "Image Src": images[idx]["src"] if idx < len(images) else "",
                    "Image Position": idx + 1 if idx < len(images) else "",

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
                    "Variant Weight Unit": variant.get("weight_unit", ""),
                    "Variant Tax Code": "",
                    "Cost per item": "",
                }
                rows.append(row)

        return rows

    def scrape_all_products(self) -> tuple[List[Dict[str, Any]], int, int]:
        all_rows: List[Dict[str, Any]] = []
        total_products = 0
        processed_pages = 0
        page = self.start_page

        while True:
            if self.end_page is not None and page > self.end_page:
                break

            try:
                products = self.fetch_products_page(page)
            except requests.RequestException as exc:
                print(f"Request failed on page {page}: {exc}")
                break

            if not products:
                print("No more products found.")
                break

            rows = self.transform_products_to_rows(products)
            all_rows.extend(rows)
            total_products += len(products)
            processed_pages += 1

            print(f"Processed page {page}: {len(products)} products, {len(rows)} rows")
            page += 1
            time.sleep(self.delay)

        return all_rows, total_products, processed_pages

    def save_to_csv(self, rows: List[Dict[str, Any]]) -> None:
        output_path = Path(self.output_csv)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(rows)

        print(f"Saved {len(rows)} rows to {output_path}")

    def run(self) -> None:
        rows, total_products, processed_pages = self.scrape_all_products()
        self.save_to_csv(rows)

        print("\nExport complete")
        print(f"Pages processed: {processed_pages}")
        print(f"Products fetched: {total_products}")
        print(f"Rows exported: {len(rows)}")
        print(f"CSV saved to: {self.output_csv}")