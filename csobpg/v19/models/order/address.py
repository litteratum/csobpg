"""Address data."""

from __future__ import annotations

from csobpg.v19 import signature as _s


class AddressData(_s.SignedModel):
    """Address data."""

    def __init__(
        self,
        address: str,
        country: str,
        city: str,
        zip_code: str,
        state: str | None = None,
        address2: str | None = None,
        address3: str | None = None,
    ) -> None:
        """Init address data.

        :param country: country in ISO 3166-1 alpha-3 (e.g. CZE)
        :param state: state in ISO 3166-2
        """
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
