"""OneClick payment process request."""

from __future__ import annotations

from csobpg.v19.models.fingerprint import SDK, Browser, Fingerprint

from .base import BaseRequest

__all__ = [
    "SDK",
    "Browser",
    "Fingerprint",
    "OneClickPaymentProcessRequest",
]


class OneClickPaymentProcessRequest(BaseRequest):
    """OneClick Payment process request."""

    def __init__(
        self,
        merchant_id: str,
        private_key: str,
        pay_id: str,
        fingerprint: Fingerprint | None = None,
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
            result["fingerprint"] = self.fingerprint.as_json()  # type: ignore[assignment]

        return result
