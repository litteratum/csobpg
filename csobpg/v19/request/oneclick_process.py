"""OneClick payment process request."""

from typing import Optional

from ..models.fingerprint import SDK, Browser, Fingerprint
from .base import BaseRequest

__all__ = [
    "OneClickPaymentProcessRequest",
    "SDK",
    "Browser",
    "Fingerprint",
]


class OneClickPaymentProcessRequest(BaseRequest):
    """OneClick Payment process request."""

    def __init__(
        self,
        merchant_id: str,
        private_key: str,
        pay_id: str,
        fingerprint: Optional[Fingerprint] = None,
    ) -> None:
        super().__init__("oneclick/process", merchant_id, private_key)
        self.pay_id = pay_id
        self.fingerprint = fingerprint

    def _get_params_sequence(self) -> tuple:
        return (
            self.merchant_id,
            self.pay_id,
            self.dttm,
            self.fingerprint,
        )

    def _as_json(self) -> dict:
        result = {
            "payId": self.pay_id,
        }
        if self.fingerprint:
            result["fingerprint"] = self.fingerprint.as_json()  # type: ignore

        return result
