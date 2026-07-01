# src/configs/shopify.py
from dataclasses import dataclass


@dataclass(frozen=True)
class ShopifyConfig:
    """Configuration for Shopify exports."""

    store_url: str
    limit: int = 250