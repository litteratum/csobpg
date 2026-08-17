"""Merchant wrappers."""

from base64 import b64encode

_MERCHANT_DATA_LEN_MAX = 255


def pack_merchant_data(data: bytes) -> str:
    """Pack Merchant Data.

    It must be transferred as BASE64 encoded string.
    """
    encoded = b64encode(data).decode("UTF-8")

    if len(encoded) > _MERCHANT_DATA_LEN_MAX:
        raise ValueError(
            "Merchant data length encoded to BASE64 is over "
            f"{_MERCHANT_DATA_LEN_MAX} chars",
        )

    return encoded
