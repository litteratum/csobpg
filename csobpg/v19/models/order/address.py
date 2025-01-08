"""Address data."""

from typing import Optional

from ...signature import SignedModel
from ..fields import _StrField


class AddressData(SignedModel):
    """Address data."""

    address = _StrField(max_length=50)
    city = _StrField(max_length=50)
    zip = _StrField(max_length=16)
    address2 = _StrField(max_length=50)
    address3 = _StrField(max_length=50)

    def __init__(
        self,
        address: str,
        country: str,  # TODO: ISO 3166-1 alpha-3, eg CZE.
        city: str,
        zip_code: str,
        state: Optional[str] = None,  # TODO: ISO 3166-2.
        address2: Optional[str] = None,
        address3: Optional[str] = None,
    ) -> None:
        # pylint:disable=too-many-arguments
        self.address = address
        self.country = country
        self.city = city
        self.zip = zip_code
        self.state = state
        self.address2 = address2
        self.address3 = address3

    def as_json(self) -> dict:
        """Return address data as JSON."""
        return {
            "address1": self.address,
            "address2": self.address2,
            "address3": self.address3,
            "city": self.city,
            "zip": self.zip,
            "state": self.state,
            "country": self.country,
        }

    def _get_params_sequence(self) -> tuple:
        return (
            self.address,
            self.address2,
            self.address3,
            self.city,
            self.zip,
            self.state,
            self.country,
        )
