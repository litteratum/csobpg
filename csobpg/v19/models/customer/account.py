"""Customer account."""

from typing import Optional

from ...signature import SignedModel
from ..fields import _IntField


class AccountData(SignedModel):
    """Customer account data."""

    order_history = _IntField(min_value=0, max_value=9999)
    payment_day = _IntField(min_value=0, max_value=999)
    payment_year = _IntField(min_value=0, max_value=999)
    oneclick_adds = _IntField(min_value=0, max_value=999)

    def __init__(
        self,
        created_at: Optional[str] = None,
        changed_at: Optional[str] = None,
        changed_pwd_at: Optional[str] = None,
        order_history: Optional[int] = None,
        payment_day: Optional[int] = None,
        payment_year: Optional[int] = None,
        oneclick_adds: Optional[int] = None,
        suspicious: Optional[bool] = None,
    ) -> None:
        """Init account data.

        :param created_at: created time in ISO8061
        :param changed_at: changed time in ISO8061
        :param changed_pwd_at: password change time in ISO8061
        """
        # pylint:disable=too-many-arguments
        self.created_at = created_at
        self.changed_at = changed_at
        self.changed_pwd_at = changed_pwd_at
        self.order_history = order_history
        self.payment_day = payment_day
        self.payment_year = payment_year
        self.oneclick_adds = oneclick_adds
        self.suspicious = suspicious

    def as_json(self) -> dict:
        """Return account data as JSON."""
        result = {}
        if self.created_at:
            result["createdAt"] = self.created_at
        if self.changed_at:
            result["changedAt"] = self.changed_at
        if self.changed_pwd_at:
            result["changedPwdAt"] = self.changed_pwd_at
        if self.order_history:
            result["orderHistory"] = self.order_history
        if self.payment_day:
            result["paymentDay"] = self.payment_day
        if self.payment_year:
            result["paymentYear"] = self.payment_year
        if self.oneclick_adds:
            result["oneclickAdds"] = self.oneclick_adds
        if self.suspicious:
            result["suspicious"] = self.suspicious
        return result

    def _get_params_sequence(self) -> tuple:
        return (
            self.created_at,
            self.changed_at,
            self.changed_pwd_at,
            self.order_history,
            self.payment_day,
            self.payment_year,
            self.oneclick_adds,
            self.suspicious,
        )
