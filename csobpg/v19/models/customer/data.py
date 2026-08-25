"""Customer data."""

from __future__ import annotations

from typing import TYPE_CHECKING

from csobpg.v19 import signature as _s

if TYPE_CHECKING:
    from .account import AccountData
    from .login import LoginData


class PhoneNumber:
    """Phone number."""

    def __init__(self, prefix: str, subscriber: str) -> None:
        """Phone number in format <prefix>.<subscriber>."""
        self.prefix = prefix
        self.subscriber = subscriber

    def __str__(self) -> str:
        return f"{self.prefix}.{self.subscriber}"


class CustomerData(_s.SignedModel):
    """Customer information."""

    def __init__(
        self,
        name: str | None = None,
        email: str | None = None,
        home_phone: PhoneNumber | None = None,
        work_phone: PhoneNumber | None = None,
        mobile_phone: PhoneNumber | None = None,
        account: AccountData | None = None,
        login: LoginData | None = None,
    ) -> None:
        self.name = name
        self.email = email
        self.home_phone = home_phone
        self.work_phone = work_phone
        self.mobile_phone = mobile_phone
        self.account = account
        self.login = login

    def as_json(self) -> dict:
        """Return customer data as JSON."""
        return {
            "name": self.name,
            "email": self.email,
            "homePhone": str(self.home_phone) if self.home_phone else None,
            "workPhone": str(self.work_phone) if self.work_phone else None,
            "mobilePhone": str(self.mobile_phone)
            if self.mobile_phone
            else None,
            "account": self.account.as_json() if self.account else None,
            "login": self.login.as_json() if self.login else None,
        }

    def _get_params_sequence(self) -> tuple:
        return (
            self.name,
            self.email,
            self.home_phone,
            self.work_phone,
            self.mobile_phone,
            self.account,
            self.login,
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(name='{self.name}', "
            f"email='{self.email}', mobile_phone={self.mobile_phone})"
        )
