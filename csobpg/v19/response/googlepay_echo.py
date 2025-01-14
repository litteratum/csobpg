"""Google Pay echo response."""

from typing import List, Optional

from csobpg.v19.signature import SignedModel

from .base import Response


class GooglePayInitParams(SignedModel):
    """Google Pay initialization parameters."""

    # pylint:disable=too-many-locals

    def __init__(
        self,
        api_version: int,
        api_version_minor: int,
        payment_method_type: str,
        allowed_card_networks: List[str],
        allowed_card_auth_methods: List[str],
        assurance_details_required: bool,
        billing_address_required: bool,
        billing_address_parameters_format: str,
        tokenization_specification_type: str,
        gateway: str,
        gateway_merchant_id: str,
        googlepay_merchant_id: str,
        merchant_name: str,
        environment: str,
        total_price_status: str,
        country_code: str,
    ):
        self.api_version = api_version
        self.api_version_minor = api_version_minor
        self.payment_method_type = payment_method_type
        self.allowed_card_networks = allowed_card_networks
        self.allowed_card_auth_methods = allowed_card_auth_methods
        self.assurance_details_required = assurance_details_required
        self.billing_address_required = billing_address_required
        self.billing_address_parameters_format = (
            billing_address_parameters_format
        )
        self.tokenization_specification_type = tokenization_specification_type
        self.gateway = gateway
        self.gateway_merchant_id = gateway_merchant_id
        self.googlepay_merchant_id = googlepay_merchant_id
        self.merchant_name = merchant_name
        self.environment = environment
        self.total_price_status = total_price_status
        self.country_code = country_code

    def _get_params_sequence(self):
        return (
            self.api_version,
            self.api_version_minor,
            self.payment_method_type,
            # TODO: perhaps it is better to be moved to the `to_sign_text`
            "|".join(self.allowed_card_networks),
            "|".join(self.allowed_card_auth_methods),
            self.assurance_details_required,
            self.billing_address_required,
            self.billing_address_parameters_format,
            self.tokenization_specification_type,
            self.gateway,
            self.gateway_merchant_id,
            self.googlepay_merchant_id,
            self.merchant_name,
            self.environment,
            self.total_price_status,
            self.country_code,
        )

    @classmethod
    def from_json(cls, response: dict) -> "GooglePayInitParams":
        """Return browser init result from JSON."""
        return cls(
            response["apiVersion"],
            response["apiVersionMinor"],
            response["paymentMethodType"],
            response["allowedCardNetworks"],
            response["allowedCardAuthMethods"],
            response["assuranceDetailsRequired"],
            response["billingAddressRequired"],
            response["billingAddressParametersFormat"],
            response["tokenizationSpecificationType"],
            response["gateway"],
            response["gatewayMerchantId"],
            response["googlepayMerchantId"],
            response["merchantName"],
            response["environment"],
            response["totalPriceStatus"],
            response["countryCode"],
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"api_version={self.api_version}, "
            f"api_version_minor={self.api_version_minor}, "
            f"payment_method_type={self.payment_method_type}, "
            f"allowed_card_networks={self.allowed_card_networks}, "
            f"allowed_card_auth_methods={self.allowed_card_auth_methods}, "
            f"assurance_details_required={self.assurance_details_required}, "
            f"billing_address_required={self.billing_address_required}, "
            f"billing_address_parameters_format={self.billing_address_parameters_format}, "
            f"tokenization_specification_type={self.tokenization_specification_type}, "
            f"gateway={self.gateway}, "
            f"gateway_merchant_id={self.gateway_merchant_id}, "
            f"googlepay_merchant_id={self.googlepay_merchant_id}, "
            f"merchant_name={self.merchant_name}, "
            f"environment={self.environment}, "
            f"total_price_status={self.total_price_status}, "
            f"country_code={self.country_code}"
            f")"
        )


class GooglePayEchoResponse(Response):
    """Google Pay echo response."""

    def __init__(
        self,
        dttm: str,
        result_code: int,
        result_message: str,
        init_params: Optional[GooglePayInitParams] = None,
    ):
        super().__init__(dttm, result_code, result_message)
        self.init_params = init_params

    @classmethod
    def _from_json(
        cls, response: dict, dttm: str, result_code: int, result_message: str
    ) -> "GooglePayEchoResponse":
        """Return payment process result from JSON."""
        return cls(
            dttm,
            result_code,
            result_message,
            (
                GooglePayInitParams.from_json(response["initParams"])
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
