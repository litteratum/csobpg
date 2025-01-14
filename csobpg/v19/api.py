"""API client."""

import logging
from typing import Optional, Union

from httprest import API
from httprest.http import HTTPClient

from csobpg.v19.models.cart import Cart
from csobpg.v19.models.currency import Currency
from csobpg.v19.models.customer import CustomerData
from csobpg.v19.models.fingerprint import Fingerprint
from csobpg.v19.models.order import OrderData
from csobpg.v19.models.payment import (
    PaymentMethod,
    PaymentOperation,
    ReturnMethod,
)
from csobpg.v19.models.webpage import WebPageAppearanceConfig, WebPageLanguage

from . import request as _request
from . import response as _response
from .key import FileRSAKey, RAMRSAKey, RSAKey


class APIClient(API):
    """API client."""

    def __init__(
        self,
        merchant_id: str,
        private_key: Union[str, RSAKey],
        public_key: Union[str, RSAKey],
        base_url: str = "https://api.platebnibrana.csob.cz/api/v1.9",
        http_client: Optional[HTTPClient] = None,
    ) -> None:
        # pylint:disable=too-many-arguments
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
        cart: Optional[Cart] = None,
        customer: Optional[CustomerData] = None,
        order: Optional[OrderData] = None,
        merchant_data: Optional[bytes] = None,
        customer_id: Optional[str] = None,
        payment_expiry: Optional[int] = None,
        # pylint:disable=line-too-long, too-many-locals
        page_appearance: WebPageAppearanceConfig = WebPageAppearanceConfig(),
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
        )  # type: ignore

    def oneclick_init_payment(
        # pylint:disable=line-too-long, too-many-locals
        self,
        template_id: str,
        order_no: str,
        return_url: str,
        return_method: ReturnMethod = ReturnMethod.POST,
        payment_method: PaymentMethod = PaymentMethod.CARD,
        client_ip: Optional[str] = None,
        total_amount: Optional[int] = None,
        currency: Optional[Currency] = None,
        close_payment: Optional[bool] = None,
        customer: Optional[CustomerData] = None,
        order: Optional[OrderData] = None,
        client_initiated: bool = True,
        sdk_used: bool = False,
        merchant_data: Optional[bytes] = None,
        ttl_sec: Optional[int] = None,
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

        if total_amount is not None and currency is None:
            raise ValueError(
                "currency must be specified if total_amount is set"
            )
        if currency is not None and total_amount is None:
            raise ValueError(
                "total_amount must be specified if currency is set"
            )
        if client_initiated and not client_ip:
            raise ValueError("client_ip must be specified if client_initiated")

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
        )  # type: ignore

    def oneclick_process(
        self, pay_id: str, fingerprint: Optional[Fingerprint] = None
    ) -> _response.OneClickPaymentProcessResponse:
        """Start OneClick payment processing."""
        self._log.info(
            "Starting OneClick payment processing for pay_id=%s", pay_id
        )
        request = _request.OneClickPaymentProcessRequest(
            self.merchant_id, str(self.private_key), pay_id, fingerprint
        )
        return _response.OneClickPaymentProcessResponse.from_json(
            self._call_api("post", request.endpoint, request.to_json()),
            str(self.public_key),
        )  # type: ignore

    def oneclick_echo(
        self, template_id: str
    ) -> _response.OneClickEchoResponse:
        """Make an OneClick echo request."""
        self._log.info('OneClick echo request for "%s"', template_id)
        request = _request.OneClickEchoRequest(
            self.merchant_id, str(self.private_key), template_id
        )
        return _response.OneClickEchoResponse.from_json(
            self._call_api("post", request.endpoint, request.to_json()),
            str(self.public_key),
        )  # type: ignore

    def get_payment_status(
        self, pay_id: str
    ) -> _response.PaymentStatusResponse:
        """Request payment status information."""
        self._log.info("Requesting payment status for pay_id=%s", pay_id)
        request = _request.PaymentStatusRequest(
            self.merchant_id, str(self.private_key), pay_id
        )
        return _response.PaymentStatusResponse.from_json(
            self._call_api("get", request.endpoint), str(self.public_key)
        )  # type: ignore

    def reverse_payment(self, pay_id: str) -> _response.PaymentReverseResponse:
        """Reverse payment.

        :param pay_id: payment ID
        """
        self._log.info("Reversing payment for pay_id=%s", pay_id)
        request = _request.PaymentReverseRequest(
            self.merchant_id, str(self.private_key), pay_id
        )
        return _response.PaymentReverseResponse.from_json(
            self._call_api("put", request.endpoint, request.to_json()),
            str(self.public_key),
        )  # type: ignore

    def close_payment(
        self, pay_id: str, total_amount: Optional[int] = None
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
            self.merchant_id, str(self.private_key), pay_id, total_amount
        )
        return _response.PaymentCloseResponse.from_json(
            self._call_api("put", request.endpoint, json=request.to_json()),
            str(self.public_key),
        )  # type: ignore

    def refund_payment(
        self, pay_id: str, amount: Optional[int] = None
    ) -> _response.PaymentRefundResponse:
        """Refund payment.

        :param pay_id: payment ID
        :param amount: amount to refund. It must be less or equal to the
          original amount and provided in hundredths of the base currency.
          If not provided, the full amount will be refunded.
        """
        self._log.info(
            "Refunding payment for pay_id=%s, amount=%s", pay_id, amount
        )
        request = _request.PaymentRefundRequest(
            self.merchant_id, str(self.private_key), pay_id, amount
        )
        return _response.PaymentRefundResponse.from_json(
            self._call_api("put", request.endpoint, request.to_json()),
            str(self.public_key),
        )  # type: ignore

    def get_payment_process_url(self, pay_id: str) -> str:
        """Build payment URL.

        :param pay_id: pay_id obtained from `payment_init`
        :return: url to process payment
        """
        self._log.info("Building payment URL for pay_id=%s", pay_id)
        return self._build_url(
            _request.PaymentProcessRequest(
                self.merchant_id, str(self.private_key), pay_id
            ).endpoint
        )

    def echo(self) -> None:
        """Make an echo request."""
        self._log.info("Making echo request")
        request = _request.EchoRequest(self.merchant_id, str(self.private_key))
        self._call_api("post", request.endpoint, request.to_json())

    def process_gateway_return(
        self, datadict: dict
    ) -> _response.PaymentProcessResponse:
        """Process gateway return."""
        self._log.info("Processing gateway return %s", datadict)
        data = {}

        for key in datadict:
            data[key] = (
                int(datadict[key])
                if key in ("paymentStatus",)
                else datadict[key]
            )

        return _response.PaymentProcessResponse.from_json(
            data, str(self.public_key)
        )  # type: ignore

    def googlepay_echo(self) -> _response.GooglePayEchoResponse:
        """Make a Google Pay echo request."""
        self._log.info("Making Google Pay echo request")
        request = _request.GooglePayEchoRequest(
            self.merchant_id, str(self.private_key)
        )
        return _response.GooglePayEchoResponse.from_json(
            self._call_api("post", request.endpoint, request.to_json()),
            str(self.public_key),
        )  # type: ignore

    def googlepay_init(
        # pylint:disable=too-many-locals
        self,
        order_no: str,
        client_ip: str,
        total_amount: int,
        payload: dict,
        return_url: str,
        return_method: ReturnMethod = ReturnMethod.POST,
        currency: Currency = Currency.CZK,
        close_payment: Optional[bool] = None,
        customer: Optional[CustomerData] = None,
        order: Optional[OrderData] = None,
        sdk_used: bool = False,
        merchant_data: Optional[bytes] = None,
        language: WebPageLanguage = WebPageLanguage.CS,
        ttl_sec: Optional[int] = None,
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
        )  # type: ignore

    def googlepay_process(
        self, pay_id: str, fingerprint: Fingerprint
    ) -> _response.OneClickPaymentProcessResponse:
        """Start Google Pay payment processing."""
        self._log.info(
            "Starting Google Pay payment processing for pay_id=%s", pay_id
        )
        request = _request.GooglePayPaymentProcessRequest(
            self.merchant_id, str(self.private_key), pay_id, fingerprint
        )
        return _response.GooglePayPaymentProcessResponse.from_json(
            self._call_api("post", request.endpoint, request.to_json()),
            str(self.public_key),
        )  # type: ignore

    def _call_api(
        self, method: str, endpoint: str, json: Optional[dict] = None
    ) -> dict:
        return self._request(method, endpoint, json).json or {}

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(merchant_id='{self.merchant_id}')"
