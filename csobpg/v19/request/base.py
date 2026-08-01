"""Base request."""

from abc import ABC, abstractmethod
from typing import Optional

from csobpg.v19 import key

from ..signature import SignedModel, sign
from .dttm import get_dttm


class BaseRequest(SignedModel, ABC):
    """Base API request."""

    def __init__(self, endpoint: str, merchant_id: str) -> None:
        self.merchant_id = merchant_id
        self.endpoint = endpoint.strip("/") + "/"
        self.dttm = get_dttm()

    def _sign(self, private_key: key.RSAKey) -> str:
        return sign(self.to_sign_text().encode(), str(private_key))

    def to_json(self, private_key: key.RSAKey) -> Optional[dict]:
        """Convert request to JSON.

        Sign with the key.
        """
        body = self._as_json()
        body["merchantId"] = self.merchant_id
        body["signature"] = self._sign(private_key)
        body["dttm"] = self.dttm
        return {key: value for key, value in body.items() if value is not None}

    @abstractmethod
    def _as_json(self) -> dict:
        """Return request as JSON.

        Note: don't include merchantId, signature, and dttm since they are
        always included.
        """
