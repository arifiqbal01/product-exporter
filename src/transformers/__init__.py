from src.transformers.product.shopify import ShopifyTransformer
from src.transformers.output.shopify_csv import ShopifyCSVTransformer
from src.transformers.product.wix import WixProductTransformer
from src.transformers.product.woocommerce import WooCommerceTransformer

PRODUCT_TRANSFORMERS = {
    "shopify": ShopifyTransformer,
    "wix_b2b": WixProductTransformer,
    "woocommerce": WooCommerceTransformer,
}