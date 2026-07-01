# src/configs/woocommerce.py

from dataclasses import dataclass


@dataclass(frozen=True)
class WooCommerceConfig:
    """Configuration for WooCommerce Store API exports."""

    store_url: str
    limit: int = 100