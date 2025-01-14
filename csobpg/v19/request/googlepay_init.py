"""Google Pay init request module."""

import json as jsonlib
from base64 import b64encode
from typing import Optional

from csobpg.v19.models import currency as _currency
from csobpg.v19.models import customer as _customer
from csobpg.v19.models import order as _order
from csobpg.v19.models import payment as _payment
from csobpg.v19.models import webpage as _webpage

from .base import BaseRequest
from .merchant import pack_merchant_data


class GooglePayPaymentInitRequest(BaseRequest):
    """Google Pay payment init request."""

    def __init__(
        self,
        merchant_id: str,
        private_key: str,
        order_no: str,
        client_ip: str,
        total_amount: int,
        payload: dict,
        return_url: str,
        return_method: _payment.ReturnMethod = _payment.ReturnMethod.POST,
        currency: _currency.Currency = _currency.Currency.CZK,
        close_payment: Optional[bool] = None,
        customer: Optional[_customer.CustomerData] = None,
        order: Optional[_order.OrderData] = None,
        sdk_used: bool = False,
        merchant_data: Optional[bytes] = None,
        language: _webpage.WebPageLanguage = _webpage.WebPageLanguage.CS,
        ttl_sec: Optional[int] = None,
    ) -> None:
        # pylint:disable=too-many-locals
        super().__init__("googlepay/init", merchant_id, private_key)

        if ttl_sec is not None and not 300 <= ttl_sec <= 1800:
            raise ValueError('"ttl_sec" must be in [300, 1800]')
        if len(order_no) > 10:
            raise ValueError('"order_no" must be up to 10 chars')
        if len(return_url) > 300:
            raise ValueError('"return_url" must be up to 300 chars')
        if total_amount <= 0:
            raise ValueError('"total_amount" must be > 0')

        self.order_no = order_no
        self.client_ip = client_ip
        self.total_amount = total_amount
        self.payload = b64encode(
            jsonlib.dumps(payload).encode("UTF-8")
        ).decode("UTF-8")
        self.return_url = return_url
        self.return_method = return_method
        self.currency = currency
        self.close_payment = close_payment
        self.customer = customer
        self.order = order
        self.sdk_used = sdk_used
        self.merchant_data = (
            pack_merchant_data(merchant_data) if merchant_data else None
        )
        self.language = language
        self.ttl_sec = ttl_sec

    def _get_params_sequence(self) -> tuple:
        return (
            self.merchant_id,
            self.order_no,
            self.dttm,
            self.client_ip,
            self.total_amount,
            self.currency,
            self.close_payment,
            self.payload,
            self.return_url,
            self.return_method,
            self.customer,
            self.order,
            self.sdk_used,
            self.merchant_data,
            self.language,
            self.ttl_sec,
        )

    def _as_json(self) -> dict:
        return {
            "orderNo": self.order_no,
            "clientIp": self.client_ip,
            "totalAmount": self.total_amount,
            "currency": self.currency.value,
            "closePayment": self.close_payment,
            "payload": self.payload,
            "returnUrl": self.return_url,
            "returnMethod": self.return_method.value,
            "customer": self.customer.as_json() if self.customer else None,
            "order": self.order.as_json() if self.order else None,
            "sdkUsed": self.sdk_used,
            "merchantData": self.merchant_data,
            "language": self.language.value,
            "ttlSec": self.ttl_sec,
        }
