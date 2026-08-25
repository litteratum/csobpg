"""Merchant wrappers."""

from base64 import b64encode


def pack_merchant_data(data: bytes) -> str:
    """Pack Merchant Data.

    It must be transferred as BASE64 encoded string.
    """
    return b64encode(data).decode("UTF-8")
