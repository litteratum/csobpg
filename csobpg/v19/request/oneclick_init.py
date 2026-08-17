"""OnceClick payment init request."""

from __future__ import annotations

from csobpg.v19.models import currency as _currency
from csobpg.v19.models import customer as _customer
from csobpg.v19.models import order as _order
from csobpg.v19.models import payment as _payment
from csobpg.v19.models import webpage as _webpage

from .base import BaseRequest
from .merchant import pack_merchant_data


class OneClickPaymentInitRequest(BaseRequest):
    """OneClick payment init request."""

    def __init__(
        self,
        merchant_id: str,
        private_key: str,
        template_id: str,
        order_no: str,
        return_url: str,
        return_method: _payment.ReturnMethod = _payment.ReturnMethod.POST,
        payment_method: _payment.PaymentMethod = _payment.PaymentMethod.CARD,
        client_ip: str | None = None,
        total_amount: int | None = None,
        currency: _currency.Currency | None = None,
        close_payment: bool | None = None,
        customer: _customer.CustomerData | None = None,
        order: _order.OrderData | None = None,
        client_initiated: bool = True,
        sdk_used: bool = False,
        merchant_data: bytes | None = None,
        ttl_sec: int | None = None,
        language: _webpage.WebPageLanguage = _webpage.WebPageLanguage.CS,
    ) -> None:
        super().__init__("oneclick/init", merchant_id, private_key)
        self.template_id = template_id
        self.order_no = order_no
        self.return_url = return_url
        self.return_method = return_method
        self.payment_method = payment_method
        self.client_ip = client_ip
        self.total_amount = total_amount
        self.currency = currency
        self.close_payment = close_payment
        self.customer = customer
        self.order = order
        self.client_initiated = client_initiated
        self.sdk_used = sdk_used
        self.merchant_data = (
            pack_merchant_data(merchant_data) if merchant_data else None
        )
        self.ttl_sec = ttl_sec
        self.language = language

    def _get_params_sequence(self) -> tuple:
        return (
            self.merchant_id,
            self.template_id,
            self.order_no,
            self.dttm,
            self.payment_method,
            self.client_ip,
            self.total_amount,
            self.currency,
            self.close_payment,
            self.return_url,
            self.return_method,
            self.customer,
            self.order,
            self.client_initiated,
            self.sdk_used,
            self.merchant_data,
            self.language,
            self.ttl_sec,
        )

    def _as_json(self) -> dict:
        result = {
            "origPayId": self.template_id,
            "orderNo": self.order_no,
            "payMethod": self.payment_method.value,
            "clientIp": self.client_ip,
            "totalAmount": self.total_amount,
            "closePayment": self.close_payment,
            "returnUrl": self.return_url,
            "returnMethod": self.return_method.value,
            "clientInitiated": self.client_initiated,
            "sdkUsed": self.sdk_used,
            "merchantData": self.merchant_data,
            "language": self.language.value,
            "ttlSec": self.ttl_sec,
        }

        if self.currency:
            result["currency"] = self.currency.value
        if self.customer:
            result["customer"] = self.customer.as_json()
        if self.order:
            result["order"] = self.order.as_json()

        return result
