"""Google Pay payment process request."""

from ..models.fingerprint import Fingerprint
from .oneclick_process import OneClickPaymentProcessRequest


class GooglePayPaymentProcessRequest(OneClickPaymentProcessRequest):
    """Google Pay payment process request."""

    def __init__(
        self,
        merchant_id: str,
        private_key: str,
        pay_id: str,
        fingerprint: Fingerprint,
    ) -> None:
        super().__init__(merchant_id, private_key, pay_id, fingerprint)
        self.endpoint = "googlepay/process"
