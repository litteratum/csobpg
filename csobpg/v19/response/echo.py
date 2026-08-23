"""Echo response."""

from __future__ import annotations

from .base import Response


class EchoResponse(Response):
    """Echo response."""

    @classmethod
    def _from_json(
        cls,
        response: dict,  # noqa: ARG003 (echo has no extra params)
        dttm: str,
        result_code: int,
        result_message: str,
    ) -> EchoResponse:
        """Return echo result from JSON."""
        return cls(dttm, result_code, result_message)

    def _get_params_sequence(self) -> tuple:
        return (self.dttm, self.result_code, self.result_message)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"dttm='{self.dttm}', "
            f"result_code={self.result_code}, "
            f"result_message='{self.result_message}'"
            ")"
        )
