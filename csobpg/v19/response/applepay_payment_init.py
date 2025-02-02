"""Response wrapper for Apple Pay payment init."""

from .oneclick_payment_init import OneClickPaymentInitResponse


class ApplePayPaymentInitResponse(OneClickPaymentInitResponse):
    """Apple Pay payment init response."""
