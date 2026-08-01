"""Payment status request."""

from csobpg.v19 import key

from .base import BaseRequest
from .url import join_url as _join_url


class PaymentStatusRequest(BaseRequest):
    """Payment status request."""

    def __init__(
        self, merchant_id: str, private_key: key.RSAKey, pay_id: str
    ) -> None:
        super().__init__("payment/status", merchant_id)
        self.pay_id = pay_id

        self.endpoint = _join_url(
            self.endpoint,
            [
                self.merchant_id,
                self.pay_id,
                self.dttm,
                self._sign(private_key),
            ],
        )

    def _get_params_sequence(self) -> tuple:
        return (self.merchant_id, self.pay_id, self.dttm)

    def _as_json(self) -> dict:
        return {"payId": self.pay_id}
