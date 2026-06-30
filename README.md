# Product Exporter

A Python ETL utility for exporting products from supported e-commerce platforms into a normalized product model and generating Shopify-compatible CSV files.

Originally built as a personal migration tool and now open sourced for anyone needing to migrate or archive product catalogs.

## Features

- Multi-platform architecture
- Shopify storefront exporter
- Wix B2B exporter
- Automatic pagination
- Shopify-compatible CSV output
- Product descriptions
- Product variants
- Multiple product images
- Inventory
- Product options
- Extensible ETL architecture

## Supported Platforms

| Platform | Status |
|----------|--------|
| Shopify | ✅ |
| Wix B2B | ✅ |

## Architecture

```
Extract
    ↓
Normalize
    ↓
Transform
    ↓
Export
```

```
CLI
    ↓
Pipeline
    ↓
Platform Exporter
    ↓
Raw Platform Data
    ↓
Platform Transformer
    ↓
Normalized Product Model
    ↓
Output Transformer
    ↓
CSV Writer
```

## Project Structure

```
src/
├── configs/
├── exporters/
│   └── queries/
├── models/
├── services/
├── transformers/
│   ├── product/
│   └── output/
├── writers/
├── cli.py
└── main.py
```

## Requirements

- Python 3.11+
- requests

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Shopify

Export every product:

```bash
python -m src.main \
    --platform shopify \
    --store https://example.myshopify.com
```

Export a page range:

```bash
python -m src.main \
    --platform shopify \
    --store https://example.myshopify.com \
    --start-page 1 \
    --end-page 5
```

---

### Wix B2B

The exporter uses the same GraphQL API as the Wix B2B storefront.

Before exporting, obtain the required authentication headers from your browser.

#### Step 1 — Sign in

Log in to the Wix B2B storefront.

#### Step 2 — Open Developer Tools

Open your browser's Developer Tools.

```
F12
```

Go to:

```
Network
```

#### Step 3 — Find the storefront GraphQL requests

In the Network search box, search for:

```
ecommerce-storefront-web
```

#### Step 4 — Trigger the product list request

Apply any filter or sorting option on the product listing page.

This generates the GraphQL request:

```
operationName:
getFilteredProducts
```

Copy these request headers:

- authorization
- x-xsrf-token
- x-wix-linguist

#### Step 5 — Verify the product detail request

Open any product from the listing.

A second GraphQL request will be made.

Open its **Payload** tab and verify:

```
operationName:
getProductBySlug
```

The exporter uses this endpoint to retrieve:

- Product description
- Images
- Variants
- Product options
- Inventory
- Brand
- Additional information

#### Step 6 — Run the exporter

```bash
python -m src.main \
    --platform wix_b2b \
    --store https://example.com \
    --authorization "<authorization-token>" \
    --xsrf-token "<xsrf-token>" \
    --linguist "<x-wix-linguist>"
```

## Output

Exports Shopify-compatible CSV files containing:

- Product title
- HTML description
- Handle
- Vendor
- Product type
- Tags
- Variants
- SKU
- Prices
- Compare-at prices
- Inventory
- Product options
- Multiple product images

## Design Principles

- Separation of extraction and transformation
- Platform-specific logic remains isolated
- Common normalized product model
- Reusable output transformers
- Easy to extend with new platforms

## Future Platforms

The architecture was designed so additional exporters can be added with minimal effort.

Potential additions include:

- WooCommerce
- Magento
- BigCommerce
- Squarespace
- Ecwid

## License

MIT