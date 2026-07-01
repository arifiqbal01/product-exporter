from src.exporters.shopify import ShopifyExporter
from src.exporters.wix_b2b import WixB2BExporter
from src.exporters.woocommerce import WooCommerceExporter

EXPORTERS = {
    "shopify": ShopifyExporter,
    "wix_b2b": WixB2BExporter,
    "woocommerce": WooCommerceExporter,
}