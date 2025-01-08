"""Payment init request package."""

from typing import Optional

from csobpg.v19.models import cart as _cart
from csobpg.v19.models import currency as _currency
from csobpg.v19.models import customer as _customer
from csobpg.v19.models import order as _order
from csobpg.v19.models import payment as _payment
from csobpg.v19.models import webpage as _webpage

from .base import BaseRequest
from .dttm import get_payment_expiry
from .merchant import pack_merchant_data


class PaymentInitRequest(BaseRequest):
    """Payment init request."""

    def __init__(
        self,
        merchant_id: str,
        private_key: str,
        order_no: str,
        total_amount: int,
        return_url: str,
        return_method: _payment.ReturnMethod = _payment.ReturnMethod.POST,
        payment_operation: _payment.PaymentOperation = _payment.PaymentOperation.PAYMENT,
        payment_method: _payment.PaymentMethod = _payment.PaymentMethod.CARD,
        currency: _currency.Currency = _currency.Currency.CZK,
        close_payment: bool = True,
        ttl_sec: int = 600,
        cart: Optional[_cart.Cart] = None,
        customer: Optional[_customer.CustomerData] = None,
        order: Optional[_order.OrderData] = None,
        merchant_data: Optional[bytes] = None,
        customer_id: Optional[str] = None,
        payment_expiry: Optional[int] = None,
        page_appearance: _webpage.WebPageAppearanceConfig = _webpage.WebPageAppearanceConfig(),
    ) -> None:
        # pylint:disable=too-many-locals
        super().__init__("payment/init", merchant_id, private_key)

        if not 300 <= ttl_sec <= 1800:
            raise ValueError('"ttl_sec" must be in [300, 1800]')
        if len(order_no) > 10:
            raise ValueError('"order_no" must be up to 10 chars')
        if len(return_url) > 300:
            raise ValueError('"return_url" must be up to 300 chars')
        if customer_id and len(customer_id) > 50:
            raise ValueError('"customer_id" must be up to 50 chars')
        if total_amount <= 0:
            raise ValueError('"total_amount" must be > 0')

        cart = cart or _cart.Cart([_cart.CartItem("Payment", 1, total_amount)])

        if cart.total_amount != total_amount:
            raise ValueError(
                "Cart's total amount does not match the requested total amount"
            )

        self.order_no = order_no
        self.total_amount = total_amount
        self.return_url = return_url
        self.return_method = return_method
        self.payment_operation = payment_operation
        self.payment_method = payment_method
        self.currency = currency
        self.close_payment = close_payment
        self.ttl_sec = ttl_sec
        self.cart = cart
        self.customer = customer
        self.order = order
        self.merchant_data = (
            pack_merchant_data(merchant_data) if merchant_data else None
        )
        self.customer_id = customer_id
        self.payment_expiry = get_payment_expiry(payment_expiry)
        self.page_appearance = page_appearance

    def _get_params_sequence(self) -> tuple:
        return (
            self.merchant_id,
            self.order_no,
            self.dttm,
            self.payment_operation,
            self.payment_method,
            self.total_amount,
            self.currency,
            self.close_payment,
            self.return_url,
            self.return_method,
            self.cart,
            self.customer,
            self.order,
            self.merchant_data,
            self.customer_id,
            self.page_appearance.language,
            self.ttl_sec,
            self.page_appearance.logo_version,
            self.page_appearance.color_scheme_version,
            self.payment_expiry,
        )

    def _as_json(self) -> dict:
        return {
            "orderNo": self.order_no,
            "totalAmount": self.total_amount,
            "returnUrl": self.return_url,
            "returnMethod": self.return_method.value,
            "payOperation": self.payment_operation.value,
            "payMethod": self.payment_method.value,
            "closePayment": self.close_payment,
            "currency": self.currency.value,
            "ttlSec": self.ttl_sec,
            "cart": self.cart.as_json(),
            "customer": self.customer.as_json() if self.customer else None,
            "order": self.order.as_json() if self.order else None,
            "merchantData": self.merchant_data,
            "customerId": self.customer_id,
            "language": self.page_appearance.language.value,
            "logoVersion": self.page_appearance.logo_version,
            "colorSchemeVersion": self.page_appearance.color_scheme_version,
            "customExpiry": self.payment_expiry,
        }
