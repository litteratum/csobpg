"""Response wrapper for applepay/process."""

from .oneclick_payment_process import OneClickPaymentProcessResponse


class ApplePayPaymentProcessResponse(OneClickPaymentProcessResponse):
    """Apple Pay Payment process response."""
