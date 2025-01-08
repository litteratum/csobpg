"""Response wrapper for payment/reverse."""

from typing import Optional

from .base import PaymentStatus, Response, get_payment_status


class PaymentReverseResponse(Response):
    """Payment reverse response."""

    def __init__(
        self,
        pay_id: str,
        dttm: str,
        result_code: int,
        result_message: str,
        payment_status: Optional[PaymentStatus] = None,
        status_detail: Optional[str] = None,
    ):
        super().__init__(dttm, result_code, result_message)
        self.pay_id = pay_id
        self.payment_status = payment_status
        self.status_detail = status_detail

    @classmethod
    def _from_json(
        cls, response: dict, dttm: str, result_code: int, result_message: str
    ) -> "PaymentReverseResponse":
        """Return payment init result from JSON."""
        return cls(
            response["payId"],
            dttm,
            result_code,
            result_message,
            payment_status=(
                get_payment_status(response["paymentStatus"])
                if response.get("paymentStatus")
                else None
            ),
            status_detail=response.get("statusDetail"),
        )

    def _get_params_sequence(self) -> tuple:
        return (
            self.pay_id,
            self.dttm,
            self.result_code,
            self.result_message,
            self.payment_status,
            self.status_detail,
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"pay_id='{self.pay_id}', "
            f"dttm='{self.dttm}', "
            f"result_code={self.result_code}, "
            f"result_message='{self.result_message}', "
            f"status={self.payment_status}, "
            f"status_detail={self.status_detail}"
            ")"
        )
