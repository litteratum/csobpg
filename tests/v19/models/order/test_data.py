"""Tests for the data module."""

import pytest

from csobpg.v19.models import currency, order


@pytest.mark.parametrize(
    "quantity",
    [
        0,
        -1,
        100,
    ],
)
def test_gift_cards_invalid_quantity(quantity: int):
    """Test invalid quantity arg for the GiftCardsData."""
    with pytest.raises(ValueError, match="should be"):
        order.GiftCardsData(quantity=quantity)


def test_gift_cards_unset_fields_are_not_signed():
    """Test the unset gift cards fields contributing nothing.

    They are returned as nulls, which `BaseRequest` strips before the
    body goes out.
    """
    gift_cards = order.GiftCardsData(currency=currency.Currency.CZK)

    assert gift_cards.to_sign_text() == "CZK"
    assert gift_cards.as_json() == {
        "totalAmount": None,
        "quantity": None,
        "currency": "CZK",
    }


def test_zero_delivery_mode_is_signed_and_sent():
    """Test electronic delivery, whose mode is a legal zero."""
    data = order.OrderData(
        delivery=order.DeliveryData(mode=order.DeliveryMode.ELECTRONIC),
    )

    assert data.to_sign_text() == "0"
    assert data.as_json()["deliveryMode"] == "0"


def test_empty_strings_are_signed_and_sent():
    """Test empty strings being signed and sent as empty strings."""
    data = order.OrderData(
        delivery=order.DeliveryData(email=""),
        shipping_added_at="",
    )
    json_body = data.as_json()

    assert data.to_sign_text() == "|"
    assert json_body["deliveryEmail"] == ""
    assert json_body["shippingAddedAt"] == ""


def test_empty_gift_cards_are_not_signed():
    """Test all-unset gift cards contributing nothing.

    They carry no items, so they contribute neither a value nor a
    delimiter.
    """
    data = order.OrderData(
        order_type=order.OrderType.CASH,
        gift_cards=order.GiftCardsData(),
    )

    assert data.to_sign_text() == "cash"


def test_empty_is_not_signed():
    """Test an all-unset order contributing nothing."""
    assert order.OrderData().to_sign_text() == ""
