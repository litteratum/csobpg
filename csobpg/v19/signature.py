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
    If it is an Enum, get its value and convert it to string.
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
        """Return the model's parameters sequence.

        Must return all params as-is.
        """

    def _to_sign_parts(self) -> list:
        """Return the parts the model contributes to the sign text.

        A nested model contributes its own parts rather than its joined
        text. Joining first would conflate a model with no set fields
        with a model whose only set field is an empty string: both render
        as "", but the first must contribute nothing while the second
        must contribute one empty part.
        """
        parts = []

        for item in self._get_params_sequence():
            if item is None:
                continue
            if isinstance(item, SignedModel):
                parts.extend(item._to_sign_parts())  # noqa: SLF001
                continue
            if isinstance(item, list):
                parts.extend(
                    [_str_or_jsbool(i) for i in item],
                )
                continue
            # NOTE: this is our guess. It is not documented by the API
            if isinstance(item, dict):
                parts.extend(
                    [_str_or_jsbool(i) for i in item.values()],
                )
                continue

            parts.append(_str_or_jsbool(item))

        return parts

    def to_sign_text(self) -> str:
        """Convert the model to sign text."""
        return "|".join(self._to_sign_parts())


def sign(text: bytes, key: str) -> str:
    """Sign the text with the given key."""
    _LOGGER.debug('Signing "%s"', text)
    key = RSA.importKey(key)
    hasher = SHA256.new(text)
    signer = PKCS1_v1_5.new(key)
    return b64encode(signer.sign(hasher)).decode()


def verify(signature: str, text: bytes, key: str) -> None:
    """Verify data.

    :param signature: signature to verify
    :param text: text to sign and verify against the signature
    :param key: public key to verify the signature
    """
    _LOGGER.debug('Verifying "%s" against "%s"', signature, text)
    key = RSA.importKey(key)
    hasher = SHA256.new(text)
    verifier = PKCS1_v1_5.new(key)

    try:
        sig_as_bytes = b64decode(signature)
    except binascii.Error as exc:
        raise APIInvalidSignatureError(
            f"Failed to decode base64: {exc}",
        ) from exc

    if not verifier.verify(hasher, sig_as_bytes):
        raise APIInvalidSignatureError("Invalid signature")
