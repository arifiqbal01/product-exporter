import argparse

from src.exporters import EXPORTERS
from src.services.pipeline import ExportPipeline


def parse_cookies(cookie_string: str) -> dict[str, str]:
    """
    Convert a browser cookie string into a dictionary.

    Example:
        "sid=abc; session=xyz"

    becomes

        {
            "sid": "abc",
            "session": "xyz",
        }
    """
    cookies = {}

    if not cookie_string:
        return cookies

    for cookie in cookie_string.split(";"):
        cookie = cookie.strip()

        if "=" not in cookie:
            continue

        key, value = cookie.split("=", 1)
        cookies[key.strip()] = value.strip()

    return cookies


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
        default=None,
        help="Products per request. Uses the platform default if omitted.",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds.",
    )

    # Wix B2B options
    parser.add_argument(
        "--authorization",
        default=None,
        help="Authorization token (required for Wix B2B).",
    )

    parser.add_argument(
        "--xsrf-token",
        default=None,
        help="XSRF token (required for Wix B2B).",
    )

    parser.add_argument(
        "--cookies",
        type=parse_cookies,
        default={},
        help=(
            "Browser cookies as a semicolon-separated string. "
            "Example: 'sid=abc; session=xyz'"
        ),
    )

    parser.add_argument(
        "--linguist",
        default=None,
        help="Optional x-wix-linguist header.",
    )

    args = parser.parse_args()

    # Platform-specific validation
    if args.platform == "wix_b2b":
        if not args.authorization:
            parser.error(
                "--authorization is required when --platform wix"
            )

        if not args.xsrf_token:
            parser.error(
                "--xsrf-token is required when --platform wix"
            )

    return args


def run() -> None:
    args = parse_args()
    pipeline = ExportPipeline(args)
    pipeline.run()