"""Order data."""

from enum import Enum
from typing import Optional

from ...signature import SignedModel
from ..currency import Currency
from ..fields import _IntField
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


class GiftCardsData(SignedModel):
    """Gift cards data."""

    quantity = _IntField(min_value=1, max_value=99)

    def __init__(
        self,
        total_amount: Optional[int] = None,
        currency: Optional[Currency] = None,
        quantity: Optional[int] = None,
    ) -> None:
        self.total_amount = total_amount
        self.currency = currency
        self.quantity = quantity

    def as_json(self) -> dict:
        """Return gift cards data as JSON."""
        body = {
            "totalAmount": self.total_amount,
            "quantity": self.quantity,
        }
        if self.currency:
            body["currency"] = self.currency.value
        return body

    def _get_params_sequence(self) -> tuple:
        return (self.total_amount, self.currency, self.quantity)


class OrderData(SignedModel):
    """Order data."""

    def __init__(
        self,
        order_type: Optional[OrderType] = None,
        availability: Optional[
            OrderAvailability
        ] = None,  # TODO: or ISO8061 format, eg "YYYY-MM-DD".
        delivery: Optional[DeliveryData] = None,
        name_match: Optional[bool] = None,
        address_match: Optional[bool] = None,
        billing: Optional[AddressData] = None,
        shipping: Optional[AddressData] = None,
        shipping_added_at: Optional[str] = None,
        reorder: Optional[bool] = None,
        gift_cards: Optional[GiftCardsData] = None,
    ) -> None:
        """Init order data.

        :param shipping_added_at: shipping added time in ISO8061
        """
        # pylint:disable=too-many-arguments
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

    def as_json(self) -> dict:
        # pylint:disable=too-many-branches
        """Return order data as JSON."""
        body = {}
        if self.order_type:
            body["type"] = self.order_type.value
        if self.availability:
            body["availability"] = self.availability.value
        if self.delivery:
            if self.delivery.indicator:
                body["delivery"] = self.delivery.indicator.value
            if self.delivery.mode:
                body["deliveryMode"] = self.delivery.mode.value
            if self.delivery.email:
                body["deliveryEmail"] = self.delivery.email
        if self.name_match is not None:
            body["nameMatch"] = self.name_match
        if self.address_match is not None:
            body["addressMatch"] = self.address_match
        if self.billing:
            body["billing"] = self.billing.as_json()
        if self.shipping:
            body["shipping"] = self.shipping.as_json()
        if self.shipping_added_at:
            body["shippingAddedAt"] = self.shipping_added_at
        if self.reorder is not None:
            body["reorder"] = self.reorder
        if self.gift_cards:
            body["giftCards"] = self.gift_cards.as_json()
        return body

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
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(order_type={self.order_type}, "
            f"availability={self.availability})"
        )
