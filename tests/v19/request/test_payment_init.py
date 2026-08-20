"""Tests for the payment init request."""

import pytest

from csobpg.v19.models import cart, currency
from csobpg.v19.request import PaymentInitRequest


def test_invalid_card_total_amount_rejected():
    """Test invalid card total amount rejected."""
    with pytest.raises(ValueError, match="requested total amount"):
        PaymentInitRequest(
            private_key="private_key",
            merchant_id="123456",
            order_no="2023-0001",
            total_amount=100,
            currency=currency.Currency.CZK,
            return_url="https://example.com/return",
            cart=cart.Cart(
                [
                    cart.CartItem(name="Item 1", quantity=1, amount=50),
                    cart.CartItem(name="Item 2", quantity=2, amount=60),
                ],
            ),
        )


def test_multi_quantity_cart_accepted():
    """Cart item amount is the line total, not the unit price."""
    PaymentInitRequest(
        private_key="private_key",
        merchant_id="123456",
        order_no="2023-0001",
        total_amount=300,
        currency=currency.Currency.CZK,
        return_url="https://example.com/return",
        cart=cart.Cart([cart.CartItem(name="Apples", quantity=2, amount=300)]),
    )
