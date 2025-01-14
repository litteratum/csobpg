"""Response wrapper for googlepay/process."""

from .oneclick_payment_process import OneClickPaymentProcessResponse


class GooglePayPaymentProcessResponse(OneClickPaymentProcessResponse):
    """Google Pay Payment process response."""
