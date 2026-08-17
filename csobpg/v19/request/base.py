"""Base request."""

from __future__ import annotations

from abc import ABC, abstractmethod

from csobpg.v19 import signature as _s

from .dttm import get_dttm


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
        return {key: value for key, value in body.items() if value is not None}

    @abstractmethod
    def _as_json(self) -> dict:
        """Return request as JSON.

        Note: don't include merchantId, signature, and dttm since they are
        always included.
        """
