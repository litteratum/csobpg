"""Tests for the payment responses.

Expected sign texts follow the CSOB specification field order listed on
the "Basic methods" wiki page.
"""

from csobpg.v19.response import (
    PaymentCloseResponse,
    PaymentInitResponse,
    PaymentProcessResponse,
    PaymentRefundResponse,
    PaymentReverseResponse,
    PaymentStatusResponse,
)
from tests.utils import metadata as _md
from tests.utils import response as _resp_util
from tests.utils import signature as _sig_util

_DTTM = "20240101120000"


def test_payment_init():
    """Test payment/init response signing.

    payId|dttm|resultCode|resultMessage|paymentStatus|customerCode
    |statusDetail
    """
    body = {
        "payId": "pid",
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "paymentStatus": 1,
        "customerCode": "cc",
        "statusDetail": "sd",
        "signature": "fake_s",
    }
    response = _resp_util.build_response(PaymentInitResponse, body)

    assert response.to_sign_text() == f"pid|{_DTTM}|0|OK|1|cc|sd"
    _sig_util.ensure_text_to_sign_equals_json_body(
        response.to_sign_text(),
        body,
    )


def test_payment_process():
    """Test payment/process response signing.

    payId|dttm|resultCode|resultMessage|paymentStatus|authCode
    |merchantData|statusDetail
    """
    body = {
        "payId": "pid",
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "paymentStatus": 7,
        "authCode": "ac",
        "merchantData": _md.MERCHANT_DATA_SIGN_TEXT,
        "statusDetail": "sd",
        "signature": "fake_s",
    }
    response = _resp_util.build_response(PaymentProcessResponse, body)

    assert response.to_sign_text() == (
        f"pid|{_DTTM}|0|OK|7|ac|{_md.MERCHANT_DATA_SIGN_TEXT}|sd"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(
        response.to_sign_text(),
        body,
    )


def test_payment_status():
    """Test payment/status response signing.

    payId|dttm|resultCode|resultMessage|paymentStatus|authCode
    |statusDetail|actions
    """
    body = {
        "payId": "pid",
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "paymentStatus": 4,
        "authCode": "ac",
        "statusDetail": "sd",
        "actions": _md.ACTIONS_JSON,
        "signature": "fake_s",
    }
    response = _resp_util.build_response(PaymentStatusResponse, body)

    assert response.to_sign_text() == (
        f"pid|{_DTTM}|0|OK|4|ac|sd|{_md.ACTIONS_SIGN_TEXT}"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(
        response.to_sign_text(),
        body,
    )


def test_payment_close():
    """Test payment/close response signing.

    payId|dttm|resultCode|resultMessage|paymentStatus|authCode
    |statusDetail
    """
    body = {
        "payId": "pid",
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "paymentStatus": 8,
        "authCode": "ac",
        "statusDetail": "sd",
        "signature": "fake_s",
    }
    response = _resp_util.build_response(PaymentCloseResponse, body)

    assert response.to_sign_text() == f"pid|{_DTTM}|0|OK|8|ac|sd"
    _sig_util.ensure_text_to_sign_equals_json_body(
        response.to_sign_text(),
        body,
    )


def test_payment_refund():
    """Test payment/refund response signing.

    payId|dttm|resultCode|resultMessage|paymentStatus|authCode
    |statusDetail
    """
    body = {
        "payId": "pid",
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "paymentStatus": 10,
        "authCode": "ac",
        "statusDetail": "sd",
        "signature": "fake_s",
    }
    response = _resp_util.build_response(PaymentRefundResponse, body)

    assert response.to_sign_text() == f"pid|{_DTTM}|0|OK|10|ac|sd"
    _sig_util.ensure_text_to_sign_equals_json_body(
        response.to_sign_text(),
        body,
    )


def test_payment_reverse():
    """Test payment/reverse response signing.

    payId|dttm|resultCode|resultMessage|paymentStatus|statusDetail
    """
    body = {
        "payId": "pid",
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "paymentStatus": 5,
        "statusDetail": "sd",
        "signature": "fake_s",
    }
    response = _resp_util.build_response(PaymentReverseResponse, body)

    assert response.to_sign_text() == f"pid|{_DTTM}|0|OK|5|sd"
    _sig_util.ensure_text_to_sign_equals_json_body(
        response.to_sign_text(),
        body,
    )
