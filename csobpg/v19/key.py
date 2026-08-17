"""RSA keys."""

from abc import ABC, abstractmethod
from pathlib import Path


class RSAKey(ABC):
    """RSA key."""

    @abstractmethod
    def __str__(self) -> str:
        """Return key object."""


class FileRSAKey(RSAKey):
    """RSA key from file."""

    def __init__(self, path: str) -> None:
        self.path = path

    def __str__(self) -> str:
        with Path(self.path).open(encoding="utf8") as file:
            return file.read()


class RAMRSAKey(FileRSAKey):
    """RAM cached RSA key."""

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self._key = None

    def __str__(self) -> str:
        if not self._key:
            self._key = super().__str__()

        return self._key
