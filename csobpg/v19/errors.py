"""API errors."""

from __future__ import annotations

import typing as _t

if _t.TYPE_CHECKING:
    from httprest import http as _http


class APIClientError(Exception):
    """API client error."""


class APIInvalidResponseError(APIClientError):
    """API returned an invalid response."""

    def __init__(
        self,
        message: str,
        response: _http.HTTPResponse | None = None,
    ):
        """Init API invalid response error.

        :param message: error message
        :param response: optional HTTP response object
        """
        self.response = response
        super().__init__(message)


class APIInvalidSignatureError(APIInvalidResponseError):
    """API returned invalid signature."""


class APIError(APIClientError):
    """API error."""

    def __init__(self, code: int, message: str) -> None:
        """Init API error.

        :param code: error code
        :message: error message
        """
        self.code = code
        self.message = message
        super().__init__(f"{self.code}: {self.message}")


class APIMissingParamError(APIError):
    """API missing param error."""

    def __init__(self, message: str) -> None:
        super().__init__(100, message)


class APIInvalidParamError(APIError):
    """API invalid param error."""

    def __init__(self, message: str) -> None:
        super().__init__(110, message)


class APIMerchantBlockedError(APIError):
    """API merchant is blocked error."""

    def __init__(self, message: str) -> None:
        super().__init__(120, message)


class APISessionExpiredError(APIError):
    """API session (request) expired error."""

    def __init__(self, message: str) -> None:
        super().__init__(130, message)


class APIPaymentNotFoundError(APIError):
    """API payment not found error."""

    def __init__(self, message: str) -> None:
        super().__init__(140, message)


class APIPaymentInInvalidStateError(APIError):
    """API payment is in invalid state error."""

    def __init__(self, message: str) -> None:
        super().__init__(150, message)


class APIPaymentMethodDisabledError(APIError):
    """API payment method is disabled error."""

    def __init__(self, message: str) -> None:
        super().__init__(160, message)


class APIPaymentMethodUnavailableError(APIError):
    """API payment method is unavailable error."""

    def __init__(self, message: str) -> None:
        super().__init__(170, message)


class APIOperationNotAllowedError(APIError):
    """API operation is not allowed error."""

    def __init__(self, message: str) -> None:
        super().__init__(180, message)


class APIPaymentMethodError(APIError):
    """API payment method error."""

    def __init__(self, message: str) -> None:
        super().__init__(190, message)


class APIDuplicatePurchaseIDError(APIError):
    """API duplicate purchaseId error."""

    def __init__(self, message: str) -> None:
        super().__init__(200, message)


class APIEETRejectedError(APIError):
    """API EET rejected error."""

    def __init__(self, message: str) -> None:
        super().__init__(500, message)


class APIMallPaymentPrecheckDeclinedError(APIError):
    """API mall payment declined in pre-check error."""

    def __init__(self, message: str) -> None:
        super().__init__(600, message)


class APIOneClickTemplateNotFoundError(APIError):
    """API one click template not found error."""

    def __init__(self, message: str) -> None:
        super().__init__(700, message)


class APIOneClickTemplatePaymentExpiredError(APIError):
    """API one click template payment expired error."""

    def __init__(self, message: str) -> None:
        super().__init__(710, message)


class APIOneClickTemplateCardExpiredError(APIError):
    """API one click template card expired error."""

    def __init__(self, message: str) -> None:
        super().__init__(720, message)


class APIOneClickTemplateCustomerRejectedError(APIError):
    """API one click template customer rejected error.

    the OneClick template was cancelled at the customer's request.
    """

    def __init__(self, message: str) -> None:
        super().__init__(730, message)


class APIOneClickTemplatePaymentReversedError(APIError):
    """API one click template payment reversed error."""

    def __init__(self, message: str) -> None:
        super().__init__(740, message)


class APICardholderAccountClosedError(APIError):
    """API cardholder account closed error."""

    def __init__(self, message: str) -> None:
        super().__init__(750, message)


class APICustomerNotFoundError(APIError):
    """API customer not found error."""

    def __init__(self, message: str) -> None:
        super().__init__(800, message)


class APICustomerFoundNoSavedCardsError(APIError):
    """API customer found no saved cards error."""

    def __init__(self, message: str) -> None:
        super().__init__(810, message)


class APICustomerFoundSavedCardsFoundError(APIError):
    """API customer found saved cards found error."""

    def __init__(self, message: str) -> None:
        super().__init__(820, message)


class APIInternalError(APIError):
    """API internal error."""

    def __init__(self, message: str) -> None:
        super().__init__(900, message)


_ERROR_FOR_CODE = {
    100: APIMissingParamError,
    110: APIInvalidParamError,
    120: APIMerchantBlockedError,
    130: APISessionExpiredError,
    140: APIPaymentNotFoundError,
    150: APIPaymentInInvalidStateError,
    160: APIPaymentMethodDisabledError,
    170: APIPaymentMethodUnavailableError,
    180: APIOperationNotAllowedError,
    190: APIPaymentMethodError,
    200: APIDuplicatePurchaseIDError,
    500: APIEETRejectedError,
    600: APIMallPaymentPrecheckDeclinedError,
    700: APIOneClickTemplateNotFoundError,
    710: APIOneClickTemplatePaymentExpiredError,
    720: APIOneClickTemplateCardExpiredError,
    730: APIOneClickTemplateCustomerRejectedError,
    740: APIOneClickTemplatePaymentReversedError,
    750: APICardholderAccountClosedError,
    800: APICustomerNotFoundError,
    810: APICustomerFoundNoSavedCardsError,
    820: APICustomerFoundSavedCardsFoundError,
    900: APIInternalError,
}


def raise_for_result_code(result_code: int, result_message: str) -> None:
    """Raise APIError if resultCode != 0."""
    if result_code == 0:
        return

    try:
        raise _ERROR_FOR_CODE[result_code](result_message)
    except KeyError:
        raise APIError(result_code, result_message) from None
