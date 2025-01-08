"""Response wrapper for payment/status."""

from typing import Optional

from csobpg.v19.models import actions as _actions

from .base import PaymentStatus, Response, get_payment_status


class PaymentStatusResponse(Response):
    """Payment status response."""

    def __init__(
        self,
        pay_id: str,
        dttm: str,
        result_code: int,
        result_message: str,
        payment_status: Optional[PaymentStatus] = None,
        auth_code: Optional[str] = None,
        status_detail: Optional[str] = None,
        actions: Optional[_actions.Actions] = None,
    ):
        super().__init__(dttm, result_code, result_message)
        self.pay_id = pay_id
        self.payment_status = payment_status
        self.auth_code = auth_code
        self.status_detail = status_detail
        self.actions = actions

    @classmethod
    def _from_json(
        cls, response: dict, dttm: str, result_code: int, result_message: str
    ) -> "PaymentStatusResponse":
        """Return payment status result from JSON."""
        return cls(
            response["payId"],
            dttm,
            result_code,
            result_message,
            (
                get_payment_status(response["paymentStatus"])
                if response.get("paymentStatus")
                else None
            ),
            response.get("authCode"),
            response.get("statusDetail"),
            (
                _actions.Actions.from_json(response["actions"])
                if response.get("actions")
                else None
            ),
        )

    def _get_params_sequence(self) -> tuple:
        return (
            self.pay_id,
            self.dttm,
            self.result_code,
            self.result_message,
            self.payment_status,
            self.auth_code,
            self.status_detail,
            self.actions,
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"pay_id='{self.pay_id}', "
            f"dttm='{self.dttm}', "
            f"result_code={self.result_code}, "
            f"result_message='{self.result_message}', "
            f"payment_status={self.payment_status}, "
            f"auth_code={self.auth_code}, "
            f"status_detail={self.status_detail}, "
            f"actions={self.actions}"
            ")"
        )
