import argparse

from src.exporters import EXPORTERS
from src.services.pipeline import ExportPipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export products from supported e-commerce platforms."
    )

    parser.add_argument(
        "--platform",
        choices=EXPORTERS.keys(),
        required=True,
        help="Source e-commerce platform.",
    )

    parser.add_argument(
        "--store",
        required=True,
        help="Store URL.",
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Optional output file. If omitted, a timestamped filename is generated.",
    )

    parser.add_argument(
        "--start-page",
        type=int,
        default=1,
        help="Page number to start exporting from.",
    )

    parser.add_argument(
        "--end-page",
        type=int,
        default=None,
        help="Last page to export. Omit to export all pages.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=250,
        help="Products per request.",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds.",
    )

    return parser.parse_args()


def run() -> None:
    args = parse_args()
    pipeline = ExportPipeline(args)
    pipeline.run()