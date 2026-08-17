"""Google Pay payment process request."""

from csobpg.v19.models import fingerprint as _fingerprint

from .oneclick_process import OneClickPaymentProcessRequest


class GooglePayPaymentProcessRequest(OneClickPaymentProcessRequest):
    """Google Pay payment process request."""

    def __init__(
        self,
        merchant_id: str,
        private_key: str,
        pay_id: str,
        fingerprint: _fingerprint.Fingerprint,
    ) -> None:
        super().__init__(merchant_id, private_key, pay_id, fingerprint)
        self.endpoint = "googlepay/process"
