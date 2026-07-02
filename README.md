# Product Exporter

A Python ETL utility for exporting products from supported e-commerce platforms into a normalized product model and generating Shopify-compatible CSV files.

Originally built as a personal migration tool and now open sourced for anyone needing to migrate or archive product catalogs.

## Features

- Multi-platform ETL architecture
- Shopify REST API exporter
- Wix B2B GraphQL exporter
- WooCommerce Store API exporter
- Odoo public storefront exporter
- PrestaShop public storefront exporter
- Automatic pagination
- Shopify-compatible CSV output
- Product descriptions
- Product variants
- Multiple product images
- Inventory
- Product options
- Extensible architecture for adding new platforms

## Supported Platforms

| Platform | Method | Status |
|----------|--------|--------|
| Shopify | REST API | ✅ |
| Wix B2B | GraphQL | ✅ |
| WooCommerce | Store API | ✅ |
| Odoo | Public HTML | ✅ |
| PrestaShop | Public HTML | ✅ |

## Architecture

```
Platform
    ↓
Exporter
    ↓
Raw Dictionary
    ↓
Transformer
    ↓
Product Model
    ↓
Output Transformer
    ↓
CSV Writer
```

### ETL Responsibilities

**Exporter**

- HTTP requests
- API communication
- HTML scraping
- Pagination
- Authentication (when required)
- Returns normalized raw dictionaries

**Transformer**

- Converts raw dictionaries into the common `Product` model
- No HTTP requests
- No HTML parsing

**Writer**

- Generates Shopify-compatible CSV files
- Platform independent

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
- beautifulsoup4

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Shopify

```bash
python -m src.main \
    --platform shopify \
    --store https://example.myshopify.com
```

---

### WooCommerce

```bash
python -m src.main \
    --platform woocommerce \
    --store https://example.com
```

---

### Odoo (Public Storefront)

```bash
python -m src.main \
    --platform odoo_public \
    --store https://example.com
```

---

### PrestaShop (Public Storefront)

```bash
python -m src.main \
    --platform prestashop_public \
    --store https://example.com/category
```

> **Note:** The current public exporter starts from category pages. Automatic category discovery will be added in a future release.

---

### Wix B2B

The exporter uses the same GraphQL API as the Wix B2B storefront.

Before exporting, obtain the required authentication headers from your browser.

#### 1. Sign in

Log in to the Wix B2B storefront.

#### 2. Open Developer Tools

Open:

```
F12
```

Go to:

```
Network
```

#### 3. Find GraphQL requests

Search for:

```
ecommerce-storefront-web
```

#### 4. Trigger the product listing request

Apply any filter or sorting option.

Copy these request headers:

- authorization
- x-xsrf-token
- x-wix-linguist

#### 5. Run the exporter

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
- Barcode
- Prices
- Compare-at prices
- Inventory
- Product options
- Multiple product images

## Design Principles

- ETL architecture
- Separation of extraction and transformation
- Platform-specific logic isolated inside exporters
- Shared normalized `Product` model
- Platform-independent output writers
- Easy to extend with new platforms

## Future Platforms

The architecture is designed so additional exporters can be added with minimal effort.

Potential additions include:

- Magento
- BigCommerce
- Squarespace
- Ecwid
- OpenCart
- Big Cartel
- Shift4Shop

## License

MIT