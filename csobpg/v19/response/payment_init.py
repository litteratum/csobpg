"""Response wrapper for payment/init."""

from typing import Optional

from .base import PaymentStatus, Response, get_payment_status


class PaymentInitResponse(Response):
    """Payment init response."""

    def __init__(
        self,
        pay_id: str,
        dttm: str,
        result_code: int,
        result_message: str,
        payment_status: Optional[PaymentStatus] = None,
        customer_code: Optional[str] = None,
        status_detail: Optional[str] = None,
    ):
        super().__init__(dttm, result_code, result_message)
        self.pay_id = pay_id
        self.payment_status = payment_status
        self.customer_code = customer_code
        self.status_detail = status_detail

    @classmethod
    def _from_json(
        cls, response: dict, dttm: str, result_code: int, result_message: str
    ) -> "PaymentInitResponse":
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
            customer_code=response.get("customerCode"),
            status_detail=response.get("statusDetail"),
        )

    def _get_params_sequence(self) -> tuple:
        return (
            self.pay_id,
            self.dttm,
            self.result_code,
            self.result_message,
            self.payment_status,
            self.customer_code,
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
            f"customer_code={self.customer_code}, "
            f"status_detail={self.status_detail}"
            ")"
        )
