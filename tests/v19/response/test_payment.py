"""Tests for the payment responses.

Expected sign texts follow the CSOB specification field order listed on
the "Basic methods" wiki page.
"""

import pytest

from csobpg.v19 import errors as _e
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

_RESPONSES = [
    PaymentInitResponse,
    PaymentProcessResponse,
    PaymentStatusResponse,
    PaymentCloseResponse,
    PaymentRefundResponse,
    PaymentReverseResponse,
]


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


@pytest.mark.parametrize("actions", [{}, {"actions": None}])
def test_payment_status_no_actions(actions):
    """Test payment/status response carrying no actions.

    `actions` is optional, and the API may either omit the key or send
    it as an explicit `null`. Both mean the same thing, and neither
    contributes anything to the signature.
    """
    body = {
        "payId": "pid",
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "paymentStatus": 4,
        "authCode": "ac",
        "statusDetail": "sd",
        **actions,
        "signature": "fake_s",
    }
    response = _resp_util.build_response(PaymentStatusResponse, body)

    assert response.actions is None
    assert response.to_sign_text() == f"pid|{_DTTM}|0|OK|4|ac|sd"


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


@pytest.mark.parametrize("response_cls", _RESPONSES)
def test_falsy_payment_status(response_cls):
    """Test a payment response carrying a falsy `paymentStatus`.

    A `paymentStatus` the API sent is part of the text the gateway
    signed, so dropping it from the text we rebuild can only fail the
    verification. Presence must therefore be decided by the value being
    `null`, not by it being falsy. `0` is not a status the API defines,
    so it has to surface as an invalid response instead of quietly
    turning into "no status".
    """
    body = {
        "payId": "pid",
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "paymentStatus": 0,
        "signature": "fake_s",
    }

    with pytest.raises(_e.APIInvalidResponseError, match="paymentStatus"):
        _resp_util.build_response(response_cls, body)


@pytest.mark.parametrize("response_cls", _RESPONSES)
@pytest.mark.parametrize("payment_status", [{}, {"paymentStatus": None}])
def test_no_payment_status(response_cls, payment_status):
    """Test a payment response carrying no `paymentStatus`.

    `paymentStatus` is optional, and the API may either omit the key or
    send it as an explicit `null`. Both mean the same thing, and neither
    contributes anything to the signature.
    """
    body = {
        "payId": "pid",
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        **payment_status,
        "signature": "fake_s",
    }
    response = _resp_util.build_response(response_cls, body)

    assert response.payment_status is None
    assert response.to_sign_text() == f"pid|{_DTTM}|0|OK"
