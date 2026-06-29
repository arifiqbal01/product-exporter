from src.transformers.product.shopify import ShopifyTransformer
from src.transformers.output.shopify_csv import ShopifyCSVTransformer

PRODUCT_TRANSFORMERS = {
    "shopify": ShopifyTransformer,
}