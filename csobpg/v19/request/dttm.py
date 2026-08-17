"""Module for dealing with dttm."""

from __future__ import annotations

import datetime

_DT_FORMAT = "%Y%m%d%H%M%S"


def get_dttm() -> str:
    """Build current dttm."""
    return datetime.datetime.now().astimezone().strftime(_DT_FORMAT)


def decode_dttm(value: str) -> datetime.datetime:
    """Decode value to the datetime object."""
    # TODO: ValueError
    return datetime.datetime.strptime(value, _DT_FORMAT).astimezone()


def get_payment_expiry(hours: int | None) -> str | None:
    """Get payment expiry date."""
    if not hours:
        return None

    if hours <= 0:
        raise ValueError('"payment_expiry" must be [1, 1440]')

    expiry_dt = datetime.datetime.now().astimezone()
    expiry_dt = expiry_dt + datetime.timedelta(hours=hours)
    return expiry_dt.strftime(_DT_FORMAT)
