"""Tests for the api."""

from __future__ import annotations

import json as jsonlib
from dataclasses import dataclass

import pytest
from freezegun import freeze_time
from httprest.http.fake_client import FakeHTTPClient, HTTPResponse

from csobpg.v19 import errors as _e
from csobpg.v19 import response as _csobpg_response
from csobpg.v19.api import APIClient
from csobpg.v19.key import RAMRSAKey, RSAKey
from csobpg.v19.models.fingerprint import SDK, Browser, Fingerprint
from csobpg.v19.response import PaymentStatus
from csobpg.v19.response.echo import EchoResponse
from csobpg.v19.response.oneclick_echo import OneClickEchoResponse
from csobpg.v19.response.oneclick_payment_init import (
    OneClickPaymentInitResponse,
)
from csobpg.v19.response.oneclick_payment_process import (
    OneClickPaymentProcessResponse,
)
from csobpg.v19.response.payment_close import PaymentCloseResponse
from csobpg.v19.response.payment_init import PaymentInitResponse
from csobpg.v19.response.payment_process import PaymentProcessResponse
from csobpg.v19.response.payment_refund import PaymentRefundResponse
from csobpg.v19.response.payment_reverse import PaymentReverseResponse
from csobpg.v19.response.payment_status import PaymentStatusResponse
from csobpg.v19.signature import sign

_PRIVATE_KEY = RAMRSAKey("tests/v19/data/merchant.key")
_PUBLIC_KEY = RAMRSAKey("tests/v19/data/merchant.pub")


@dataclass
class _Components:
    api: APIClient
    base_url: str
    http_client: FakeHTTPClient

    @classmethod
    def compose(
        cls,
        merchant_id: str = "mid",
        private_key: RSAKey = _PRIVATE_KEY,
        public_key: RSAKey = _PUBLIC_KEY,
        base_url: str = "https://api.com",
        http_client: FakeHTTPClient | None = None,
    ) -> _Components:
        """Compose components."""
        http_client = http_client or FakeHTTPClient()
        return cls(
            APIClient(
                merchant_id,
                private_key,
                public_key,
                base_url,
                http_client,
            ),
            base_url,
            http_client,
        )


def _http_client(json: dict, status_code: int = 200) -> FakeHTTPClient:
    """Return an HTTP client responding with the given JSON."""
    return FakeHTTPClient(
        responses=[
            HTTPResponse(
                status_code,
                jsonlib.dumps(json).encode(),
                headers={"Content-Type": "application/json"},
            ),
        ],
    )


@freeze_time("1955-11-12")
def test_init_payment():
    """Test for the payment init."""
    resp = PaymentInitResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    resp = comps.api.init_payment("oid", 1000, "http://return.com")
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "cart": [{"amount": 1000, "name": "Payment", "quantity": 1}],
                "closePayment": True,
                "currency": "CZK",
                "dttm": "19551112000000",
                "language": "cs",
                "merchantId": comps.api.merchant_id,
                "orderNo": "oid",
                "payMethod": "card",
                "payOperation": "payment",
                "returnMethod": "POST",
                "returnUrl": "http://return.com",
                "signature": (
                    "mk2a83Kfc1jM2kUzOX2c4wQljQFg2zgc1n19Oyh3iVXIBRcpWfGS3jHaa"
                    "h6rw3xnXDyA5ye5J2a/y00FLU3bBc4EPvnV3FLADQkJaLhgYsMX22wznm"
                    "CpGcF9MEk165b7wTdxq8hhuTjTTL+FehNYAt2WBoPRlOSSlWGgT4o6j0b"
                    "4iwe9F82vARknJVAlTXDipjQx9JJqkcPYyBXd6Zxnr4N35YrOzEfZ4DyX"
                    "7uiZgFd2QKRPo/VKZvmmiPSom7zeFdipukGvyIdXG/1Wl+iScCBf/Z93V"
                    "Xpzrtp9l4IbfB4hyThjedQ+Bd1/PitlJeTplscfffPExosZHVK7usguAQ"
                    "=="
                ),
                "totalAmount": 1000,
                "ttlSec": 600,
            },
            "cert": None,
            "method": "post",
            "url": f"{comps.base_url}/payment/init",
        },
    ]


@freeze_time("1955-11-12")
def test_get_payment_status():
    """Test for the payment status get."""
    resp = PaymentStatusResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    resp = comps.api.get_payment_status("oid")
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": None,
            "method": "get",
            "url": (
                f"{comps.base_url}/payment/status/mid/oid/19551112000000/qOvsS"
                "hm%2FqBiQmwar3tCQoc%2F9igPha2rBdbu3bhWHeSLMfHSVDid0cEdcn8R5Nw"
                "bsoZKqLW7pBfDQtgAhiWmVJEywguwwcplwc57bc%2BLCjgeu0mMGUxvJcmt5k"
                "jRXFabzQHc3Pheno2p4jf%2Fp5O7m67JdsSTonrB7J3SvxiX37dIdsXEOtT4Q"
                "Sf2G1cENqUfQBqL6z40eZmJ2SB6nKy8Ji0QwQN07KFHgBdM0Jt50ZJJ0uQk8W"
                "Ef%2BwJPEDUiDQNvrVVRjgi1IwT1CrWsRAMp%2Bmn9Dfck4%2BrjVCB9ZpiE3"
                "%2B11UPPxFEchcgYYBzOQ3ZJnFY8hpNuCt7gqJ2VE%2FagxmRQ%3D%3D"
            ),
            "cert": None,
        },
    ]


@freeze_time("1955-11-12")
def test_reverse_payment():
    """Test for the payment reversal."""
    resp = PaymentReverseResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    resp = comps.api.reverse_payment("oid")
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "merchantId": comps.api.merchant_id,
                "payId": "oid",
                "signature": (
                    "qOvsShm/qBiQmwar3tCQoc/9igPha2rBdbu3bhWHeSLMfHSVDid0cEdcn"
                    "8R5NwbsoZKqLW7pBfDQtgAhiWmVJEywguwwcplwc57bc+LCjgeu0mMGUx"
                    "vJcmt5kjRXFabzQHc3Pheno2p4jf/p5O7m67JdsSTonrB7J3SvxiX37dI"
                    "dsXEOtT4QSf2G1cENqUfQBqL6z40eZmJ2SB6nKy8Ji0QwQN07KFHgBdM0"
                    "Jt50ZJJ0uQk8WEf+wJPEDUiDQNvrVVRjgi1IwT1CrWsRAMp+mn9Dfck4+"
                    "rjVCB9ZpiE3+11UPPxFEchcgYYBzOQ3ZJnFY8hpNuCt7gqJ2VE/agxmRQ"
                    "=="
                ),
            },
            "method": "put",
            "url": f"{comps.base_url}/payment/reverse",
            "cert": None,
        },
    ]


@freeze_time("1955-11-12")
def test_close_payment():
    """Test for the payment close."""
    resp = PaymentCloseResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    resp = comps.api.close_payment("oid", total_amount=1010)
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "merchantId": comps.api.merchant_id,
                "payId": "oid",
                "signature": (
                    "hc6JmmMa9JOOb6lKnHclSQ1OZJWX5sI71oxyAu5FJlQ2+JoiGKOGOMMJH"
                    "Z+VA+nSawjNYcvZg9eDM4c3DYFLYjLI0CDZojXb7tg/jtW9eGBhgNERGR"
                    "JoTPLviWAbztQoLYR09sCi0U/X9Hwn7A14P7yjQIjscphRVWHDo6ye/G4"
                    "3byRURoSyMqdd3DJwRlttJbvmOXVqRk6Qh6gPJRMMXIe0fPmGNO2YykFb"
                    "r4ICeA9uIqIgKRUEGEEIQmMZZTf1BdQv9VNfkBR0+JXzgyp62fjIxuepd"
                    "24VrxunwveNhnTB6ynhIbDOz5yhs0c+wEmkxg5Yp0RNxCKZB+ixr/JZuA"
                    "=="
                ),
                "totalAmount": 1010,
            },
            "method": "put",
            "url": f"{comps.base_url}/payment/close",
            "cert": None,
        },
    ]


@freeze_time("1955-11-12")
def test_refund_payment():
    """Test for the payment refund."""
    resp = PaymentRefundResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    resp = comps.api.refund_payment("oid", amount=1010)
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "amount": 1010,
                "dttm": "19551112000000",
                "merchantId": comps.api.merchant_id,
                "payId": "oid",
                "signature": (
                    "hc6JmmMa9JOOb6lKnHclSQ1OZJWX5sI71oxyAu5FJlQ2+JoiGKOGOMMJH"
                    "Z+VA+nSawjNYcvZg9eDM4c3DYFLYjLI0CDZojXb7tg/jtW9eGBhgNERGR"
                    "JoTPLviWAbztQoLYR09sCi0U/X9Hwn7A14P7yjQIjscphRVWHDo6ye/G4"
                    "3byRURoSyMqdd3DJwRlttJbvmOXVqRk6Qh6gPJRMMXIe0fPmGNO2YykFb"
                    "r4ICeA9uIqIgKRUEGEEIQmMZZTf1BdQv9VNfkBR0+JXzgyp62fjIxuepd"
                    "24VrxunwveNhnTB6ynhIbDOz5yhs0c+wEmkxg5Yp0RNxCKZB+ixr/JZuA"
                    "=="
                ),
            },
            "method": "put",
            "url": f"{comps.base_url}/payment/refund",
            "cert": None,
        },
    ]


@freeze_time("1955-11-12")
def test_api_error():
    """Test for an API error."""
    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    401,
                    jsonlib.dumps({"resultCode": 110}).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    with pytest.raises(_e.APIError):
        comps.api.refund_payment("oid", amount=1010)


@freeze_time("1955-11-12")
def test_api_error_empty_json():
    """Test for an API error.

    If an empty JSON is returned, an HTTPError should be raised.
    """
    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    401,
                    jsonlib.dumps({}).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    with pytest.raises(_e.APIInvalidResponseError, match="Empty"):
        comps.api.refund_payment("oid", amount=1010)


@freeze_time("1955-11-12")
def test_api_error_signed():
    """Test for a signed API error.

    Its signature must be verified before the resultCode is raised for.
    """
    resp = PaymentRefundResponse(
        "pid",
        "20240919164156",
        150,
        "Payment not in valid state",
    )
    comps = _Components.compose(
        http_client=_http_client(
            {
                "payId": resp.pay_id,
                "dttm": resp.dttm,
                "resultCode": str(resp.result_code),
                "resultMessage": resp.result_message,
                "signature": sign(
                    resp.to_sign_text().encode(),
                    str(_PRIVATE_KEY),
                ),
            },
            200,
        ),
    )

    with pytest.raises(_e.APIPaymentInInvalidStateError):
        comps.api.refund_payment("oid", amount=1010)


@freeze_time("1955-11-12")
def test_api_error_fabricated():
    """Test for a fabricated API error.

    An error must not be reported if the response claiming it is signed,
    but the signature does not match.
    """
    resp = PaymentRefundResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
    )
    comps = _Components.compose(
        http_client=_http_client(
            {
                "payId": resp.pay_id,
                "dttm": resp.dttm,
                # the params below are not the signed ones
                "resultCode": "150",
                "resultMessage": "Payment not in valid state",
                "paymentStatus": resp.payment_status.value,
                "signature": sign(
                    resp.to_sign_text().encode(),
                    str(_PRIVATE_KEY),
                ),
            },
            200,
        ),
    )

    with pytest.raises(_e.APIInvalidSignatureError):
        comps.api.refund_payment("oid", amount=1010)


@freeze_time("1955-11-12")
def test_api_error_unsigned():
    """Test for an unsigned API error.

    The API does not sign the requests it rejects before processing them.
    Such an error must still be reported.
    """
    comps = _Components.compose(
        http_client=_http_client(
            {"resultCode": 100, "resultMessage": "Missing parameter payId"},
            401,
        ),
    )

    with pytest.raises(_e.APIError, match="Missing parameter payId"):
        comps.api.refund_payment("oid", amount=1010)


@freeze_time("1955-11-12")
def test_api_error_signed_without_params():
    """Test for a signed API error missing the response params.

    Such a response cannot be verified, but the error it reports must not
    get lost.
    """
    comps = _Components.compose(
        http_client=_http_client(
            {
                "dttm": "20240919164156",
                "resultCode": 150,
                "resultMessage": "Payment not in valid state",
                "signature": "signature",
            },
            400,
        ),
    )

    with pytest.raises(_e.APIPaymentInInvalidStateError):
        comps.api.refund_payment("oid", amount=1010)


@freeze_time("1955-11-12")
def test_unsigned_success_response():
    """Test for an unsigned successful response.

    An unsigned response must never be turned into a result.
    """
    resp = PaymentRefundResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
    )
    comps = _Components.compose(
        http_client=_http_client(
            {
                "payId": resp.pay_id,
                "dttm": resp.dttm,
                "resultCode": str(resp.result_code),
                "resultMessage": resp.result_message,
                "paymentStatus": resp.payment_status.value,
            },
        ),
    )

    with pytest.raises(_e.APIInvalidResponseError):
        comps.api.refund_payment("oid", amount=1010)


@freeze_time("1955-11-12")
def test_missing_result_code():
    """Test for a response without the resultCode."""
    comps = _Components.compose(
        http_client=_http_client({"resultMessage": "OK"}),
    )

    with pytest.raises(_e.APIInvalidResponseError, match="resultCode"):
        comps.api.refund_payment("oid", amount=1010)


@freeze_time("1955-11-12")
@pytest.mark.parametrize(
    "result_code",
    ["unknown", None, [], {"resultCode": 0}],
)
def test_invalid_result_code(result_code):
    """Test for an invalid resultCode."""
    comps = _Components.compose(
        http_client=_http_client({"resultCode": result_code}),
    )

    with pytest.raises(_e.APIInvalidResponseError, match="Invalid resultCode"):
        comps.api.refund_payment("oid", amount=1010)


@freeze_time("1955-11-12")
@pytest.mark.parametrize("payment_status", ["unknown", None, []])
def test_invalid_payment_status(payment_status):
    """Test for an invalid paymentStatus."""
    comps = _Components.compose(
        http_client=_http_client(
            {
                "resultCode": 0,
                "paymentStatus": payment_status,
                "signature": "signature",
            },
        ),
    )

    with pytest.raises(
        _e.APIInvalidResponseError,
        match="Invalid paymentStatus",
    ):
        comps.api.refund_payment("oid", amount=1010)


@freeze_time("1955-11-12")
def test_unknown_payment_status():
    """Test for a well-formed, but unknown paymentStatus."""
    comps = _Components.compose(
        http_client=_http_client(
            {
                "payId": "pid",
                "dttm": "20240919164156",
                "resultCode": 0,
                "resultMessage": "",
                "paymentStatus": 42,
                "signature": "signature",
            },
        ),
    )

    with pytest.raises(
        _e.APIInvalidResponseError,
        match="Unexpected paymentStatus",
    ):
        comps.api.refund_payment("oid", amount=1010)


@freeze_time("1955-11-12")
def test_success_result_code_with_error_status():
    """Test for a non-200 response reporting a success resultCode.

    The API returns 200 for every request it has processed. A resultCode 0
    with any other status contradicts that and must not be reported as
    a success.
    """
    comps = _Components.compose(
        http_client=_http_client({"resultCode": 0}, 500),
    )

    with pytest.raises(_e.APIInvalidResponseError) as exc_info:
        comps.api.refund_payment("oid", amount=1010)

    assert exc_info.value.response.status_code == 500


@freeze_time("1955-11-12")
def test_no_json_response():
    """Test for a response carrying no JSON.

    The HTTP response must be attached to the error, as it is the only
    thing left to diagnose it with.
    """
    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    502,
                    b"<html>Bad Gateway</html>",
                    headers={"Content-Type": "text/html"},
                ),
            ],
        ),
    )

    with pytest.raises(_e.APIInvalidResponseError, match="No JSON") as exc:
        comps.api.refund_payment("oid", amount=1010)

    assert exc.value.response.status_code == 502


@freeze_time("1955-11-12")
def test_malformed_json_response():
    """Test for a response with a malformed JSON body."""
    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    b"{",
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )

    with pytest.raises(
        _e.APIInvalidResponseError,
        match="Invalid response from API",
    ) as exc:
        comps.api.refund_payment("oid", amount=1010)

    assert exc.value.response.status_code == 200


@freeze_time("1955-11-12")
def test_get_payment_process_url():
    """Test for the payment process URL build."""
    comps = _Components.compose()
    assert comps.api.get_payment_process_url("oid") == (
        f"{comps.base_url}/payment/process/mid/oid/19551112000000/qOvsShm%2FqB"
        "iQmwar3tCQoc%2F9igPha2rBdbu3bhWHeSLMfHSVDid0cEdcn8R5NwbsoZKqLW7pBfDQt"
        "gAhiWmVJEywguwwcplwc57bc%2BLCjgeu0mMGUxvJcmt5kjRXFabzQHc3Pheno2p4jf%2"
        "Fp5O7m67JdsSTonrB7J3SvxiX37dIdsXEOtT4QSf2G1cENqUfQBqL6z40eZmJ2SB6nKy8"
        "Ji0QwQN07KFHgBdM0Jt50ZJJ0uQk8WEf%2BwJPEDUiDQNvrVVRjgi1IwT1CrWsRAMp%2B"
        "mn9Dfck4%2BrjVCB9ZpiE3%2B11UPPxFEchcgYYBzOQ3ZJnFY8hpNuCt7gqJ2VE%2Fagx"
        "mRQ%3D%3D"
    )


@freeze_time("1955-11-12")
def test_echo():
    """Test for the echo."""
    resp = EchoResponse("20240919164156", 0, "OK")

    resp_json = {
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    resp = comps.api.echo()
    assert isinstance(resp, EchoResponse)
    assert resp.dttm == "20240919164156"
    assert resp.result_code == 0
    assert resp.result_message == "OK"
    assert resp.success
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "merchantId": comps.api.merchant_id,
                "signature": (
                    "i73Jtef6OPfGlH6I/YbwNv9vEeTUVtlQvJ0ZHOcaoWv2/NfGAhLdjiyWI"
                    "uDys0IJk17ndTCZdbDOF4Ku/sj47uI5qAaJskLeHGZaFytFcIEmd7R9sY"
                    "O4Ath1UvXmNdpNJyQXwlqnQrMDwcxRLWaWclQWZeTjjihxFNWbN5sN0xC"
                    "+BJgY73AuvmiC0yakQE2eWPFcS2ErvTgPb5mb3Wudut8O5JzflTNEGjmv"
                    "T+ln2ndB8qefvm5vcRYvoNeJcF/yXTRUjy4lMf8Ua9lHSwYNz3sjgbn1b"
                    "B7xcJRFUFfp94W8gWBxcflxVmk4/s0Pe7CPJxuTITi1rSGS8sayGGywZA"
                    "=="
                ),
            },
            "method": "post",
            "url": f"{comps.base_url}/echo",
            "cert": None,
        },
    ]


class TestProcessGatewayReturn:
    """Tests for the gateway return processing.

    The gateway return is posted by the customer's browser, so its params
    are fully under the customer's control. Nothing but a valid signature
    may be trusted.
    """

    @staticmethod
    def _datadict(
        result_code: int = 0,
        result_message: str = "",
        signed: bool = True,
    ) -> dict:
        """Return a gateway return datadict as the browser posts it."""
        resp = PaymentProcessResponse(
            "pid",
            "20240919164156",
            result_code,
            result_message,
            PaymentStatus.IN_PROGRESS,
            auth_code="acode",
        )
        datadict = {
            "payId": resp.pay_id,
            "dttm": resp.dttm,
            "resultCode": str(resp.result_code),
            "resultMessage": resp.result_message,
            "paymentStatus": resp.payment_status.value,
            "authCode": resp.auth_code,
        }

        if signed:
            datadict["signature"] = sign(
                resp.to_sign_text().encode(),
                str(_PRIVATE_KEY),
            )

        return datadict

    def test_ok(self):
        """Test OK case."""
        comps = _Components.compose()

        resp = comps.api.process_gateway_return(self._datadict())

        assert resp.success
        assert resp.auth_code == "acode"
        assert resp.payment_status is PaymentStatus.IN_PROGRESS
        assert not comps.http_client.history

    def test_datadict_is_not_modified(self):
        """Test the caller's datadict is left untouched."""
        datadict = self._datadict()
        original = {**datadict}

        _Components.compose().api.process_gateway_return(datadict)

        assert datadict == original

    def test_signed_error(self):
        """Test for a signed failure.

        Its signature must be verified before the resultCode is raised for.
        """
        datadict = self._datadict(150, "Payment not in valid state")

        with pytest.raises(_e.APIPaymentInInvalidStateError):
            _Components.compose().api.process_gateway_return(datadict)

    def test_unsigned_error(self):
        """Test for an unsigned failure.

        Dropping the signature must not be a way to fabricate a failure.
        """
        datadict = self._datadict(
            150,
            "Payment not in valid state",
            signed=False,
        )

        with pytest.raises(
            _e.APIInvalidResponseError,
            match="Missing signature",
        ):
            _Components.compose().api.process_gateway_return(datadict)

    def test_empty_signature(self):
        """Test for a failure signed with an empty signature."""
        datadict = self._datadict(150, "Payment not in valid state")
        datadict["signature"] = ""

        with pytest.raises(_e.APIInvalidResponseError, match="Empty"):
            _Components.compose().api.process_gateway_return(datadict)

    def test_fabricated_error(self):
        """Test for a fabricated failure.

        The signature is valid, but not for the params claiming the failure.
        """
        datadict = self._datadict()
        datadict["resultCode"] = "150"
        datadict["resultMessage"] = "Payment not in valid state"

        with pytest.raises(_e.APIInvalidSignatureError):
            _Components.compose().api.process_gateway_return(datadict)

    def test_fabricated_success(self):
        """Test for a fabricated success."""
        datadict = self._datadict(150, "Payment not in valid state")
        datadict["resultCode"] = "0"
        datadict["resultMessage"] = ""

        with pytest.raises(_e.APIInvalidSignatureError):
            _Components.compose().api.process_gateway_return(datadict)

    def test_empty_datadict(self):
        """Test for an empty datadict."""
        with pytest.raises(_e.APIInvalidResponseError, match="Empty"):
            _Components.compose().api.process_gateway_return({})

    def test_missing_result_code(self):
        """Test for a datadict without the resultCode."""
        datadict = self._datadict()
        del datadict["resultCode"]

        with pytest.raises(_e.APIInvalidResponseError, match="resultCode"):
            _Components.compose().api.process_gateway_return(datadict)

    def test_invalid_result_code(self):
        """Test for a malformed resultCode."""
        datadict = self._datadict()
        datadict["resultCode"] = "unknown"

        with pytest.raises(
            _e.APIInvalidResponseError,
            match="Invalid resultCode",
        ):
            _Components.compose().api.process_gateway_return(datadict)

    def test_missing_mandatory_param(self):
        """Test for a datadict without a mandatory response param."""
        datadict = self._datadict()
        del datadict["payId"]

        with pytest.raises(
            _e.APIInvalidResponseError,
            match="Missing mandatory parameter",
        ):
            _Components.compose().api.process_gateway_return(datadict)

    def test_invalid_payment_status(self):
        """Test for a malformed paymentStatus."""
        datadict = self._datadict()
        datadict["paymentStatus"] = "unknown"

        with pytest.raises(
            _e.APIInvalidResponseError,
            match="Invalid paymentStatus",
        ):
            _Components.compose().api.process_gateway_return(datadict)

    def test_unknown_payment_status(self):
        """Test for a well-formed, but unknown paymentStatus."""
        datadict = self._datadict()
        datadict["paymentStatus"] = 42

        with pytest.raises(
            _e.APIInvalidResponseError,
            match="Unexpected paymentStatus",
        ):
            _Components.compose().api.process_gateway_return(datadict)


@freeze_time("1955-11-12")
class TestOneClickInitPayment:
    """Tests for the OneClick payment_init."""

    def test_ok(self):
        """Test OK case."""
        resp = OneClickPaymentInitResponse(
            "pid",
            "20240919164156",
            0,
            "",
            PaymentStatus.IN_PROGRESS,
        )

        resp_json = {
            "payId": resp.pay_id,
            "dttm": resp.dttm,
            "resultCode": str(resp.result_code),
            "resultMessage": resp.result_message,
            "paymentStatus": resp.payment_status.value,
            "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
        }

        comps = _Components.compose(
            http_client=FakeHTTPClient(
                responses=[
                    HTTPResponse(
                        200,
                        jsonlib.dumps(resp_json).encode(),
                        headers={"Content-Type": "application/json"},
                    ),
                ],
            ),
        )
        resp = comps.api.oneclick_init_payment(
            "tid",
            "oid",
            "http://return.com",
            client_ip="127.0.0.1",
        )
        assert comps.http_client.history == [
            {
                "_method": "_request",
                "headers": None,
                "json": {
                    "clientInitiated": True,
                    "clientIp": "127.0.0.1",
                    "dttm": "19551112000000",
                    "language": "cs",
                    "merchantId": comps.api.merchant_id,
                    "orderNo": "oid",
                    "origPayId": "tid",
                    "payMethod": "card",
                    "returnMethod": "POST",
                    "returnUrl": "http://return.com",
                    "sdkUsed": False,
                    "signature": (
                        "rY2SNMWrmmuoIKRi+NLi3dbq6qk2eKq9z1rmzOHlvMzZa5dwWeXIR"
                        "9FX3XrB8jTLzK/lqTV2FczHuK8HQiPcYWC+tR4ePuaabDXfV5zeUE"
                        "lQ0/zagSve9EIrI3FwoQlW4SligbKu/VS+CYSNm/jD8MragS/U61Q"
                        "Na7e2kay7KiI5DRXFex4+rN/Txkv4arisaIjN5dmE+VDR755oo8LR"
                        "f4XCno1AqbgJimqOylmEnCfRdvxnfYT1aW84KTiZznOgA3vhiSrVd"
                        "0I+L9+s3RkA1wfcrGahKQRDsJa4JzgV9V0t63TxQLoUd4aVv8zlwJ"
                        "ujuTyMniSXmteMRR03gcDsNA=="
                    ),
                },
                "method": "post",
                "url": f"{comps.base_url}/oneclick/init",
                "cert": None,
            },
        ]


@freeze_time("1955-11-12")
def test_oneclick_process():
    """Test for the oneclick process."""
    resp = OneClickPaymentProcessResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    resp = comps.api.oneclick_process("tid")
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "merchantId": comps.api.merchant_id,
                "payId": "tid",
                "signature": (
                    "0OT7wNlDCoaMtbvgmW0wf0OHu8SxRobRzHdyPEen/69prijU9QxfjNYV5"
                    "Sx7ucER8NBQOis9BxolIZgvhSeo+aH0+u6BARzfXY35CgTglnZfGBIYKA"
                    "eIMmv4xd3AaSMboMbh5js0fb1kBNsS+ouQTgzkLCZnubvUHhg1H9A4vSc"
                    "Tf+opG5DB+OJq1UmmRjmaI8Sirx52RH3mcJhjNd+/cd9n4MdbAwRrb9UF"
                    "vocHii6im3QEf8UvOCZcvv/npC6GTkLyazvNmSaol4ZtJ7aYP08jexm5Q"
                    "mTVyfpVko2XgbQ/SuYSGEBZ3iaMD4H6SVkwMjZ6OuqBVir6xC8eV5gCuA"
                    "=="
                ),
            },
            "method": "post",
            "url": f"{comps.base_url}/oneclick/process",
            "cert": None,
        },
    ]


@freeze_time("1955-11-12")
def test_oneclick_echo():
    """Test for the oneclick echo."""
    resp = OneClickEchoResponse("pid", "20240919164156", 0, "")

    resp_json = {
        "origPayId": resp.template_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    comps.api.oneclick_echo("tid")
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "merchantId": comps.api.merchant_id,
                "origPayId": "tid",
                "signature": (
                    "0OT7wNlDCoaMtbvgmW0wf0OHu8SxRobRzHdyPEen/69prijU9QxfjNYV5"
                    "Sx7ucER8NBQOis9BxolIZgvhSeo+aH0+u6BARzfXY35CgTglnZfGBIYKA"
                    "eIMmv4xd3AaSMboMbh5js0fb1kBNsS+ouQTgzkLCZnubvUHhg1H9A4vSc"
                    "Tf+opG5DB+OJq1UmmRjmaI8Sirx52RH3mcJhjNd+/cd9n4MdbAwRrb9UF"
                    "vocHii6im3QEf8UvOCZcvv/npC6GTkLyazvNmSaol4ZtJ7aYP08jexm5Q"
                    "mTVyfpVko2XgbQ/SuYSGEBZ3iaMD4H6SVkwMjZ6OuqBVir6xC8eV5gCuA"
                    "=="
                ),
            },
            "method": "post",
            "url": f"{comps.base_url}/oneclick/echo",
            "cert": None,
        },
    ]


@freeze_time("1955-11-12")
def test_googlepay_echo():
    """Test for the Google Pay echo."""
    # TODO: I'd add to_json method to Response
    init_params = {
        "apiVersion": 1.2,
        "apiVersionMinor": 2,
        "paymentMethodType": "pmt",
        "allowedCardNetworks": ["acn1", "acn2"],
        "allowedCardAuthMethods": ["aum1", "aum2"],
        "assuranceDetailsRequired": False,
        "billingAddressRequired": True,
        "billingAddressParametersFormat": "bapf",
        "tokenizationSpecificationType": "tst",
        "gateway": "g",
        "gatewayMerchantId": "gmi",
        "googlepayMerchantId": "gpmi",
        "merchantName": "mn",
        "environment": "e",
        "totalPriceStatus": "tps",
        "countryCode": "cc",
    }
    resp = _csobpg_response.GooglePayEchoResponse(
        "20240919164156",
        0,
        "",
        _csobpg_response.GooglePayInitParams.from_json(init_params),
    )

    resp_json = {
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "initParams": init_params,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    comps.api.googlepay_echo()
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "cert": None,
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "merchantId": "mid",
                "signature": (
                    "i73Jtef6OPfGlH6I/YbwNv9vEeTUVtlQvJ0ZHOcaoWv2/NfGAhLdjiyWI"
                    "uDys0IJk17ndTCZdbDOF4Ku/sj47uI5qAaJskLeHGZaFytFcIEmd7R9sY"
                    "O4Ath1UvXmNdpNJyQXwlqnQrMDwcxRLWaWclQWZeTjjihxFNWbN5sN0xC"
                    "+BJgY73AuvmiC0yakQE2eWPFcS2ErvTgPb5mb3Wudut8O5JzflTNEGjmv"
                    "T+ln2ndB8qefvm5vcRYvoNeJcF/yXTRUjy4lMf8Ua9lHSwYNz3sjgbn1b"
                    "B7xcJRFUFfp94W8gWBxcflxVmk4/s0Pe7CPJxuTITi1rSGS8sayGGywZA"
                    "=="
                ),
            },
            "method": "post",
            "url": f"{comps.base_url}/googlepay/echo",
        },
    ]


@freeze_time("1955-11-12")
def test_googlepay_init():
    """Test for the Google Pay payment init."""
    resp = _csobpg_response.GooglePayPaymentInitResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    resp = comps.api.googlepay_init(
        "oid",
        "127.0.0.1",
        100,
        {"example": "payload"},
        "return_url",
    )
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "cert": None,
            "headers": None,
            "json": {
                "clientIp": "127.0.0.1",
                "currency": "CZK",
                "dttm": "19551112000000",
                "language": "cs",
                "merchantId": "mid",
                "orderNo": "oid",
                "payload": "eyJleGFtcGxlIjogInBheWxvYWQifQ==",
                "returnMethod": "POST",
                "returnUrl": "return_url",
                "sdkUsed": False,
                "signature": (
                    "hf0GyLcS7ru80h6G06QLN8qVS4Uf8Ma+06CAzjK/MGxNElLrqHVkGXVhT"
                    "JCoBdWyH47PQTcT8LrSSydAxoJ3FvzKflrFyQnYXQ985SygKw+VYTf9li"
                    "Gz3YKSkm8DTjtYq2orxbNV+MiaP6cubYqVuqluSzYhaGT0KuPxdQCR6r3"
                    "0PpRGVbFe3zlaEF76t4mFlCOwz9ZBHd0YBDcrs+7v+ThLNmf6hVZMwlNF"
                    "lcSM1R2+X/nQLrMm/L25tF9IxnZJ3cmHNtru99dhea8t3+cNFZzNfuIhG"
                    "t0TWegfMtLAMAAqJHCTf//htjHzcU0PYIlutfRp6DXj0YUV1aPJu4IQBg"
                    "=="
                ),
                "totalAmount": 100,
            },
            "method": "post",
            "url": f"{comps.base_url}/googlepay/init",
        },
    ]


@freeze_time("1955-11-12")
def test_googlepay_process():
    """Test for the Google Pay payment process."""
    resp = _csobpg_response.GooglePayPaymentProcessResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    resp = comps.api.googlepay_process(
        "tid",
        Fingerprint(
            Browser("agent", "accept", "lang", js_enabled=True),
            SDK(max_timeout=0, reference_number="ref", transaction_id="tid"),
        ),
    )
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "cert": None,
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "fingerprint": {
                    "browser": {
                        "acceptHeader": "accept",
                        "javascriptEnabled": True,
                        "language": "lang",
                        "userAgent": "agent",
                    },
                    "sdk": {
                        "maxTimeout": 0,
                        "referenceNumber": "ref",
                        "transID": "tid",
                    },
                },
                "merchantId": "mid",
                "payId": "tid",
                "signature": (
                    "S2MlASvQIvKNeRsnUXPpSPIxB/Qmfn5TPPt/V5abWmmHMY5xKzAS7/7TJ"
                    "Bm8uP1cfNrdCEfINq0h0XetV6M4ypGkoanydORX9x6thsJRZ43l+ay4qk"
                    "899txOvPnqtUouohCugdDis6UzYCEc9CgX9rcwvf/yXyBTTGoh/10nhTi"
                    "LV9dZLUWeP8crMXbei45FPtrB/KUR4dl0bLyBn5lTY5GYJbuQB34FHONX"
                    "ovKyCS/hEhvdywBYXjwhNbzadOv0zE2GspuHaMXqC9YFrcxtx6M1J9JLS"
                    "Xqc6LzCs+BTfsACVLEw97o7RB1syuC5GFXJ2I1QHgAivkobaHLx0J6rQA"
                    "=="
                ),
            },
            "method": "post",
            "url": f"{comps.base_url}/googlepay/process",
        },
    ]


@freeze_time("1955-11-12")
def test_applepay_echo():
    """Test for the Apple Pay echo."""
    init_params = {
        "countryCode": "CZ",
        "supportedNetworks": ["masterCard", "visa"],
        "merchantCapabilities": ["supports3DS"],
    }
    resp = _csobpg_response.ApplePayEchoResponse(
        "20240919164156",
        0,
        "",
        _csobpg_response.ApplePayInitParams.from_json(init_params),
    )

    resp_json = {
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "initParams": init_params,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    comps.api.applepay_echo()
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "json": {
                "dttm": "19551112000000",
                "merchantId": "mid",
                "signature": (
                    "i73Jtef6OPfGlH6I/YbwNv9vEeTUVtlQvJ0ZHOcaoWv2/NfGAhLdjiyWI"
                    "uDys0IJk17ndTCZdbDOF4Ku/sj47uI5qAaJskLeHGZaFytFcIEmd7R9sY"
                    "O4Ath1UvXmNdpNJyQXwlqnQrMDwcxRLWaWclQWZeTjjihxFNWbN5sN0xC"
                    "+BJgY73AuvmiC0yakQE2eWPFcS2ErvTgPb5mb3Wudut8O5JzflTNEGjmv"
                    "T+ln2ndB8qefvm5vcRYvoNeJcF/yXTRUjy4lMf8Ua9lHSwYNz3sjgbn1b"
                    "B7xcJRFUFfp94W8gWBxcflxVmk4/s0Pe7CPJxuTITi1rSGS8sayGGywZA"
                    "=="
                ),
            },
            "method": "post",
            "url": f"{comps.base_url}/applepay/echo",
            "cert": None,
            "headers": None,
        },
    ]


@freeze_time("1955-11-12")
def test_applepay_init():
    """Test for the Apple Pay payment init."""
    resp = _csobpg_response.ApplePayPaymentInitResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    resp = comps.api.applepay_init(
        "oid",
        "127.0.0.1",
        100,
        {"example": "payload"},
        "return_url",
    )
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "cert": None,
            "headers": None,
            "json": {
                "clientIp": "127.0.0.1",
                "currency": "CZK",
                "dttm": "19551112000000",
                "language": "cs",
                "merchantId": "mid",
                "orderNo": "oid",
                "payload": "eyJleGFtcGxlIjogInBheWxvYWQifQ==",
                "returnMethod": "POST",
                "returnUrl": "return_url",
                "sdkUsed": False,
                "signature": (
                    "hf0GyLcS7ru80h6G06QLN8qVS4Uf8Ma+06CAzjK/MGxNElLrqHVkGXVhT"
                    "JCoBdWyH47PQTcT8LrSSydAxoJ3FvzKflrFyQnYXQ985SygKw+VYTf9li"
                    "Gz3YKSkm8DTjtYq2orxbNV+MiaP6cubYqVuqluSzYhaGT0KuPxdQCR6r3"
                    "0PpRGVbFe3zlaEF76t4mFlCOwz9ZBHd0YBDcrs+7v+ThLNmf6hVZMwlNF"
                    "lcSM1R2+X/nQLrMm/L25tF9IxnZJ3cmHNtru99dhea8t3+cNFZzNfuIhG"
                    "t0TWegfMtLAMAAqJHCTf//htjHzcU0PYIlutfRp6DXj0YUV1aPJu4IQBg"
                    "=="
                ),
                "totalAmount": 100,
            },
            "method": "post",
            "url": f"{comps.base_url}/applepay/init",
        },
    ]


@freeze_time("1955-11-12")
def test_applepay_process():
    """Test for the Apple Pay payment process."""
    resp = _csobpg_response.ApplePayPaymentProcessResponse(
        "pid",
        "20240919164156",
        0,
        "",
        PaymentStatus.IN_PROGRESS,
    )

    resp_json = {
        "payId": resp.pay_id,
        "dttm": resp.dttm,
        "resultCode": str(resp.result_code),
        "resultMessage": resp.result_message,
        "paymentStatus": resp.payment_status.value,
        "signature": sign(resp.to_sign_text().encode(), str(_PRIVATE_KEY)),
    }

    comps = _Components.compose(
        http_client=FakeHTTPClient(
            responses=[
                HTTPResponse(
                    200,
                    jsonlib.dumps(resp_json).encode(),
                    headers={"Content-Type": "application/json"},
                ),
            ],
        ),
    )
    resp = comps.api.applepay_process(
        "tid",
        Fingerprint(
            Browser("agent", "accept", "lang", js_enabled=True),
            SDK(max_timeout=0, reference_number="ref", transaction_id="tid"),
        ),
    )
    assert comps.http_client.history == [
        {
            "_method": "_request",
            "cert": None,
            "headers": None,
            "json": {
                "dttm": "19551112000000",
                "fingerprint": {
                    "browser": {
                        "acceptHeader": "accept",
                        "javascriptEnabled": True,
                        "language": "lang",
                        "userAgent": "agent",
                    },
                    "sdk": {
                        "maxTimeout": 0,
                        "referenceNumber": "ref",
                        "transID": "tid",
                    },
                },
                "merchantId": "mid",
                "payId": "tid",
                "signature": (
                    "S2MlASvQIvKNeRsnUXPpSPIxB/Qmfn5TPPt/V5abWmmHMY5xKzAS7/7TJ"
                    "Bm8uP1cfNrdCEfINq0h0XetV6M4ypGkoanydORX9x6thsJRZ43l+ay4qk"
                    "899txOvPnqtUouohCugdDis6UzYCEc9CgX9rcwvf/yXyBTTGoh/10nhTi"
                    "LV9dZLUWeP8crMXbei45FPtrB/KUR4dl0bLyBn5lTY5GYJbuQB34FHONX"
                    "ovKyCS/hEhvdywBYXjwhNbzadOv0zE2GspuHaMXqC9YFrcxtx6M1J9JLS"
                    "Xqc6LzCs+BTfsACVLEw97o7RB1syuC5GFXJ2I1QHgAivkobaHLx0J6rQA"
                    "=="
                ),
            },
            "method": "post",
            "url": f"{comps.base_url}/applepay/process",
        },
    ]
