from itertools import product
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from src.configs.odoo import OdooPublicConfig
from src.exporters.base import BaseExporter


class OdooPublicExporter(BaseExporter):
    """Fetches raw product data from a public Odoo storefront."""

    def __init__(self, config: OdooPublicConfig):
        self.config = config
        self.session = requests.Session()

        # Prevent infinite pagination / duplicate exports.
        self.seen_product_urls: set[str] = set()

    def fetch_page(self, page: int) -> list[dict[str, Any]]:
        print(f"Fetching page {page}")

        summaries = self.fetch_product_list(page)

        if not summaries:
            print("Fetched 0 products")
            return []

        new_summaries = []

        for summary in summaries:
            url = summary["url"]

            if url in self.seen_product_urls:
                continue

            self.seen_product_urls.add(url)
            new_summaries.append(summary)

        if not new_summaries:
            print("No new products found")
            return []

        products = [
            self.fetch_product(summary["url"])
            for summary in new_summaries
        ]

        print(f"Fetched {len(products)} products")

        return products

    def fetch_product_list(
        self,
        page: int,
    ) -> list[dict[str, Any]]:
        if page == 1:
            url = f"{self.config.store_url.rstrip('/')}/shop"
        else:
            url = (
                f"{self.config.store_url.rstrip('/')}"
                f"/shop/page/{page}"
            )

        response = self.session.get(
            url,
            timeout=30,
        )
        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        products: list[dict[str, Any]] = []
        seen_urls = set()

        for card in soup.select("[data-product-template-id]"):
            link = card.select_one(
                "a[href*='/shop/']"
            )

            if not link:
                continue

            href = link.get("href")

            if not href:
                continue

            product_url = urljoin(
                self.config.store_url,
                href,
            )

            if product_url in seen_urls:
                continue

            seen_urls.add(product_url)

            products.append(
                {
                    "url": product_url,
                }
            )

        return products

    def fetch_product(
        self,
        product_url: str,
    ) -> dict[str, Any]:
        response = self.session.get(
            product_url,
            timeout=30,
        )
        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        product_id = self.get_input_value(
            soup,
            "product_id",
        )

        template_id = self.get_input_value(
            soup,
            "product_template_id",
        )

        category_id = self.get_input_value(
            soup,
            "product_category_id",
        )

        title = ""

        if node := soup.select_one("h1"):
            title = node.get_text(strip=True)

        description = ""

        if node := soup.select_one(
            "#product_full_description"
        ):
            description = str(node)

        price = ""

        if node := soup.select_one(
            ".oe_currency_value"
        ):
            price = node.get_text(strip=True)

        images: list[str] = []
        seen_images = set()

        for img in soup.select(".carousel-inner img"):
            src = (
                img.get("src")
                or img.get("data-src")
                or img.get("data-lazy-src")
            )

            if not src:
                continue

            src = urljoin(
                self.config.store_url,
                src,
            )

            if src in seen_images:
                continue

            seen_images.add(src)
            images.append(src)

        option_names: list[str] = []
        option_values: list[list[str]] = []

        for attribute in soup.select(
            "[data-attribute_name]"
        ):
            name = attribute.get(
                "data-attribute_name",
                "",
            ).strip()

            values = list(
                dict.fromkeys(
                    value.get(
                        "data-value_name",
                        "",
                    ).strip()
                    for value in attribute.select(
                        "[data-value_name]"
                    )
                    if value.get("data-value_name")
                )
            )

            if not name or not values:
                continue

            option_names.append(name)
            option_values.append(values)

        variants = self.build_variants(
            option_values,
            price,
        )

        return {
            "id": template_id or product_id,
            "product_id": product_id,
            "template_id": template_id,
            "category_id": category_id,
            "slug": product_url.rstrip("/").split("/")[-1],
            "url": product_url,
            "title": title,
            "description": description,
            "price": price,
            "images": images,
            "option_names": option_names,
            "variants": variants,
            "vendor": "",
            "category": "",
            "tags": [],
        }

    @staticmethod
    def build_variants(
        option_values: list[list[str]],
        price: str,
    ) -> list[dict[str, Any]]:
        if not option_values:
            return [
                {
                    "sku": "",
                    "options": [],
                    "price": price,
                    "compare_at_price": "",
                }
            ]

        variants = []

        for combination in product(*option_values):
            variants.append(
                {
                    "sku": "",
                    "options": list(combination),
                    "price": price,
                    "compare_at_price": "",
                }
            )

        return variants

    @staticmethod
    def get_input_value(
        soup: BeautifulSoup,
        name: str,
    ) -> str:
        if node := soup.select_one(
            f"input[name='{name}']"
        ):
            return node.get(
                "value",
                "",
            )

        return ""