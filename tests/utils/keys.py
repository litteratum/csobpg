"""Keys used by the signing tests."""

from pathlib import Path

PRIVATE_KEY_PATH = "tests/v19/data/merchant.key"

with Path(PRIVATE_KEY_PATH).open(encoding="utf8") as f:
    PRIVATE_KEY = f.read()
