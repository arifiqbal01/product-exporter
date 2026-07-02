from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from src.configs.prestashop import PrestashopPublicConfig
from src.exporters.base import BaseExporter

class PrestashopPublicExporter(BaseExporter):
    """Fetches raw product data from a public PrestaShop storefront."""

    CATEGORY_URLS = [
        "https://label-label.be/labellabel2025/en/18-cuddle-cloths",
        "https://label-label.be/labellabel2025/en/19-rolling-cars",
        "https://label-label.be/labellabel2025/en/17-wooden-toys",
        "https://label-label.be/labellabel2025/en/20-stacking-blocks",
        "https://label-label.be/labellabel2025/en/21-activity-toys",
        "https://label-label.be/labellabel2025/en/22-rollplay",
        "https://label-label.be/labellabel2025/en/23-musical-toys",
        "https://label-label.be/labellabel2025/en/15-soft-toys",
    ]

    def __init__(self, config: PrestashopPublicConfig):
        self.config = config
        self.session = requests.Session()

        # Prevent infinite pagination / duplicate exports.
        self.seen_product_urls: set[str] = set()

    def fetch_page(self, page: int) -> list[dict[str, Any]]:
        print(f"Fetching page {page}")

        summaries = []

        for category_url in self.CATEGORY_URLS:
            summaries.extend(
                self.fetch_product_list(
                    category_url,
                    page,
                )
            )

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
            category_url: str,
            page: int,
    ) -> list[dict[str, Any]]:
        if page == 1:
            url = category_url.rstrip("/")
        else:
            url = f"{category_url.rstrip('/')}?page={page}"

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

        for card in soup.select(
            "article.product-miniature"
        ):
            link = card.select_one(
                "a.product-thumbnail"
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

        product_id = ""

        if node := soup.select_one(
            ".js-product-details"
        ):
            product_id = node.get(
                "data-id-product",
                "",
            )

        title = ""

        if node := soup.select_one("h1"):
            title = node.get_text(strip=True)

        description = ""

        if node := soup.select_one(
            ".product-description"
        ):
            description = str(node)

        price = ""

        if node := soup.select_one(
            ".current-price .price"
        ):
            price = node.get_text(strip=True)

        images: list[str] = []
        seen_images = set()

        for img in soup.select(
            ".product-images img"
        ):
            src = (
                img.get("data-magnify-src")
                or img.get("data-full-size-image-url")
                or img.get("data-src")
                or img.get("src")
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

        return {
            "id": product_id,
            "url": product_url,
            "slug": product_url.rstrip("/").split("/")[-1],
            "title": title,
            "description": description,
            "price": price,
            "images": images,
            "variants": [],
            "option_names": [],
            "vendor": "",
            "category": "",
            "tags": [],
        }
