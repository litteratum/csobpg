"""Fingerprint model."""

from typing import Optional

from ..signature import SignedModel


class SDK(SignedModel):
    """SDK."""

    def __init__(
        self,
        max_timeout: int,
        reference_number: str,
        transaction_id: str,
        app_id: Optional[str] = None,
        enc_data: Optional[str] = None,
        ephem_pub_key: Optional[str] = None,
    ) -> None:
        self.max_timeout = max_timeout
        self.reference_number = reference_number
        self.transaction_id = transaction_id
        self.app_id = app_id
        self.enc_data = enc_data
        self.ephem_pub_key = ephem_pub_key

    def _get_params_sequence(self) -> tuple:
        return (
            self.app_id,
            self.enc_data,
            self.ephem_pub_key,
            self.max_timeout,
            self.reference_number,
            self.transaction_id,
        )

    def as_json(self) -> dict:
        """Return SDK as JSON."""
        return {
            "appId": self.app_id,
            "encData": self.enc_data,
            "ephemPubKey": self.ephem_pub_key,
            "maxTimeout": self.max_timeout,
            "referenceNumber": self.reference_number,
            "transID": self.transaction_id,
        }


class Browser(SignedModel):
    """Browser."""

    def __init__(
        self,
        user_agent: str,
        accept_header: str,
        language: str,
        js_enabled: bool,
        color_depth: Optional[int] = None,
        screen_height: Optional[int] = None,
        screen_width: Optional[int] = None,
        timezone: Optional[float] = None,
        java_enabled: Optional[bool] = None,
        challenge_window_size: Optional[str] = None,
    ) -> None:
        self.user_agent = user_agent
        self.accept_header = accept_header
        self.language = language
        self.js_enabled = js_enabled
        self.color_depth = color_depth
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.timezone = timezone
        self.java_enabled = java_enabled
        self.challenge_window_size = challenge_window_size

    def _get_params_sequence(self) -> tuple:
        return (
            self.user_agent,
            self.accept_header,
            self.language,
            self.js_enabled,
            self.color_depth,
            self.screen_height,
            self.screen_width,
            self.timezone,
            self.java_enabled,
            self.challenge_window_size,
        )

    def as_json(self) -> dict:
        """Return browser as JSON."""
        result = {
            "userAgent": self.user_agent,
            "acceptHeader": self.accept_header,
            "language": self.language,
            "javascriptEnabled": self.js_enabled,
        }

        if self.color_depth:
            result["colorDepth"] = self.color_depth
        if self.screen_height:
            result["screenHeight"] = self.screen_height
        if self.screen_width:
            result["screenWidth"] = self.screen_width
        if self.timezone:
            result["timezone"] = self.timezone
        if self.java_enabled:
            result["javaEnabled"] = self.java_enabled
        if self.challenge_window_size:
            result["challengeWindowSize"] = self.challenge_window_size

        return result


class Fingerprint(SignedModel):
    """Fingerprint."""

    def __init__(
        self, browser: Optional[Browser] = None, sdk: Optional[SDK] = None
    ) -> None:
        super().__init__()
        self.browser = browser
        self.sdk = sdk

    def _get_params_sequence(self) -> tuple:
        return (self.browser, self.sdk)

    def as_json(self) -> dict:
        """Return fingerprint as JSON."""
        result = {}

        if self.browser:
            result["browser"] = self.browser.as_json()
        if self.sdk:
            result["sdk"] = self.sdk.as_json()

        return result
