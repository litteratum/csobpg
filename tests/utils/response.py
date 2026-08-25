"""Response utils."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from csobpg.v19.response.base import Response

_R = TypeVar("_R", bound="Response")


def build_response(response_cls: type[_R], body: dict) -> _R:
    """Build a response from its JSON body.

    Skips the signature verification `from_json` does, so that a wrong
    `to_sign_text` fails on the assertion instead of on the signature.
    """
    return response_cls._from_json(  # noqa: SLF001
        body,
        body.get("dttm", ""),
        body["resultCode"],
        body.get("resultMessage", ""),
    )
