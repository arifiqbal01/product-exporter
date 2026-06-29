# src/models/product.py
from dataclasses import dataclass, field


@dataclass
class Image:
    src: str
    position: int = 1


@dataclass
class Variant:
    sku: str = ""
    option1: str = ""
    option2: str = ""
    option3: str = ""

    price: str = ""
    compare_at_price: str = ""

    grams: int = 0
    weight_unit: str = ""

    inventory_quantity: int = 0
    inventory_tracker: str = ""
    inventory_policy: str = "deny"

    fulfillment_service: str = "manual"

    barcode: str = ""

    taxable: bool = True
    requires_shipping: bool = True


@dataclass
class Product:
    id: str

    handle: str = ""
    title: str = ""
    description: str = ""

    vendor: str = ""
    product_type: str = ""
    tags: str = ""

    published: bool = True

    option_names: list[str] = field(default_factory=list)

    images: list[Image] = field(default_factory=list)

    variants: list[Variant] = field(default_factory=list)