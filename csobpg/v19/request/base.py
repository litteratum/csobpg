"""Base request."""

from __future__ import annotations

from abc import ABC, abstractmethod

from csobpg.v19 import signature as _s

from .dttm import get_dttm


def _with_none_removed(body: dict) -> dict:
    """Return a copy of the dict without None values and empty objects."""
    result = {}
    for key, val in body.items():
        if val is None:
            continue
        cleaned = _cleaned(val)
        if _is_empty(cleaned):
            continue
        result[key] = cleaned
    return result


def _cleaned(val):
    """Remove None values and empty objects from a nested value."""
    if isinstance(val, dict):
        return _with_none_removed(val)
    if isinstance(val, list):
        return [
            item
            for item in (_cleaned(item) for item in val if item is not None)
            if not _is_empty(item)
        ]
    return val


def _is_empty(val) -> bool:
    """Tell whether a cleaned value carries no items at all."""
    return isinstance(val, (dict, list)) and not val


class BaseRequest(_s.SignedModel, ABC):
    """Base API request."""

    def __init__(
        self,
        endpoint: str,
        merchant_id: str,
        private_key: str,
    ) -> None:
        self.merchant_id = merchant_id
        self.private_key = private_key
        self.endpoint = endpoint.strip("/") + "/"
        self.dttm = get_dttm()

    def _sign(self) -> str:
        """Build request signature."""
        return _s.sign(self.to_sign_text().encode(), self.private_key)

    def to_json(self) -> dict | None:
        """Convert request to JSON.

        Sign with the key.
        """
        body = self._as_json()
        body["merchantId"] = self.merchant_id
        body["signature"] = self._sign()
        body["dttm"] = self.dttm
        return _with_none_removed(body)

    @abstractmethod
    def _as_json(self) -> dict:
        """Return request as JSON.

        Note: don't include merchantId, signature, and dttm since they are
        always included.
        Don't filter None or empty objects, they are filtered by the base.
        """
