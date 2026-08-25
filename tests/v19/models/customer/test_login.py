"""Tests for the login module."""

from csobpg.v19.models import customer as _customer


def test_empty_strings_are_signed_and_sent():
    """Test empty strings being signed and sent as empty strings."""
    login = _customer.LoginData(
        auth=_customer.AuthMethod.GUEST,
        auth_at="",
        auth_data="",
    )

    assert login.to_sign_text() == "guest||"
    assert login.as_json() == {
        "auth": "guest",
        "authAt": "",
        "authData": "",
    }


def test_empty_is_not_signed():
    """Test an all-unset login contributing nothing."""
    assert _customer.LoginData().to_sign_text() == ""
