from scraper import ShopifyProductExporter


def main() -> None:
    exporter = ShopifyProductExporter(
        store_url="https://www.exportleftovers.com",
        output_csv="output/shopify_import_exportleftovers.csv",
        start_page=1,
        end_page=1,  # set to None to scrape all pages
        limit=25,
        delay=1.0,
    )
    exporter.run()


if __name__ == "__main__":
    main()