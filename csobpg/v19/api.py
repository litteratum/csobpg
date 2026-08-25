"""API client."""

from __future__ import annotations

import http as _h
import logging
from typing import TYPE_CHECKING

from httprest import API
from httprest import http as _http
from httprest.http import errors as _http_errs

from csobpg.v19 import errors as _e
from csobpg.v19.models.currency import Currency
from csobpg.v19.models.payment import (
    PaymentMethod,
    PaymentOperation,
    ReturnMethod,
)
from csobpg.v19.models.webpage import WebPageAppearanceConfig, WebPageLanguage

from . import request as _request
from . import response as _response
from .key import FileRSAKey, RAMRSAKey, RSAKey

if TYPE_CHECKING:
    from httprest.http import HTTPClient

    from csobpg.v19.models.cart import Cart
    from csobpg.v19.models.customer import CustomerData
    from csobpg.v19.models.fingerprint import Fingerprint
    from csobpg.v19.models.order import OrderData


class APIClient(API):
    """API client."""

    def __init__(
        self,
        merchant_id: str,
        private_key: str | RSAKey,
        public_key: str | RSAKey,
        base_url: str = "https://api.platebnibrana.csob.cz/api/v1.9",
        http_client: HTTPClient | None = None,
    ) -> None:
        super().__init__(base_url, http_client)
        self.merchant_id = merchant_id

        if isinstance(private_key, str):
            self.private_key = FileRSAKey(private_key)
        else:
            self.private_key = private_key

        if isinstance(public_key, str):
            self.public_key = RAMRSAKey(public_key)
        else:
            self.public_key = public_key

        self._log = logging.getLogger(str(self))

    def init_payment(
        self,
        order_no: str,
        total_amount: int,
        return_url: str,
        return_method: ReturnMethod = ReturnMethod.POST,
        payment_operation: PaymentOperation = PaymentOperation.PAYMENT,
        payment_method: PaymentMethod = PaymentMethod.CARD,
        currency: Currency = Currency.CZK,
        close_payment: bool = True,
        ttl_sec: int = 600,
        cart: Cart | None = None,
        customer: CustomerData | None = None,
        order: OrderData | None = None,
        merchant_data: bytes | None = None,
        customer_id: str | None = None,
        payment_expiry: int | None = None,
        page_appearance: WebPageAppearanceConfig | None = None,
    ) -> _response.PaymentInitResponse:
        """Init payment."""
        self._log.info(
            'Initializing payment: order_no="%s", total_amount=%s, '
            'return_url="%s", return_method=%s, payment_operation=%s, '
            "payment_method=%s, currency=%s, close_payment=%s, ttl_sec=%s, "
            "cart=%s, customer=%s, order=%s, customer_id=%s, "
            "payment_expiry=%s",
            order_no,
            total_amount,
            return_url,
            return_method,
            payment_operation,
            payment_method,
            currency,
            close_payment,
            ttl_sec,
            cart,
            customer,
            order,
            customer_id,
            payment_expiry,
        )
        request = _request.PaymentInitRequest(
            self.merchant_id,
            str(self.private_key),
            order_no=order_no,
            total_amount=total_amount,
            return_url=return_url,
            return_method=return_method,
            payment_operation=payment_operation,
            payment_method=payment_method,
            currency=currency,
            close_payment=close_payment,
            ttl_sec=ttl_sec,
            cart=cart,
            customer=customer,
            order=order,
            merchant_data=merchant_data,
            customer_id=customer_id,
            payment_expiry=payment_expiry,
            page_appearance=page_appearance,
        )
        return _response.PaymentInitResponse.from_json(
            self._call_api("post", request.endpoint, json=request.to_json()),
            str(self.public_key),
        )

    def oneclick_init_payment(
        self,
        template_id: str,
        order_no: str,
        return_url: str,
        return_method: ReturnMethod = ReturnMethod.POST,
        payment_method: PaymentMethod = PaymentMethod.CARD,
        client_ip: str | None = None,
        total_amount: int | None = None,
        currency: Currency | None = None,
        close_payment: bool | None = None,
        customer: CustomerData | None = None,
        order: OrderData | None = None,
        client_initiated: bool = True,
        sdk_used: bool = False,
        merchant_data: bytes | None = None,
        ttl_sec: int | None = None,
        language: WebPageLanguage = WebPageLanguage.CS,
    ) -> _response.OneClickPaymentInitResponse:
        """Init OneClick payment.

        :param template_id: OneClick template ID. Corresponds to the payId
          initiated by a payment init with PaymentOperation.ONE_CLICK_PAYMENT
        """
        self._log.info(
            'Initializing OneClick payment using the "%s" template: '
            'order_no="%s", total_amount=%s, return_url="%s", '
            "return_method=%s, payment_method=%s, currency=%s, "
            "close_payment=%s, ttl_sec=%s, customer=%s, order=%s, "
            "client_initiated=%s, sdk_used=%s",
            template_id,
            order_no,
            total_amount,
            return_url,
            return_method,
            payment_method,
            currency,
            close_payment,
            ttl_sec,
            customer,
            order,
            client_initiated,
            sdk_used,
        )

        request = _request.OneClickPaymentInitRequest(
            self.merchant_id,
            str(self.private_key),
            template_id=template_id,
            order_no=order_no,
            total_amount=total_amount,
            return_url=return_url,
            return_method=return_method,
            payment_method=payment_method,
            currency=currency,
            close_payment=close_payment,
            ttl_sec=ttl_sec,
            customer=customer,
            order=order,
            merchant_data=merchant_data,
            client_ip=client_ip,
            client_initiated=client_initiated,
            sdk_used=sdk_used,
            language=language,
        )
        return _response.OneClickPaymentInitResponse.from_json(
            self._call_api("post", request.endpoint, json=request.to_json()),
            str(self.public_key),
        )

    def oneclick_process(
        self,
        pay_id: str,
        fingerprint: Fingerprint | None = None,
    ) -> _response.OneClickPaymentProcessResponse:
        """Start OneClick payment processing."""
        self._log.info(
            "Starting OneClick payment processing for pay_id=%s",
            pay_id,
        )
        request = _request.OneClickPaymentProcessRequest(
            self.merchant_id,
            str(self.private_key),
            pay_id,
            fingerprint,
        )
        return _response.OneClickPaymentProcessResponse.from_json(
            self._call_api("post", request.endpoint, request.to_json()),
            str(self.public_key),
        )

    def oneclick_echo(
        self,
        template_id: str,
    ) -> _response.OneClickEchoResponse:
        """Make an OneClick echo request."""
        self._log.info('OneClick echo request for "%s"', template_id)
        request = _request.OneClickEchoRequest(
            self.merchant_id,
            str(self.private_key),
            template_id,
        )
        return _response.OneClickEchoResponse.from_json(
            self._call_api("post", request.endpoint, request.to_json()),
            str(self.public_key),
        )

    def get_payment_status(
        self,
        pay_id: str,
    ) -> _response.PaymentStatusResponse:
        """Request payment status information."""
        self._log.info("Requesting payment status for pay_id=%s", pay_id)
        request = _request.PaymentStatusRequest(
            self.merchant_id,
            str(self.private_key),
            pay_id,
        )
        return _response.PaymentStatusResponse.from_json(
            self._call_api("get", request.endpoint),
            str(self.public_key),
        )

    def reverse_payment(self, pay_id: str) -> _response.PaymentReverseResponse:
        """Reverse payment.

        :param pay_id: payment ID
        """
        self._log.info("Reversing payment for pay_id=%s", pay_id)
        request = _request.PaymentReverseRequest(
            self.merchant_id,
            str(self.private_key),
            pay_id,
        )
        return _response.PaymentReverseResponse.from_json(
            self._call_api("put", request.endpoint, request.to_json()),
            str(self.public_key),
        )

    def close_payment(
        self,
        pay_id: str,
        total_amount: int | None = None,
    ) -> _response.PaymentCloseResponse:
        """Close payment (move to settlement).

        :param total_amount: close the payment with this amount. It must be
          less or equal to the original amount and provided in hundredths of
          the base currency
        """
        self._log.info(
            "Closing payment for pay_id=%s, total_amount=%s",
            pay_id,
            total_amount,
        )
        request = _request.PaymentCloseRequest(
            self.merchant_id,
            str(self.private_key),
            pay_id,
            total_amount,
        )
        return _response.PaymentCloseResponse.from_json(
            self._call_api("put", request.endpoint, json=request.to_json()),
            str(self.public_key),
        )

    def refund_payment(
        self,
        pay_id: str,
        amount: int | None = None,
    ) -> _response.PaymentRefundResponse:
        """Refund payment.

        :param pay_id: payment ID
        :param amount: amount to refund. It must be less or equal to the
          original amount and provided in hundredths of the base currency.
          If not provided, the full amount will be refunded.
        """
        self._log.info(
            "Refunding payment for pay_id=%s, amount=%s",
            pay_id,
            amount,
        )
        request = _request.PaymentRefundRequest(
            self.merchant_id,
            str(self.private_key),
            pay_id,
            amount,
        )
        return _response.PaymentRefundResponse.from_json(
            self._call_api("put", request.endpoint, request.to_json()),
            str(self.public_key),
        )

    def get_payment_process_url(self, pay_id: str) -> str:
        """Build payment URL.

        :param pay_id: pay_id obtained from `payment_init`
        :return: url to process payment
        """
        self._log.info("Building payment URL for pay_id=%s", pay_id)
        return self._build_url(
            _request.PaymentProcessRequest(
                self.merchant_id,
                str(self.private_key),
                pay_id,
            ).endpoint,
        )

    def echo(self) -> _response.EchoResponse:
        """Make an echo request."""
        self._log.info("Making echo request")
        request = _request.EchoRequest(self.merchant_id, str(self.private_key))
        return _response.EchoResponse.from_json(
            self._call_api("post", request.endpoint, request.to_json()),
            str(self.public_key),
        )

    def process_gateway_return(
        self,
        datadict: dict,
    ) -> _response.PaymentProcessResponse:
        """Process gateway return."""
        self._log.info("Processing gateway return %s", datadict)
        data = {**datadict}

        self._validate_response_json(data)
        self._ensure_signature(data)

        return _response.PaymentProcessResponse.from_json(
            data,
            str(self.public_key),
        )

    def googlepay_echo(self) -> _response.GooglePayEchoResponse:
        """Make a Google Pay echo request."""
        self._log.info("Making Google Pay echo request")
        request = _request.GooglePayEchoRequest(
            self.merchant_id,
            str(self.private_key),
        )
        return _response.GooglePayEchoResponse.from_json(
            self._call_api("post", request.endpoint, request.to_json()),
            str(self.public_key),
        )

    def googlepay_init(
        self,
        order_no: str,
        client_ip: str,
        total_amount: int,
        payload: dict,
        return_url: str,
        return_method: ReturnMethod = ReturnMethod.POST,
        currency: Currency = Currency.CZK,
        close_payment: bool | None = None,
        customer: CustomerData | None = None,
        order: OrderData | None = None,
        sdk_used: bool = False,
        merchant_data: bytes | None = None,
        language: WebPageLanguage = WebPageLanguage.CS,
        ttl_sec: int | None = None,
    ) -> _response.GooglePayPaymentInitResponse:
        """Init Google Pay payment."""
        self._log.info(
            "Initializing Google Pay payment: "
            'order_no="%s", total_amount=%s, return_url="%s", '
            "return_method=%s, currency=%s, "
            "close_payment=%s, customer=%s, order=%s, "
            "sdk_used=%s, language=%s, ttl_sec=%s",
            order_no,
            total_amount,
            return_url,
            return_method,
            currency,
            close_payment,
            customer,
            order,
            sdk_used,
            language,
            ttl_sec,
        )
        request = _request.GooglePayPaymentInitRequest(
            self.merchant_id,
            str(self.private_key),
            order_no=order_no,
            client_ip=client_ip,
            total_amount=total_amount,
            payload=payload,
            return_url=return_url,
            return_method=return_method,
            currency=currency,
            close_payment=close_payment,
            customer=customer,
            order=order,
            sdk_used=sdk_used,
            merchant_data=merchant_data,
            language=language,
            ttl_sec=ttl_sec,
        )
        return _response.GooglePayPaymentInitResponse.from_json(
            self._call_api("post", request.endpoint, json=request.to_json()),
            str(self.public_key),
        )

    def googlepay_process(
        self,
        pay_id: str,
        fingerprint: Fingerprint,
    ) -> _response.GooglePayPaymentProcessResponse:
        """Start Google Pay payment processing."""
        self._log.info(
            "Starting Google Pay payment processing for pay_id=%s",
            pay_id,
        )
        request = _request.GooglePayPaymentProcessRequest(
            self.merchant_id,
            str(self.private_key),
            pay_id,
            fingerprint,
        )
        return _response.GooglePayPaymentProcessResponse.from_json(
            self._call_api("post", request.endpoint, request.to_json()),
            str(self.public_key),
        )

    def applepay_echo(self) -> _response.ApplePayEchoResponse:
        """Make Apple Pay echo request."""
        self._log.info("Making Apple Pay echo request")
        request = _request.ApplePayEchoRequest(
            self.merchant_id,
            str(self.private_key),
        )
        return _response.ApplePayEchoResponse.from_json(
            self._call_api("post", request.endpoint, request.to_json()),
            str(self.public_key),
        )

    def applepay_init(
        self,
        order_no: str,
        client_ip: str,
        total_amount: int,
        payload: dict,
        return_url: str,
        return_method: ReturnMethod = ReturnMethod.POST,
        currency: Currency = Currency.CZK,
        close_payment: bool | None = None,
        customer: CustomerData | None = None,
        order: OrderData | None = None,
        sdk_used: bool = False,
        merchant_data: bytes | None = None,
        language: WebPageLanguage = WebPageLanguage.CS,
        ttl_sec: int | None = None,
    ) -> _response.ApplePayPaymentInitResponse:
        """Init Apple Pay payment."""
        self._log.info(
            "Initializing Apple Pay payment: "
            'order_no="%s", total_amount=%s, return_url="%s", '
            "return_method=%s, currency=%s, "
            "close_payment=%s, customer=%s, order=%s, "
            "sdk_used=%s, language=%s, ttl_sec=%s",
            order_no,
            total_amount,
            return_url,
            return_method,
            currency,
            close_payment,
            customer,
            order,
            sdk_used,
            language,
            ttl_sec,
        )
        request = _request.ApplePayPaymentInitRequest(
            self.merchant_id,
            str(self.private_key),
            order_no=order_no,
            client_ip=client_ip,
            total_amount=total_amount,
            payload=payload,
            return_url=return_url,
            return_method=return_method,
            currency=currency,
            close_payment=close_payment,
            customer=customer,
            order=order,
            sdk_used=sdk_used,
            merchant_data=merchant_data,
            language=language,
            ttl_sec=ttl_sec,
        )
        return _response.ApplePayPaymentInitResponse.from_json(
            self._call_api("post", request.endpoint, json=request.to_json()),
            str(self.public_key),
        )

    def applepay_process(
        self,
        pay_id: str,
        fingerprint: Fingerprint,
    ) -> _response.ApplePayPaymentProcessResponse:
        """Start Apple Pay payment processing."""
        self._log.info(
            "Starting Apple Pay payment processing for pay_id=%s",
            pay_id,
        )
        request = _request.ApplePayPaymentProcessRequest(
            self.merchant_id,
            str(self.private_key),
            pay_id,
            fingerprint,
        )
        return _response.ApplePayPaymentProcessResponse.from_json(
            self._call_api("post", request.endpoint, request.to_json()),
            str(self.public_key),
        )

    def _call_api(
        self,
        method: str,
        endpoint: str,
        json: dict | None = None,
    ) -> dict:
        http_response = self._request(method, endpoint, json)
        body = self._extract_response_json(http_response)

        if http_response.status_code != _h.HTTPStatus.OK:
            _e.raise_for_result_code(
                body["resultCode"],
                body.get("resultMessage", ""),
            )
            raise _e.APIInvalidResponseError(
                "resultCode is 0 but HTTP status code is not 200",
                response=http_response,
            )

        try:
            self._ensure_signature(body)
        except _e.APIInvalidResponseError as exc:
            raise _e.APIInvalidResponseError(
                str(exc),
                response=http_response,
            ) from None

        return body

    def _extract_response_json(self, response: _http.HTTPResponse) -> dict:
        try:
            body = response.json
        except _http_errs.HTTPInvalidResponseError as exc:
            raise _e.APIInvalidResponseError(
                f"Invalid response from API: {exc}",
                response=response,
            ) from None

        if body is None:
            raise _e.APIInvalidResponseError(
                "No JSON response from API",
                response=response,
            )

        try:
            self._validate_response_json(body)
        except _e.APIInvalidResponseError as exc:
            raise _e.APIInvalidResponseError(
                str(exc),
                response=response,
            ) from None

        return body

    def _validate_response_json(self, body: dict) -> None:
        if not body:
            raise _e.APIInvalidResponseError("Empty JSON body")

        if "resultCode" not in body:
            raise _e.APIInvalidResponseError(
                "API response does not contain resultCode",
            )

        try:
            result_code = int(body["resultCode"])
        except (ValueError, TypeError):
            raise _e.APIInvalidResponseError(
                f"Invalid resultCode {body['resultCode']} in response",
            ) from None

        # NOTE: fix the API's inconsistency - it defines int but sends str
        body["resultCode"] = result_code

        if "paymentStatus" not in body:
            return

        # NOTE: fix the API's inconsistency - it defines int but sends str
        try:
            body["paymentStatus"] = int(body["paymentStatus"])
        except (ValueError, TypeError):
            raise _e.APIInvalidResponseError(
                f"Invalid paymentStatus {body['paymentStatus']}",
            ) from None

    def _ensure_signature(self, body: dict) -> None:
        try:
            signature = body["signature"]
        except KeyError:
            raise _e.APIInvalidResponseError(
                "Missing signature in response",
            ) from None

        if not signature:
            raise _e.APIInvalidResponseError("Empty signature")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(merchant_id='{self.merchant_id}')"
