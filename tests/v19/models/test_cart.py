"""Tests for the cart module."""

from __future__ import annotations

import pytest

from csobpg.v19.models import cart


def test_cart_item_as_json():
    """Test for the CartItem.as_json()."""
    item = cart.CartItem("example_name", 10, 100)
    assert item.as_json() == {
        "name": "example_name",
        "quantity": 10,
        "amount": 100,
    }

    item.description = "desc"
    assert item.as_json()["description"] == "desc"


@pytest.mark.parametrize(
    ["name", "quantity", "amount", "description"],
    [
        ("a" * 100, 1, 1, None),
        ("name", 0, 1, None),
        ("name", 1, -1, "desc"),
        ("name", 1, 1, "a" * 41),
    ],
)
def test_cart_item_invalid_args(
    name: str,
    quantity: int,
    amount: int,
    description: str | None,
):
    """Test for the invalid CartItem args."""
    with pytest.raises(ValueError, match="should be"):
        cart.CartItem(name, quantity, amount, description)


def test_cart_as_json():
    """Test for the Cart.as_json()."""
    item = cart.CartItem("example", 1, 1)
    assert cart.Cart([item]).as_json() == [item.as_json()]


@pytest.mark.parametrize("items", [[], [cart.CartItem("example", 1, 1)] * 3])
def test_invalid_size(items):
    """Test for the invalid cart size."""
    with pytest.raises(ValueError, match="1 or 2"):
        cart.Cart(items)


def test_total_amount():
    """Test for the total_amount."""
    assert (
        cart.Cart(
            [cart.CartItem("Apples", 2, 10), cart.CartItem("Oranges", 1, 20)],
        ).total_amount
        == 40
    )
