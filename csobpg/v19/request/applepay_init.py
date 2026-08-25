"""Apple Pay init request module."""

from __future__ import annotations

import json as jsonlib
from base64 import b64encode

from csobpg.v19.models import currency as _currency
from csobpg.v19.models import customer as _customer
from csobpg.v19.models import order as _order
from csobpg.v19.models import payment as _payment
from csobpg.v19.models import webpage as _webpage

from .base import BaseRequest
from .merchant import pack_merchant_data


class ApplePayPaymentInitRequest(BaseRequest):
    """Apple Pay payment init request."""

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
        close_payment: bool | None = None,
        customer: _customer.CustomerData | None = None,
        order: _order.OrderData | None = None,
        sdk_used: bool = False,
        merchant_data: bytes | None = None,
        language: _webpage.WebPageLanguage = _webpage.WebPageLanguage.CS,
        ttl_sec: int | None = None,
    ) -> None:
        super().__init__("applepay/init", merchant_id, private_key)

        self.order_no = order_no
        self.client_ip = client_ip
        self.total_amount = total_amount
        self.payload = b64encode(
            jsonlib.dumps(payload).encode("UTF-8"),
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
