"""Tests for the fingerprint module."""

from csobpg.v19.models import fingerprint as _fp


class TestBrowser:
    """Tests for the `Browser`."""

    def test_zeros_and_false_are_signed_and_sent(self):
        """Test zero and false being signed and sent.

        Zero and false are legal browser values, not "unset": a UTC
        browser has a zero timezone offset and `javaEnabled` may legally
        be false.
        """
        browser = _fp.Browser(
            user_agent="UA",
            accept_header="acc",
            language="cs",
            js_enabled=True,
            color_depth=0,
            screen_height=0,
            screen_width=0,
            timezone=0,
            java_enabled=False,
        )

        assert browser.to_sign_text() == "UA|acc|cs|true|0|0|0|0|false"
        assert browser.as_json() == {
            "userAgent": "UA",
            "acceptHeader": "acc",
            "language": "cs",
            "javascriptEnabled": True,
            "colorDepth": 0,
            "screenHeight": 0,
            "screenWidth": 0,
            "timezone": 0,
            "javaEnabled": False,
            "challengeWindowSize": None,
        }

    def test_empty_challenge_window_size_is_signed_and_sent(self):
        """Test an empty challenge window size being signed and sent."""
        browser = _fp.Browser(
            user_agent="UA",
            accept_header="acc",
            language="cs",
            js_enabled=True,
            challenge_window_size="",
        )

        assert browser.to_sign_text() == "UA|acc|cs|true|"
        assert browser.as_json()["challengeWindowSize"] == ""


class TestSDK:
    """Tests for the `SDK`."""

    def test_unset_fields_are_not_signed(self):
        """Test the unset 3DS fields contributing nothing.

        They are returned as nulls, which `BaseRequest` strips before
        the body goes out.
        """
        sdk = _fp.SDK(
            max_timeout=10,
            reference_number="ref",
            transaction_id="tid",
        )

        assert sdk.to_sign_text() == "10|ref|tid"
        assert sdk.as_json() == {
            "appId": None,
            "encData": None,
            "ephemPubKey": None,
            "maxTimeout": 10,
            "referenceNumber": "ref",
            "transID": "tid",
        }


class TestFingerprint:
    """Tests for the `Fingerprint`."""

    def test_empty_is_not_signed(self):
        """Test an all-unset fingerprint contributing nothing.

        It carries no items, so it contributes neither a value nor a
        delimiter.
        """
        fingerprint = _fp.Fingerprint()

        assert fingerprint.to_sign_text() == ""
        assert fingerprint.as_json() == {"browser": None, "sdk": None}
