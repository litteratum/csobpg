"""Tests for the echo responses.

Expected sign texts follow the CSOB specification field order:

* echo: "Basic methods" wiki page
* applepay/echo: "Methods for Apple Pay" wiki page
* googlepay/echo: "Methods for Google Pay" wiki page
* oneclick/echo: "Methods for OneClick Payment" wiki page
"""

from csobpg.v19.response import (
    ApplePayEchoResponse,
    EchoResponse,
    GooglePayEchoResponse,
    OneClickEchoResponse,
)
from tests.utils import response as _resp_util
from tests.utils import signature as _sig_util

_DTTM = "20240101120000"


def test_echo():
    """Test echo response signing: dttm|resultCode|resultMessage."""
    body = {
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "signature": "fake_s",
    }
    response = _resp_util.build_response(EchoResponse, body)

    assert response.to_sign_text() == f"{_DTTM}|0|OK"
    _sig_util.ensure_text_to_sign_equals_json_body(
        response.to_sign_text(),
        body,
    )


def test_oneclick_echo():
    """Test oneclick/echo signing: origPayId|dttm|resultCode|resultMessage."""
    body = {
        "origPayId": "tid",
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "signature": "fake_s",
    }
    response = _resp_util.build_response(OneClickEchoResponse, body)

    assert response.to_sign_text() == f"tid|{_DTTM}|0|OK"
    _sig_util.ensure_text_to_sign_equals_json_body(
        response.to_sign_text(),
        body,
    )


def test_applepay_echo():
    """Test applepay/echo signing.

    dttm|resultCode|resultMessage
    |initParams.countryCode|initParams.supportedNetworks
    |initParams.merchantCapabilities
    """
    body = {
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "initParams": {
            "countryCode": "CZ",
            "supportedNetworks": ["visa", "masterCard"],
            "merchantCapabilities": ["supports3DS", "supportsCredit"],
        },
        "signature": "fake_s",
    }
    response = _resp_util.build_response(ApplePayEchoResponse, body)

    assert response.to_sign_text() == (
        f"{_DTTM}|0|OK|CZ|visa|masterCard|supports3DS|supportsCredit"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(
        response.to_sign_text(),
        body,
    )


def test_googlepay_echo():
    """Test googlepay/echo signing.

    dttm|resultCode|resultMessage
    |initParams.apiVersion|initParams.apiVersionMinor
    |initParams.paymentMethodType|initParams.allowedCardNetworks
    |initParams.allowedCardAuthMethods
    |initParams.assuranceDetailsRequired
    |initParams.billingAddressRequired
    |initParams.billingAddressParametersFormat
    |initParams.tokenizationSpecificationType|initParams.gateway
    |initParams.gatewayMerchantId|initParams.googlepayMerchantId
    |initParams.merchantName|initParams.environment
    |initParams.totalPriceStatus|initParams.countryCode
    """
    body = {
        "dttm": _DTTM,
        "resultCode": 0,
        "resultMessage": "OK",
        "initParams": {
            "apiVersion": 2,
            "apiVersionMinor": 1,
            "paymentMethodType": "CARD",
            "allowedCardNetworks": ["VISA", "MASTERCARD"],
            "allowedCardAuthMethods": ["PAN_ONLY", "CRYPTOGRAM_3DS"],
            "assuranceDetailsRequired": True,
            "billingAddressRequired": False,
            "billingAddressParametersFormat": "FULL",
            "tokenizationSpecificationType": "PAYMENT_GATEWAY",
            "gateway": "csob",
            "gatewayMerchantId": "gmid",
            "googlepayMerchantId": "gpmid",
            "merchantName": "mname",
            "environment": "TEST",
            "totalPriceStatus": "FINAL",
            "countryCode": "CZ",
        },
        "signature": "fake_s",
    }
    response = _resp_util.build_response(GooglePayEchoResponse, body)

    assert response.to_sign_text() == (
        f"{_DTTM}|0|OK|2|1|CARD|VISA|MASTERCARD|PAN_ONLY|CRYPTOGRAM_3DS|"
        "true|false|FULL|PAYMENT_GATEWAY|csob|gmid|gpmid|mname|TEST|FINAL|CZ"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(
        response.to_sign_text(),
        body,
    )
