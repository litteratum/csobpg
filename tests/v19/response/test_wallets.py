"""Tests for the OneClick, Apple Pay and Google Pay payment responses.

All six responses share one specification field order:

    payId|dttm|resultCode|resultMessage|paymentStatus|statusDetail
    |actions

listed on the "Methods for OneClick Payment", "Methods for Apple Pay"
and "Methods for Google Pay" wiki pages.
"""

import pytest

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


@pytest.mark.parametrize(
    "response_cls",
    [
        OneClickPaymentInitResponse,
        OneClickPaymentProcessResponse,
        ApplePayPaymentInitResponse,
        ApplePayPaymentProcessResponse,
        GooglePayPaymentInitResponse,
        GooglePayPaymentProcessResponse,
    ],
)
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
