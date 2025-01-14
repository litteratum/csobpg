"""Response wrapper for Google Pay payment init."""

from .oneclick_payment_init import OneClickPaymentInitResponse


class GooglePayPaymentInitResponse(OneClickPaymentInitResponse):
    """Google Pay payment init response."""
