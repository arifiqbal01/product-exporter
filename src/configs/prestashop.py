# src/configs/prestashop.py

from dataclasses import dataclass


@dataclass(frozen=True)
class PrestashopPublicConfig:
    """Configuration for public PrestaShop storefront exports."""

    store_url: str