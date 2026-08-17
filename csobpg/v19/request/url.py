"""Module for building urls."""

from collections.abc import Iterable
from urllib.parse import quote_plus, urljoin


def join_url(endpoint: str, params: Iterable[str]) -> str:
    """Join url."""
    return urljoin(endpoint, "/".join(map(quote_plus, params)))
