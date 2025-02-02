"""Apple Pay echo request."""

from .base import BaseRequest


class ApplePayEchoRequest(BaseRequest):
    """Apple Pay echo request."""

    def __init__(self, merchant_id: str, private_key: str) -> None:
        super().__init__("applepay/echo", merchant_id, private_key)

    def _get_params_sequence(self) -> tuple:
        return (self.merchant_id, self.dttm)

    def _as_json(self) -> dict:
        return {}
