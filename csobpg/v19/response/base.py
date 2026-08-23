"""Base API response wrappers."""

from abc import ABC, abstractmethod
from enum import Enum

from csobpg.v19 import errors as _e
from csobpg.v19 import signature as _s


class PaymentStatus(Enum):
    """Payment status."""

    INITIATED = 1
    IN_PROGRESS = 2
    CANCELLED = 3
    CONFIRMED = 4
    REVERSED = 5
    DENIED = 6
    WAITING_SETTLEMENT = 7
    SETTLED = 8
    REFUND_PROCESSING = 9
    RETURNED = 10


def get_payment_status(status: int) -> PaymentStatus:
    """Build payment status from its code."""
    try:
        return PaymentStatus(status)
    except ValueError:
        raise _e.APIInvalidResponseError(
            f'Unexpected paymentStatus "{status}"',
        ) from None


class Response(_s.SignedModel, ABC):
    """API response."""

    def __init__(self, dttm: str, result_code: int, result_message: str):
        self.dttm = dttm
        self.result_code = result_code
        self.result_message = result_message

    @property
    def success(self) -> bool:
        """Return whether the request was successful."""
        return self.result_code == 0

    @classmethod
    def from_json(cls, response: dict, public_key: str):
        """Return response from JSON.

        :param response: valid signed response from the API
        :param public_key: public key to verify the response signature
        """
        result_code = response["resultCode"]
        result_message = response.get("resultMessage", "")

        try:
            obj = cls._from_json(
                response,
                response.get("dttm", ""),
                result_code,
                result_message,
            )
        except KeyError as exc:
            raise _e.APIInvalidResponseError(
                f'Missing mandatory parameter "{exc.args[0]}"',
            ) from None
        except (ValueError, TypeError) as exc:
            raise _e.APIInvalidResponseError(
                f"Invalid parameter value: {exc}",
            ) from None

        _s.verify(
            response["signature"],
            obj.to_sign_text().encode(),
            public_key,
        )
        _e.raise_for_result_code(result_code, result_message)
        return obj

    @classmethod
    @abstractmethod
    def _from_json(
        cls,
        response: dict,
        dttm: str,
        result_code: int,
        result_message: str,
    ) -> "Response":
        """Return response from JSON."""
