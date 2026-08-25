"""Signature utils.

The gateway rebuilds TEXT_TO_SIGN from the request it receives, so
what a request signs must be exactly what it sends: "All parameters
sent in the request are included in the list. If any of the optional
parameters is not added, it will not appear in the resulting compiled
chain".
"""

from __future__ import annotations

import collections as _collections
from typing import Any


def ensure_text_to_sign_equals_json_body(
    text_to_sign: str,
    json_body: dict,
) -> None:
    """Ensure text_to_sign carries exactly the values sent in json_body.

    Compares the two as multisets of values: every value sent must be
    signed, and every value signed must be sent. Position is not checked,
    so assert the full text_to_sign separately to pin the field order.

    On mismatch the report names the JSON path of every value sent and,
    for every value signed, its text_to_sign index and neighbours. An
    unbalanced value can be traced back to the field that produced it: a
    value missing from the body has no path, so its signed neighbours
    identify the field the body dropped.
    """
    body = {key: val for key, val in json_body.items() if key != "signature"}

    sent = _flatten_json_vals(body)
    signed = text_to_sign.split("|")

    sent_counts = _collections.Counter(val for _, val in sent)
    signed_counts = _collections.Counter(signed)

    if sent_counts == signed_counts:
        return

    problems = [
        _describe(val, sent, signed)
        for val in sorted(set(sent_counts) | set(signed_counts))
        if sent_counts[val] != signed_counts[val]
    ]
    raise AssertionError(
        "text_to_sign does not match the JSON body:\n" + "\n".join(problems),
    )


def _describe(
    val: str,
    sent: list[tuple[str, str]],
    signed: list[str],
) -> str:
    """Report where a value is sent in the body and signed in the text."""
    paths = [path for path, item in sent if item == val]
    indexes = [index for index, item in enumerate(signed) if item == val]

    lines = [
        f"  {val!r} sent {len(paths)}x, signed {len(indexes)}x",
        f"    sent at:   {', '.join(paths) or '<nothing>'}",
    ]

    if not indexes:
        lines.append("    signed at: <nowhere>")
        return "\n".join(lines)

    contexts = [f"[{index}] {_context(signed, index)}" for index in indexes]
    lines.append(f"    signed at: {contexts[0]}")
    lines.extend(f"               {context}" for context in contexts[1:])
    return "\n".join(lines)


def _context(signed: list[str], index: int) -> str:
    """Show a signed value together with its neighbours."""
    before = signed[index - 1] if index else "^"
    after = signed[index + 1] if index + 1 < len(signed) else "$"
    return f"{before}|>{signed[index]}<|{after}"


def _flatten_json_vals(body: dict) -> list[tuple[str, str]]:
    """Flatten a json body into (path, value) pairs."""
    result: list[tuple[str, str]] = []

    for key, val in body.items():
        result.extend(_flatten_val(key, val))

    return result


def _flatten_val(path: str, val: Any) -> list[tuple[str, str]]:
    """Flatten a single json value into (path, value) pairs."""
    if isinstance(val, bool):
        return [(path, str(val).lower())]

    if isinstance(val, dict):
        return [
            pair
            for key, item in val.items()
            for pair in _flatten_val(f"{path}.{key}", item)
        ]

    if isinstance(val, list):
        return [
            pair
            for index, item in enumerate(val)
            for pair in _flatten_val(f"{path}[{index}]", item)
        ]

    return [(path, str(val))]
