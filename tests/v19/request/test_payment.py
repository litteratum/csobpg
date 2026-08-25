"""Tests for the payment requests.

Expected sign texts follow the CSOB specification field order listed on
the "Basic methods" wiki page.
"""

from csobpg.v19.request import (
    PaymentCloseRequest,
    PaymentProcessRequest,
    PaymentRefundRequest,
    PaymentReverseRequest,
    PaymentStatusRequest,
)
from tests.utils import keys as _keys
from tests.utils import signature as _sig_util


def test_payment_close():
    """Test payment/close signing: merchantId|payId|dttm|totalAmount."""
    request = PaymentCloseRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        pay_id="pid",
        total_amount=250,
    )

    assert request.to_sign_text() == f"mid|pid|{request.dttm}|250"
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def test_payment_refund():
    """Test payment/refund signing: merchantId|payId|dttm|amount."""
    request = PaymentRefundRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        pay_id="pid",
        amount=250,
    )

    assert request.to_sign_text() == f"mid|pid|{request.dttm}|250"
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def test_payment_reverse():
    """Test payment/reverse signing: merchantId|payId|dttm."""
    request = PaymentReverseRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        pay_id="pid",
    )

    assert request.to_sign_text() == f"mid|pid|{request.dttm}"
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def test_payment_process():
    """Test payment/process signing: merchantId|payId|dttm."""
    request = PaymentProcessRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        pay_id="pid",
    )

    assert request.to_sign_text() == f"mid|pid|{request.dttm}"
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def test_payment_status():
    """Test payment/status signing: merchantId|payId|dttm."""
    request = PaymentStatusRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        pay_id="pid",
    )

    assert request.to_sign_text() == f"mid|pid|{request.dttm}"
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )
