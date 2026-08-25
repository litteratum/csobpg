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
        return {
            "auth": self.auth.value if self.auth else None,
            "authAt": self.auth_at,
            "authData": self.auth_data,
        }

    def _get_params_sequence(self) -> tuple:
        return (self.auth, self.auth_at, self.auth_data)
