"""Tests for the echo requests.

Expected sign texts follow the CSOB specification field order:

* echo: "Basic methods" wiki page
* applepay/echo: "Methods for Apple Pay" wiki page
* googlepay/echo: "Methods for Google Pay" wiki page
* oneclick/echo: "Methods for OneClick Payment" wiki page
"""

from csobpg.v19.request import (
    ApplePayEchoRequest,
    EchoRequest,
    GooglePayEchoRequest,
    OneClickEchoRequest,
)
from tests.utils import keys as _keys
from tests.utils import signature as _sig_util


def test_echo():
    """Test echo request signing: merchantId|dttm."""
    request = EchoRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
    )

    assert request.to_sign_text() == f"mid|{request.dttm}"
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def test_applepay_echo():
    """Test applepay/echo request signing: merchantId|dttm."""
    request = ApplePayEchoRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
    )

    assert request.to_sign_text() == f"mid|{request.dttm}"
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def test_googlepay_echo():
    """Test googlepay/echo request signing: merchantId|dttm."""
    request = GooglePayEchoRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
    )

    assert request.to_sign_text() == f"mid|{request.dttm}"
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )


def test_oneclick_echo():
    """Test oneclick/echo request signing: merchantId|origPayId|dttm."""
    request = OneClickEchoRequest(
        merchant_id="mid",
        private_key=_keys.PRIVATE_KEY,
        template_id="tid",
    )

    assert request.to_sign_text() == f"mid|tid|{request.dttm}"
    _sig_util.ensure_text_to_sign_equals_json_body(
        request.to_sign_text(),
        request.to_json(),
    )
