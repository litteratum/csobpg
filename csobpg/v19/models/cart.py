"""Cart models."""

from __future__ import annotations

from csobpg.v19 import signature as _s


class CartItem(_s.SignedModel):
    """Cart item."""

    def __init__(
        self,
        name: str,
        quantity: int,
        amount: int,
        description: str | None = None,
    ) -> None:
        """Init a cart item.

        :param amount: total amount (unit price * quantity)
        """
        self.name = name
        self.quantity = quantity
        self.amount = amount
        self.description = description

    def as_json(self) -> dict:
        """Return cart item as JSON."""
        return {
            "name": self.name,
            "quantity": self.quantity,
            "amount": self.amount,
            "description": self.description,
        }

    def _get_params_sequence(self) -> tuple:
        return (self.name, self.quantity, self.amount, self.description)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(name='{self.name}', "
            f"quantity={self.quantity}, amount={self.amount})"
        )


class Cart(_s.SignedModel):
    """Cart."""

    def __init__(self, items: list[CartItem]) -> None:
        """Init a cart."""
        self._items = items

        self.total_amount = sum(item.amount for item in self._items)

    def as_json(self) -> list[dict]:
        """Return cart as a JSON array."""
        return [item.as_json() for item in self._items]

    def _get_params_sequence(self) -> tuple:
        return tuple(item for item in self._items)

    def __str__(self) -> str:
        items_str = ", ".join(str(item) for item in self._items)
        return f"{self.__class__.__name__}[{items_str}]"
