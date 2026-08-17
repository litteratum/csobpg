"""OneClick echo response."""

from .base import Response


class OneClickEchoResponse(Response):
    """OneClick echo response."""

    def __init__(
        self,
        template_id: str,
        dttm: str,
        result_code: int,
        result_message: str,
    ):
        super().__init__(dttm, result_code, result_message)
        self.template_id = template_id

    @classmethod
    def _from_json(
        cls,
        response: dict,
        dttm: str,
        result_code: int,
        result_message: str,
    ) -> "OneClickEchoResponse":
        """Return payment process result from JSON."""
        return cls(response["origPayId"], dttm, result_code, result_message)

    def _get_params_sequence(self) -> tuple:
        return (
            self.template_id,
            self.dttm,
            self.result_code,
            self.result_message,
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"template_id='{self.template_id}', "
            f"dttm='{self.dttm}', "
            f"result_code={self.result_code}, "
            f"result_message='{self.result_message}'"
            ")"
        )
