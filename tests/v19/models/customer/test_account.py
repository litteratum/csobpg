"""Tests for the account module."""

from csobpg.v19.models import customer as _customer


def test_zero_counters_are_signed_and_sent():
    """Test a brand new account: every counter zero, not suspicious.

    Zero is a legal counter value, not "unset".
    """
    account = _customer.AccountData(
        order_history=0,
        payment_day=0,
        payment_year=0,
        oneclick_adds=0,
        suspicious=False,
    )

    assert account.to_sign_text() == "0|0|0|0|false"
    assert account.as_json() == {
        "createdAt": None,
        "changedAt": None,
        "changedPwdAt": None,
        "orderHistory": 0,
        "paymentDay": 0,
        "paymentYear": 0,
        "oneclickAdds": 0,
        "suspicious": False,
    }


def test_empty_dates_are_signed_and_sent():
    """Test empty dates being signed and sent as empty strings."""
    account = _customer.AccountData(
        created_at="",
        changed_at="",
        changed_pwd_at="",
    )
    json_body = account.as_json()

    assert account.to_sign_text() == "||"
    assert json_body["createdAt"] == ""
    assert json_body["changedAt"] == ""
    assert json_body["changedPwdAt"] == ""


def test_empty_is_not_signed():
    """Test an all-unset account contributing nothing."""
    assert _customer.AccountData().to_sign_text() == ""
