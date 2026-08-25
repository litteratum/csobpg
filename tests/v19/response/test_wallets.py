"""Tests for the OneClick, Apple Pay and Google Pay payment responses.

All six responses share one specification field order:

    payId|dttm|resultCode|resultMessage|paymentStatus|statusDetail
    |actions

listed on the "Methods for OneClick Payment", "Methods for Apple Pay"
and "Methods for Google Pay" wiki pages.
"""

import pytest

from csobpg.v19 import errors as _e
from csobpg.v19.response import (
    ApplePayPaymentInitResponse,
    ApplePayPaymentProcessResponse,
    GooglePayPaymentInitResponse,
    GooglePayPaymentProcessResponse,
    OneClickPaymentInitResponse,
    OneClickPaymentProcessResponse,
)
from tests.utils import metadata as _md
from tests.utils import response as _resp_util
from tests.utils import signature as _sig_util

_DTTM = "20240101120000"

_RESPONSES = [
    OneClickPaymentInitResponse,
    OneClickPaymentProcessResponse,
    ApplePayPaymentInitResponse,
    ApplePayPaymentProcessResponse,
    GooglePayPaymentInitResponse,
    GooglePayPaymentProcessResponse,
]


@pytest.mark.parametrize("response_cls", _RESPONSES)
def test_to_sign_text(response_cls):
    """Test wallet init and process responses signing."""
    body = {
        "payId": "pid",
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "paymentStatus": 4,
        "statusDetail": "sd",
        "actions": _md.ACTIONS_JSON,
        "signature": "fake_s",
    }
    response = _resp_util.build_response(response_cls, body)

    assert response.to_sign_text() == (
        f"pid|{_DTTM}|0|OK|4|sd|{_md.ACTIONS_SIGN_TEXT}"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(
        response.to_sign_text(),
        body,
    )


@pytest.mark.parametrize("response_cls", _RESPONSES)
@pytest.mark.parametrize("actions", [{}, {"actions": None}])
def test_no_actions(response_cls, actions):
    """Test wallet responses carrying no actions.

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
        "statusDetail": "sd",
        **actions,
        "signature": "fake_s",
    }
    response = _resp_util.build_response(response_cls, body)

    assert response.actions is None
    assert response.to_sign_text() == f"pid|{_DTTM}|0|OK|4|sd"


@pytest.mark.parametrize("response_cls", _RESPONSES)
def test_falsy_payment_status(response_cls):
    """Test a wallet response carrying a falsy `paymentStatus`.

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
    """Test a wallet response carrying no `paymentStatus`.

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
