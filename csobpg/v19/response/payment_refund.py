"""Response wrapper for payment/close."""

from .payment_close import PaymentCloseResponse as _PaymentCloseResponse


class PaymentRefundResponse(_PaymentCloseResponse):
    """Payment refund response."""

    @classmethod
    def _from_json(
        cls,
        response: dict,
        dttm: str,
        result_code: int,
        result_message: str,
    ) -> "PaymentRefundResponse":
        return super()._from_json(response, dttm, result_code, result_message)  # type: ignore[return-value]
