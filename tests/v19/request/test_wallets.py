"""Tests for the Apple Pay and Google Pay requests.

Expected sign texts follow the CSOB specification field order listed on
the "Methods for Apple Pay" and "Methods for Google Pay" wiki pages.
"""

from csobpg.v19.models import currency as _currency
from csobpg.v19.models import customer as _customer
from csobpg.v19.models import order as _order
from csobpg.v19.models import payment as _payment
from csobpg.v19.models import webpage as _webpage
from csobpg.v19.request import (
    ApplePayPaymentInitRequest,
    ApplePayPaymentProcessRequest,
    GooglePayPaymentInitRequest,
    GooglePayPaymentProcessRequest,
)
from tests.utils import keys as _keys
from tests.utils import metadata as _md
from tests.utils import signature as _sig_util

_PAYLOAD = {"data": "d"}
_PAYLOAD_SIGN_TEXT = "eyJkYXRhIjogImQifQ=="


def _assert_wallet_init(request):
    """Assert a wallet init request signing.

    merchantId|orderNo|dttm|clientIp|totalAmount|currency|closePayment
    |payload|returnUrl|returnMethod|customer|order|sdkUsed|merchantData
    |language|ttlSec
    """
    assert request.to_sign_text() == (
        f"mid|oid|{request.dttm}|127.0.0.1|250|CZK|true|"
        f"{_PAYLOAD_SIGN_TEXT}|rurl|POST|"
        f"{_md.CUSTOMER_SIGN_TEXT}|{_md.ORDER_SIGN_TEXT}|true|"
        f"{_md.MERCHANT_DATA_SIGN_TEXT}|cs|600"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def _assert_wallet_process(request):
    """Assert a wallet process request signing.

    merchantId|payId|dttm|fingerprint
    """
    assert request.to_sign_text() == (
        f"mid|pid|{request.dttm}|{_md.FINGERPRINT_SIGN_TEXT}"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def test_applepay_init():
    """Test applepay/init signing."""
    _assert_wallet_init(
        ApplePayPaymentInitRequest(
            merchant_id="mid",
            private_key=_keys.PRIVATE_KEY,
            order_no="oid",
            client_ip="127.0.0.1",
            total_amount=250,
            payload=_PAYLOAD,
            return_url="rurl",
            return_method=_payment.ReturnMethod.POST,
            currency=_currency.Currency.CZK,
            close_payment=True,
            customer=_md.customer_data(),
            order=_md.order_data(),
            sdk_used=True,
            merchant_data=_md.MERCHANT_DATA,
            language=_webpage.WebPageLanguage.CS,
            ttl_sec=600,
        ),
    )


def test_googlepay_init():
    """Test googlepay/init signing."""
    _assert_wallet_init(
        GooglePayPaymentInitRequest(
            merchant_id="mid",
            private_key=_keys.PRIVATE_KEY,
            order_no="oid",
            client_ip="127.0.0.1",
            total_amount=250,
            payload=_PAYLOAD,
            return_url="rurl",
            return_method=_payment.ReturnMethod.POST,
            currency=_currency.Currency.CZK,
            close_payment=True,
            customer=_md.customer_data(),
            order=_md.order_data(),
            sdk_used=True,
            merchant_data=_md.MERCHANT_DATA,
            language=_webpage.WebPageLanguage.CS,
            ttl_sec=600,
        ),
    )


def test_applepay_process():
    """Test applepay/process signing."""
    _assert_wallet_process(
        ApplePayPaymentProcessRequest(
            merchant_id="mid",
            private_key=_keys.PRIVATE_KEY,
            pay_id="pid",
            fingerprint=_md.fingerprint(),
        ),
    )


def test_googlepay_process():
    """Test googlepay/process signing."""
    _assert_wallet_process(
        GooglePayPaymentProcessRequest(
            merchant_id="mid",
            private_key=_keys.PRIVATE_KEY,
            pay_id="pid",
            fingerprint=_md.fingerprint(),
        ),
    )


def _assert_wallet_init_without_customer_and_order(request):
    """Assert a wallet init request without customer and order items.

    Both carry no items, so they contribute neither a value nor a
    delimiter, and no empty object in the body.
    """
    sign_text = request.to_sign_text()
    json_body = request.to_json()

    assert sign_text == (
        f"mid|oid|{request.dttm}|127.0.0.1|250|CZK|"
        f"{_PAYLOAD_SIGN_TEXT}|rurl|POST|false|cs"
    )
    assert "customer" not in json_body
    assert "order" not in json_body
    _sig_util.ensure_text_to_sign_equals_json_body(sign_text, json_body)


def test_applepay_init_without_customer_and_order_items():
    """Test applepay/init signing without customer and order items."""
    _assert_wallet_init_without_customer_and_order(
        ApplePayPaymentInitRequest(
            merchant_id="mid",
            private_key=_keys.PRIVATE_KEY,
            order_no="oid",
            client_ip="127.0.0.1",
            total_amount=250,
            payload=_PAYLOAD,
            return_url="rurl",
            customer=_customer.CustomerData(),
            order=_order.OrderData(),
        ),
    )


def test_googlepay_init_without_customer_and_order_items():
    """Test googlepay/init signing without customer and order items."""
    _assert_wallet_init_without_customer_and_order(
        GooglePayPaymentInitRequest(
            merchant_id="mid",
            private_key=_keys.PRIVATE_KEY,
            order_no="oid",
            client_ip="127.0.0.1",
            total_amount=250,
            payload=_PAYLOAD,
            return_url="rurl",
            customer=_customer.CustomerData(),
            order=_order.OrderData(),
        ),
    )
