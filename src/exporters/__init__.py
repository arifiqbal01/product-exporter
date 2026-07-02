from src.exporters.shopify import ShopifyExporter
from src.exporters.wix_b2b import WixB2BExporter
from src.exporters.woocommerce import WooCommerceExporter
from src.exporters.odoo_public import OdooPublicExporter
from src.exporters.prestashop_public import PrestashopPublicExporter

EXPORTERS = {
    "shopify": ShopifyExporter,
    "wix_b2b": WixB2BExporter,
    "woocommerce": WooCommerceExporter,
    "odoo_public": OdooPublicExporter,
    "prestashop_public": PrestashopPublicExporter,
}