"""Tests for the address module."""

import pytest

from csobpg.v19.models import order


@pytest.mark.parametrize(
    ["address", "city", "zip_code", "address2", "address3"],
    [
        ("a" * 51, "city", "zip", "address2", "address3"),
        ("address", "a" * 51, "zip", "address2", "address3"),
        ("address", "city", "a" * 17, "address2", "address3"),
        ("address", "city", "zip", "a" * 51, "address3"),
        ("address", "city", "zip", "address2", "a" * 51),
    ],
)
def test_address_invalid_args(
    address: str,
    city: str,
    zip_code: str,
    address2: str,
    address3: str,
):
    """Test for the invalid CartItem args."""
    with pytest.raises(ValueError, match="should be"):
        order.AddressData(
            address,
            "CZE",
            city,
            zip_code,
            "state",
            address2,
            address3,
        )


def test_as_json():
    """Test address as JSON."""
    assert order.AddressData(
        "a1",
        "country",
        "city",
        "zip",
        "state",
        "a2",
        "a3",
    ).as_json() == {
        "address1": "a1",
        "address2": "a2",
        "address3": "a3",
        "city": "city",
        "zip": "zip",
        "state": "state",
        "country": "country",
    }


def test_unset_fields_are_not_signed():
    """Test the unset address fields contributing nothing.

    They are returned as nulls, which `BaseRequest` strips before the
    body goes out.
    """
    address = order.AddressData(
        address="a",
        country="CZE",
        city="c",
        zip_code="1",
    )

    assert address.to_sign_text() == "a|c|1|CZE"
    assert address.as_json() == {
        "address1": "a",
        "address2": None,
        "address3": None,
        "city": "c",
        "zip": "1",
        "state": None,
        "country": "CZE",
    }
