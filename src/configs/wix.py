from dataclasses import dataclass


@dataclass(frozen=True)
class WixConfig:
    """Configuration for Wix B2B exports."""

    store_url: str

    authorization: str
    xsrf_token: str

    limit: int = 100

    collection_id: str = "00000000-000000-000000-000000000001"

    linguist: str | None = None