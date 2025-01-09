"""Customer login."""

from enum import Enum
from typing import Optional

from ...signature import SignedModel


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


class LoginData(SignedModel):
    """Customer login data."""

    def __init__(
        self,
        auth: Optional[AuthMethod] = None,
        auth_at: Optional[str] = None,
        auth_data: Optional[str] = None,
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
