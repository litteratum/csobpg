"""Payment status request."""

from .base import BaseRequest
from .url import join_url as _join_url


class PaymentStatusRequest(BaseRequest):
    """Payment status request."""

    def __init__(
        self, merchant_id: str, private_key: str, pay_id: str
    ) -> None:
        super().__init__("payment/status", merchant_id, private_key)
        self.pay_id = pay_id

        self.endpoint = _join_url(
            self.endpoint,
            [self.merchant_id, self.pay_id, self.dttm, self.signature],
        )

    def _get_params_sequence(self) -> tuple:
        return (self.merchant_id, self.pay_id, self.dttm)

    def _as_json(self) -> dict:
        return {"payId": self.pay_id}
