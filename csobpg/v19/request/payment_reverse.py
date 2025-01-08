"""Payment reverse request."""

from .base import BaseRequest


class PaymentReverseRequest(BaseRequest):
    """Payment reverse request."""

    def __init__(
        self, merchant_id: str, private_key: str, pay_id: str
    ) -> None:
        super().__init__("payment/reverse", merchant_id, private_key)
        self.pay_id = pay_id

    def _get_params_sequence(self) -> tuple:
        return (self.merchant_id, self.pay_id, self.dttm)

    def _as_json(self) -> dict:
        return {"payId": self.pay_id}
