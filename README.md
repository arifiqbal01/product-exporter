# Shopify Product Exporter

A small Python utility for exporting public Shopify product data from a store’s `/products.json` endpoint and converting it into a Shopify-compatible CSV format.

## Features
- Fetches products from a Shopify storefront JSON endpoint
- Handles pagination
- Extracts product, variant, and image data
- Exports results into a CSV format suitable for Shopify workflows

## Tech
Python · Requests · CSV

## Run
```bash
python src/main.py