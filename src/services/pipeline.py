import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from src.constants import CSV_FIELDS
from src.exporters import EXPORTERS
from src.transformers import PRODUCT_TRANSFORMERS
from src.transformers.output.shopify_csv import ShopifyCSVTransformer
from src.writers.csv_writer import CSVWriter


class ExportPipeline:

    def __init__(self, args):
        self.args = args

    def run(self):

        exporter = self._build_exporter()

        page = self.args.start_page

        all_rows = []
        total_products = 0

        while True:

            if (
                self.args.end_page is not None
                and page > self.args.end_page
            ):
                break

            raw_products = exporter.fetch_page(page)

            if not raw_products:
                break

            products = PRODUCT_TRANSFORMERS[
                self.args.platform
            ].transform(raw_products)

            rows = ShopifyCSVTransformer.transform(products)

            all_rows.extend(rows)
            total_products += len(products)

            page += 1

            if self.args.delay > 0:
                time.sleep(self.args.delay)

        output_file = self._build_output_path()

        CSVWriter.write(
            rows=all_rows,
            fieldnames=CSV_FIELDS,
            output_file=output_file,
        )

        print("\nExport Complete")
        print(f"Platform : {self.args.platform}")
        print(f"Products : {total_products}")
        print(f"Rows     : {len(all_rows)}")
        print(f"Output   : {output_file}")

    def _build_exporter(self):
        exporter_cls = EXPORTERS[self.args.platform]

        return exporter_cls(
            store_url=self.args.store,
            limit=self.args.limit,
        )

    def _build_output_path(self) -> str:
        """
        Builds an output filename like:

        output/shopify/exportleftovers_20260629_163845.csv
        output/wix/littlebrands_20260630_101215.csv
        """

        # User supplied an output file
        if self.args.output:
            return self.args.output

        store_name = (
            urlparse(self.args.store)
            .netloc
            .replace("www.", "")
            .split(".")[0]
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        directory = Path("output") / self.args.platform
        directory.mkdir(parents=True, exist_ok=True)

        filename = f"{store_name}_{timestamp}.csv"

        return str(directory / filename)