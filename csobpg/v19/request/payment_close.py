"""Payment close request."""

from typing import Optional

from .base import BaseRequest


class PaymentCloseRequest(BaseRequest):
    """Payment close request."""

    def __init__(
        self,
        merchant_id: str,
        private_key: str,
        pay_id: str,
        total_amount: Optional[int] = None,
    ) -> None:
        super().__init__("payment/close", merchant_id, private_key)
        self.pay_id = pay_id
        self.total_amount = total_amount

    def _get_params_sequence(self) -> tuple:
        return (self.merchant_id, self.pay_id, self.dttm, self.total_amount)

    def _as_json(self) -> dict:
        return {"payId": self.pay_id, "totalAmount": self.total_amount}
