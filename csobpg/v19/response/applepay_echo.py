"""Apple Pay echo response."""

from typing import Optional

from csobpg.v19.signature import SignedModel

from .base import Response


class ApplePayInitParams(SignedModel):
    """Apple Pay initialization parameters."""

    # pylint:disable=too-many-locals

    def __init__(
        self,
        country_code: str,
        supported_networks: list[str],
        merchant_capabilities: list[str],
    ):
        """Init ApplePay init params.

        :param country_code: ISO 3166-1 alpha-2 country code
        """
        self.country_code = country_code
        self.supported_networks = supported_networks
        self.merchant_capabilities = merchant_capabilities

    def _get_params_sequence(self):
        return (
            self.country_code,
            # TODO: perhaps it is better to be moved to the `to_sign_text`
            "|".join(self.supported_networks),
            "|".join(self.merchant_capabilities),
        )

    @classmethod
    def from_json(cls, response: dict) -> "ApplePayInitParams":
        """Return browser init result from JSON."""
        return cls(
            response["countryCode"],
            response["supportedNetworks"],
            response["merchantCapabilities"],
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"country_code={self.country_code}, "
            f"supported_networks={self.supported_networks}, "
            f"merchant_capabilities={self.merchant_capabilities}"
            f")"
        )


class ApplePayEchoResponse(Response):
    """Apple Pay echo response."""

    def __init__(
        self,
        dttm: str,
        result_code: int,
        result_message: str,
        init_params: Optional[ApplePayInitParams] = None,
    ):
        super().__init__(dttm, result_code, result_message)
        self.init_params = init_params

    @classmethod
    def _from_json(
        cls, response: dict, dttm: str, result_code: int, result_message: str
    ) -> "ApplePayEchoResponse":
        """Return payment process result from JSON."""
        return cls(
            dttm,
            result_code,
            result_message,
            (
                ApplePayInitParams.from_json(response["initParams"])
                if "initParams" in response
                else None
            ),
        )

    def _get_params_sequence(self) -> tuple:
        return (
            self.dttm,
            self.result_code,
            self.result_message,
            self.init_params,
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"dttm='{self.dttm}', "
            f"result_code={self.result_code}, "
            f"result_message='{self.result_message}'"
            f"init_params={self.init_params}"
            ")"
        )
