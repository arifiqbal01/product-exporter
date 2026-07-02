from src.transformers.product.shopify import ShopifyTransformer
from src.transformers.output.shopify_csv import ShopifyCSVTransformer
from src.transformers.product.wix import WixProductTransformer
from src.transformers.product.woocommerce import WooCommerceTransformer
from src.transformers.product.odoo_public import OdooPublicTransformer
from src.transformers.product.prestashop_public import PrestashopPublicTransformer

PRODUCT_TRANSFORMERS = {
    "shopify": ShopifyTransformer,
    "wix_b2b": WixProductTransformer,
    "woocommerce": WooCommerceTransformer,
    "odoo_public": OdooPublicTransformer,
    "prestashop_public": PrestashopPublicTransformer,
}