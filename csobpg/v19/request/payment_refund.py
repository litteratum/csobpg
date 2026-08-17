"""Payment refund request."""

from __future__ import annotations

from .base import BaseRequest


class PaymentRefundRequest(BaseRequest):
    """Payment close request."""

    def __init__(
        self,
        merchant_id: str,
        private_key: str,
        pay_id: str,
        amount: int | None = None,
    ) -> None:
        super().__init__("payment/refund", merchant_id, private_key)
        self.pay_id = pay_id
        self.amount = amount

    def _get_params_sequence(self) -> tuple:
        return (self.merchant_id, self.pay_id, self.dttm, self.amount)

    def _as_json(self) -> dict:
        return {"payId": self.pay_id, "amount": self.amount}
