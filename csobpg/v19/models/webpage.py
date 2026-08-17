"""Webpage models."""

from __future__ import annotations

from enum import Enum


class WebPageLanguage(Enum):
    """PG web page language."""

    CS = "cs"
    EN = "en"
    DE = "de"
    FR = "fr"
    HU = "hu"
    IT = "it"
    JA = "ja"
    PL = "pl"
    PT = "pt"
    RO = "ro"
    RU = "ru"
    SK = "sk"
    ES = "es"
    TR = "tr"
    VI = "vi"
    HR = "hr"
    SL = "sl"
    SV = "sv"


class WebPageAppearanceConfig:
    """PG web page appearance configuration."""

    def __init__(
        self,
        language: WebPageLanguage = WebPageLanguage.CS,
        logo_version: int | None = None,
        color_scheme_version: int | None = None,
    ) -> None:
        self.language = language
        self.logo_version = logo_version
        self.color_scheme_version = color_scheme_version
