"""Tests config."""

from pathlib import Path

KEY_PATH = "tests/keys/key.key"
with Path(KEY_PATH).open(encoding="utf8") as f:
    KEY = f.read()
