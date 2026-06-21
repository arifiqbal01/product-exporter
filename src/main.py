import argparse

from scraper import ShopifyProductExporter


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export public Shopify products to a Shopify-compatible CSV file."
    )
    parser.add_argument(
        "--store",
        required=True,
        help="Shopify store URL, e.g. https://www.exportleftovers.com",
    )
    parser.add_argument(
        "--output",
        default="output/shopify_products.csv",
        help="Output CSV file path",
    )
    parser.add_argument(
        "--start-page",
        type=int,
        default=1,
        help="Page number to start scraping from",
    )
    parser.add_argument(
        "--end-page",
        type=int,
        default=None,
        help="Last page to scrape. Omit to scrape until no more products are found.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Products per page (Shopify usually supports up to 250 depending on endpoint behavior)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay in seconds between page requests",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    exporter = ShopifyProductExporter(
        store_url=args.store,
        output_csv=args.output,
        start_page=args.start_page,
        end_page=args.end_page,
        limit=args.limit,
        delay=args.delay,
    )
    exporter.run()


if __name__ == "__main__":
    main()