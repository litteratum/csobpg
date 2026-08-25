"""Tests for the data module."""

from csobpg.v19.models import customer as _customer


def test_empty_strings_are_signed_and_sent():
    """Test empty strings being signed and sent as empty strings."""
    customer = _customer.CustomerData(name="", email="")
    json_body = customer.as_json()

    assert customer.to_sign_text() == "|"
    assert json_body["name"] == ""
    assert json_body["email"] == ""


def test_empty_account_and_login_are_not_signed():
    """Test an all-unset account and login contributing nothing.

    They carry no items, so they contribute neither a value nor a
    delimiter.
    """
    customer = _customer.CustomerData(
        email="a@b.c",
        account=_customer.AccountData(),
        login=_customer.LoginData(),
    )

    assert customer.to_sign_text() == "a@b.c"


def test_empty_is_not_signed():
    """Test an all-unset customer contributing nothing."""
    assert _customer.CustomerData().to_sign_text() == ""
