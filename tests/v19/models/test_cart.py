"""Tests for the cart module."""

from csobpg.v19.models import cart


def test_cart_item_as_json():
    """Test for the CartItem.as_json()."""
    item = cart.CartItem("example_name", 10, 100)
    assert item.as_json() == {
        "name": "example_name",
        "quantity": 10,
        "amount": 100,
        "description": None,
    }

    item.description = "desc"
    assert item.as_json()["description"] == "desc"


def test_cart_as_json():
    """Test for the Cart.as_json()."""
    item = cart.CartItem("example", 1, 1)
    assert cart.Cart([item]).as_json() == [item.as_json()]


def test_total_amount():
    """Test for the total_amount."""
    assert (
        cart.Cart(
            [cart.CartItem("Apples", 2, 10), cart.CartItem("Oranges", 1, 20)],
        ).total_amount
        == 30
    )


def test_cart_item_empty_description():
    """Test an empty description being signed and sent."""
    item = cart.CartItem("n", 1, 100, description="")

    assert item.to_sign_text() == "n|1|100|"
    assert item.as_json()["description"] == ""
