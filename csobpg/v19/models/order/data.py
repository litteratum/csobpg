"""Order data."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from csobpg.v19 import signature as _s

if TYPE_CHECKING:
    from csobpg.v19.models.currency import Currency

    from .address import AddressData
    from .delivery import DeliveryData


class OrderType(Enum):
    """Order type."""

    PURCHASE = "purchase"
    BALANCE = "balance"
    PREPAID = "prepaid"
    CASH = "cash"
    CHECK = "check"


class OrderAvailability(Enum):
    """Order availability."""

    NOW = "now"
    PREORDER = "preorder"


class GiftCardsData(_s.SignedModel):
    """Gift cards data."""

    def __init__(
        self,
        total_amount: int | None = None,
        currency: Currency | None = None,
        quantity: int | None = None,
    ) -> None:
        self.total_amount = total_amount
        self.currency = currency
        self.quantity = quantity

    def as_json(self) -> dict:
        """Return gift cards data as JSON."""
        return {
            "totalAmount": self.total_amount,
            "quantity": self.quantity,
            "currency": self.currency.value if self.currency else None,
        }

    def _get_params_sequence(self) -> tuple:
        return (self.total_amount, self.currency, self.quantity)


class TrxUsage(Enum):
    """Specific transaction usage identified by the merchant."""

    CRYPTO = "crypto"
    NFT = "NFT"


class OrderData(_s.SignedModel):
    """Order data."""

    def __init__(
        self,
        order_type: OrderType | None = None,
        # TODO: or ISO8061 format, eg "YYYY-MM-DD".
        availability: OrderAvailability | None = None,
        delivery: DeliveryData | None = None,
        name_match: bool | None = None,
        address_match: bool | None = None,
        billing: AddressData | None = None,
        shipping: AddressData | None = None,
        shipping_added_at: str | None = None,
        reorder: bool | None = None,
        gift_cards: GiftCardsData | None = None,
        trx_usage: TrxUsage | None = None,
    ) -> None:
        """Init order data.

        :param shipping_added_at: shipping added time in ISO8061
        """
        self.order_type = order_type
        self.availability = availability
        self.delivery = delivery
        self.name_match = name_match
        self.address_match = address_match
        self.billing = billing
        self.shipping = shipping
        self.shipping_added_at = shipping_added_at
        self.reorder = reorder
        self.gift_cards = gift_cards
        self.trx_usage = trx_usage

    def as_json(self) -> dict:
        """Return order data as JSON."""
        return {
            "type": self.order_type.value if self.order_type else None,
            "availability": self.availability.value
            if self.availability
            else None,
            "delivery": self.delivery.indicator.value
            if self.delivery and self.delivery.indicator
            else None,
            "deliveryMode": self.delivery.mode.value
            if self.delivery and self.delivery.mode
            else None,
            "deliveryEmail": self.delivery.email if self.delivery else None,
            "nameMatch": self.name_match,
            "addressMatch": self.address_match,
            "billing": self.billing.as_json() if self.billing else None,
            "shipping": self.shipping.as_json() if self.shipping else None,
            "shippingAddedAt": self.shipping_added_at,
            "reorder": self.reorder,
            "giftcards": self.gift_cards.as_json()
            if self.gift_cards
            else None,
            "trxUsage": self.trx_usage.value if self.trx_usage else None,
        }

    def _get_params_sequence(self) -> tuple:
        return (
            self.order_type,
            self.availability,
            (self.delivery.indicator if self.delivery else None),
            (self.delivery.mode if self.delivery else None),
            self.delivery.email if self.delivery else None,
            self.name_match,
            self.address_match,
            self.billing,
            self.shipping,
            self.shipping_added_at,
            self.reorder,
            self.gift_cards,
            self.trx_usage,
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(order_type={self.order_type}, "
            f"availability={self.availability})"
        )
