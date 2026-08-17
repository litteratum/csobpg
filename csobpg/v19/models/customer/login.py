"""Customer login."""

from __future__ import annotations

from enum import Enum

from csobpg.v19 import signature as _s


class AuthMethod(Enum):
    """Auth method."""

    GUEST = "guest"
    ACCOUNT = "account"
    FEDERATED = "federated"
    ISSUER = "issuer"
    THIRD_PARTY = "thirdparty"
    FIDO = "fido"
    FIDO_SIGNED = "fido_signed"
    API = "api"


class LoginData(_s.SignedModel):
    """Customer login data."""

    def __init__(
        self,
        auth: AuthMethod | None = None,
        auth_at: str | None = None,
        auth_data: str | None = None,
    ):
        """Init login data.

        :param auth_at: auth time in ISO8061
        """
        self.auth = auth
        self.auth_at = auth_at
        self.auth_data = auth_data

    def as_json(self) -> dict:
        """Return login data as JSON."""
        result = {}
        if self.auth:
            result["auth"] = self.auth.value
        if self.auth_at:
            result["authAt"] = self.auth_at
        if self.auth_data:
            result["authData"] = self.auth_data
        return result

    def _get_params_sequence(self) -> tuple:
        return (self.auth, self.auth_at, self.auth_data)
