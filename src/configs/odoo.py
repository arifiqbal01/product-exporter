# src/configs/odoo.py

from dataclasses import dataclass


@dataclass(frozen=True)
class OdooPublicConfig:
    """Configuration for public Odoo storefront exports."""

    store_url: str