"""OneClick echo request."""

from .base import BaseRequest


class OneClickEchoRequest(BaseRequest):
    """OneClick echo request."""

    def __init__(
        self, merchant_id: str, private_key: str, template_id: str
    ) -> None:
        super().__init__("oneclick/echo", merchant_id, private_key)
        self.template_id = template_id

    def _get_params_sequence(self) -> tuple:
        return (self.merchant_id, self.template_id, self.dttm)

    def _as_json(self) -> dict:
        return {"origPayId": self.template_id}
