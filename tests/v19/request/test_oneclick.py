"""Tests for the OneClick requests.

Expected sign texts follow the CSOB specification field order listed on
the "Methods for OneClick Payment" wiki page.
"""

from csobpg.v19.models import currency as _currency
from csobpg.v19.models import customer as _customer
from csobpg.v19.models import fingerprint as _fp
from csobpg.v19.models import order as _order
from csobpg.v19.models import payment as _payment
from csobpg.v19.models import webpage as _webpage
from csobpg.v19.request import (
    OneClickPaymentInitRequest,
    OneClickPaymentProcessRequest,
)
from tests.utils import keys as _keys
from tests.utils import metadata as _md
from tests.utils import signature as _sig_util


def test_oneclick_init():
    """Test oneclick/init signing.

    merchantId|origPayId|orderNo|dttm|payMethod|clientIp|totalAmount
    |currency|closePayment|returnUrl|returnMethod|customer|order
    |clientInitiated|sdkUsed|merchantData|language|ttlSec
    """
    request = OneClickPaymentInitRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        template_id="tid",
        order_no="oid",
        return_url="rurl",
        return_method=_payment.ReturnMethod.POST,
        payment_method=_payment.PaymentMethod.CARD,
        client_ip="127.0.0.1",
        total_amount=250,
        currency=_currency.Currency.CZK,
        close_payment=True,
        customer=_md.customer_data(),
        order=_md.order_data(),
        client_initiated=True,
        sdk_used=True,
        merchant_data=_md.MERCHANT_DATA,
        ttl_sec=600,
        language=_webpage.WebPageLanguage.CS,
    )

    assert request.to_sign_text() == (
        f"mid|tid|oid|{request.dttm}|card|127.0.0.1|250|CZK|true|rurl|POST|"
        f"{_md.CUSTOMER_SIGN_TEXT}|{_md.ORDER_SIGN_TEXT}|true|true|"
        f"{_md.MERCHANT_DATA_SIGN_TEXT}|cs|600"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def test_oneclick_process():
    """Test oneclick/process signing.

    merchantId|payId|dttm|fingerprint
    """
    request = OneClickPaymentProcessRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        pay_id="pid",
        fingerprint=_md.fingerprint(),
    )

    assert request.to_sign_text() == (
        f"mid|pid|{request.dttm}|{_md.FINGERPRINT_SIGN_TEXT}"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def test_oneclick_init_new_account():
    """Test oneclick/init signing for a brand new customer account.

    Same specification field order as `test_oneclick_init`. Every
    account counter is legally zero here.
    """
    request = OneClickPaymentInitRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        template_id="tid",
        order_no="oid",
        return_url="rurl",
        return_method=_payment.ReturnMethod.POST,
        payment_method=_payment.PaymentMethod.CARD,
        client_ip="127.0.0.1",
        total_amount=250,
        currency=_currency.Currency.CZK,
        close_payment=True,
        customer=_md.new_account_customer_data(),
        order=_md.order_data(),
        client_initiated=True,
        sdk_used=True,
        merchant_data=_md.MERCHANT_DATA,
        ttl_sec=600,
        language=_webpage.WebPageLanguage.CS,
    )

    assert request.to_sign_text() == (
        f"mid|tid|oid|{request.dttm}|card|127.0.0.1|250|CZK|true|rurl|POST|"
        f"{_md.NEW_ACCOUNT_CUSTOMER_SIGN_TEXT}|{_md.ORDER_SIGN_TEXT}|"
        f"true|true|{_md.MERCHANT_DATA_SIGN_TEXT}|cs|600"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def test_oneclick_process_utc_browser():
    """Test oneclick/process signing for a UTC browser without Java.

    Same specification field order as `test_oneclick_process`. The
    browser timezone is legally zero and `javaEnabled` legally false.
    """
    request = OneClickPaymentProcessRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        pay_id="pid",
        fingerprint=_md.utc_browser_fingerprint(),
    )

    assert request.to_sign_text() == (
        f"mid|pid|{request.dttm}|{_md.UTC_BROWSER_FINGERPRINT_SIGN_TEXT}"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def test_oneclick_init_without_customer_and_order_items():
    """Test an all-unset customer and order being neither signed nor sent.

    Both carry no items, so they contribute neither a value nor a
    delimiter, and no empty object in the body.
    """
    request = OneClickPaymentInitRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        template_id="tid",
        order_no="oid",
        return_url="rurl",
        customer=_customer.CustomerData(),
        order=_order.OrderData(),
    )
    sign_text = request.to_sign_text()
    json_body = request.to_json()

    assert (
        sign_text == f"mid|tid|oid|{request.dttm}|card|rurl|POST|true|false|cs"
    )
    assert "customer" not in json_body
    assert "order" not in json_body
    _sig_util.ensure_text_to_sign_equals_json_body(sign_text, json_body)


def test_oneclick_process_without_fingerprint_items():
    """Test an all-unset fingerprint being neither signed nor sent."""
    request = OneClickPaymentProcessRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        pay_id="pid",
        fingerprint=_fp.Fingerprint(),
    )
    sign_text = request.to_sign_text()
    json_body = request.to_json()

    assert sign_text == f"mid|pid|{request.dttm}"
    assert "fingerprint" not in json_body
    _sig_util.ensure_text_to_sign_equals_json_body(sign_text, json_body)


def test_oneclick_process_unset_sdk_fields_are_not_sent():
    """Test the unset SDK fields not being sent as nulls."""
    request = OneClickPaymentProcessRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        pay_id="pid",
        fingerprint=_fp.Fingerprint(
            sdk=_fp.SDK(
                max_timeout=10,
                reference_number="ref",
                transaction_id="tid",
            ),
        ),
    )
    sign_text = request.to_sign_text()
    json_body = request.to_json()

    assert sign_text == f"mid|pid|{request.dttm}|10|ref|tid"
    assert json_body["fingerprint"] == {
        "sdk": {
            "maxTimeout": 10,
            "referenceNumber": "ref",
            "transID": "tid",
        },
    }
    _sig_util.ensure_text_to_sign_equals_json_body(sign_text, json_body)
