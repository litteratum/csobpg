"""Module for building signatures."""

import binascii
import logging
from abc import ABC, abstractmethod
from base64 import b64decode, b64encode
from enum import Enum
from typing import Any

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from .errors import APIInvalidSignatureError

_LOGGER = logging.getLogger(__name__)


def _str_or_jsbool(val: Any) -> str:
    """Convert a value into string.

    If it is a bool, convert it to the string and lowercase it.
    If it is a SignedModel, convert it to the string by calling the
        `to_sign_text` method.
    If it is an Enum, get its value.
    If it is anything else, rely on the `str` function.
    """
    if isinstance(val, bool):
        return str(val).lower()
    if isinstance(val, Enum):
        return str(val.value)
    if isinstance(val, SignedModel):
        return val.to_sign_text()
    return str(val)


class SignedModel(ABC):
    """Signed model."""

    @abstractmethod
    def _get_params_sequence(self) -> tuple:
        """Return request parameters sequence."""

    def to_sign_text(self) -> str:
        """Convert request to sign text.

        This text then will be used to sign the request.
        """
        return "|".join(
            map(
                _str_or_jsbool,
                [
                    item
                    for item in self._get_params_sequence()
                    if item is not None
                ],
            )
        )


def sign(text: bytes, key: str) -> str:
    """Sign the text with the given key."""
    _LOGGER.debug('Signing "%s"', text)
    key = RSA.importKey(key)  # type: ignore
    hasher = SHA256.new(text)
    signer = PKCS1_v1_5.new(key)  # type: ignore
    return b64encode(signer.sign(hasher)).decode()


def verify(signature: str, text: bytes, key: str) -> None:
    """Verify data.

    :param signature: signature to verify
    :param text: text to sign and verify against the signature
    :param key: public key to verify the signature
    """
    _LOGGER.debug('Verifying "%s" against "%s"', signature, text)
    key = RSA.importKey(key)  # type: ignore
    hasher = SHA256.new(text)
    verifier = PKCS1_v1_5.new(key)  # type: ignore

    try:
        sig_as_bytes = b64decode(signature)
    except binascii.Error as exc:
        raise APIInvalidSignatureError(
            f"Failed to decode base64: {exc}"
        ) from exc

    # pylint:disable=not-callable
    if not verifier.verify(hasher, sig_as_bytes):
        raise APIInvalidSignatureError("Invalid signature")
