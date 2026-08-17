"""Fields."""

from __future__ import annotations

from abc import ABC, abstractmethod


class _Field(ABC):
    """API request field."""

    def __init__(self) -> None:
        self.private_name = ""
        self.public_name = ""

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        """Validate a value."""


class _StrField(_Field):
    def __init__(self, max_length: int | None = None) -> None:
        self.max_length = max_length
        super().__init__()

    def validate(self, value: str | None):
        if (
            self.max_length is not None
            and value
            and len(value) > self.max_length
        ):
            raise ValueError(
                f"{self.public_name} should be <= {self.max_length}",
            )


class _IntField(_Field):
    def __init__(
        self,
        min_value: int | None = None,
        max_value: int | None = None,
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value
        super().__init__()

    def validate(self, value: int | None):
        if (
            self.min_value is not None
            and value is not None
            and value < self.min_value
        ):
            raise ValueError(
                f"{self.public_name} should be >= {self.min_value}",
            )
        if (
            self.max_value is not None
            and value is not None
            and value > self.max_value
        ):
            raise ValueError(
                f"{self.public_name} should be <= {self.max_value}",
            )
