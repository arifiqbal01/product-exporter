# Shopify Product Exporter

A small Python utility for exporting public Shopify product data from a store’s `/products.json` endpoint and converting it into a Shopify-compatible CSV format.

## Features
- Fetches products from a Shopify storefront JSON endpoint
- Supports configurable store URL, output file, page range, limit, and delay
- Handles pagination automatically
- Extracts product, variant, and image data
- Exports results into a CSV format suitable for Shopify workflows

## Tech
Python · Requests · CSV

## Run

### Scrape one page
```bash
python src/main.py --store https://www.exportleftovers.com --end-page 1