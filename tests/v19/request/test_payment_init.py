"""Tests for the payment init request."""

import pytest

from csobpg.v19.models import cart as _cart
from csobpg.v19.models import currency as _currency
from csobpg.v19.models import customer as _customer
from csobpg.v19.models import order as _order
from csobpg.v19.models import payment as _payment
from csobpg.v19.models import webpage as _webpage
from csobpg.v19.request import PaymentInitRequest
from tests.utils import keys as _keys_util
from tests.utils import signature as _sig_util


def test_to_sign_text():
    """Test to_sign_text method."""
    request = PaymentInitRequest(
        merchant_id="mid",
        private_key=_keys_util.PRIVATE_KEY,
        order_no="oid",
        total_amount=250,
        return_url="rurl",
        return_method=_payment.ReturnMethod.POST,
        payment_operation=_payment.PaymentOperation.PAYMENT,
        payment_method=_payment.PaymentMethod.CARD,
        currency=_currency.Currency.CZK,
        close_payment=True,
        ttl_sec=600,
        cart=_cart.Cart(
            [
                _cart.CartItem(
                    name="i1",
                    quantity=1,
                    amount=100,
                    description="i1d",
                ),
                _cart.CartItem(
                    name="i2",
                    quantity=2,
                    amount=150,
                    description="i2d",
                ),
            ],
        ),
        customer=_customer.CustomerData(
            name="John Doe",
            email="example.com",
            home_phone=_customer.PhoneNumber(
                prefix="+420",
                subscriber="123456789",
            ),
            work_phone=_customer.PhoneNumber(
                prefix="+420",
                subscriber="987654321",
            ),
            mobile_phone=_customer.PhoneNumber(
                prefix="+420",
                subscriber="555555555",
            ),
            account=_customer.AccountData(
                created_at="2023-01-01T00:00:00Z",
                changed_at="2023-01-02T00:00:00Z",
                changed_pwd_at="2023-01-03T00:00:00Z",
                order_history=1,
                payment_day=1,
                payment_year=1,
                oneclick_adds=1,
                suspicious=False,
            ),
            login=_customer.LoginData(
                auth=_customer.AuthMethod.FEDERATED,
                auth_at="2023-01-01T00:00:00Z",
                auth_data="any",
            ),
        ),
        order=_order.OrderData(
            _order.OrderType.CASH,
            _order.OrderAvailability.PREORDER,
            delivery=_order.DeliveryData(
                indicator=_order.DeliveryIndicator.OTHER,
                mode=_order.DeliveryMode.LATER,
                email="dem",
            ),
            name_match=False,
            address_match=False,
            billing=_order.AddressData(
                address="ba",
                country="CZ",
                city="Prague",
                zip_code="11000",
                state="Prague",
                address2="ba2",
                address3="ba3",
            ),
            shipping=_order.AddressData(
                address="sa",
                country="CZ",
                city="Prague",
                zip_code="11000",
                state="Prague",
                address2="sa2",
                address3="sa3",
            ),
            shipping_added_at="2023-01-01T00:00:00Z",
            reorder=False,
            gift_cards=_order.GiftCardsData(
                total_amount=100,
                currency=_currency.Currency.CZK,
                quantity=2,
            ),
        ),
        merchant_data=b"Hello, World!",
        customer_id="cid",
        payment_expiry=100,
        page_appearance=_webpage.WebPageAppearanceConfig(
            language=_webpage.WebPageLanguage.CS,
            logo_version=2,
            color_scheme_version=3,
        ),
    )

    dttm = request.dttm
    expiry = request.payment_expiry
    sign_text = request.to_sign_text()

    assert sign_text == (
        f"mid|oid|{dttm}|payment|card|250|CZK|true|rurl|POST|i1|1|100|"
        "i1d|i2|2|150|i2d|John Doe|example.com|+420.123456789|+420.987654321|"
        "+420.555555555|2023-01-01T00:00:00Z|2023-01-02T00:00:00Z|"
        "2023-01-03T00:00:00Z|1|1|1|1|false|federated|2023-01-01T00:00:00Z|"
        "any|cash|preorder|other|3|dem|false|false|ba|ba2|ba3|Prague|11000|"
        "Prague|CZ|sa|sa2|sa3|Prague|11000|Prague|CZ|2023-01-01T00:00:00Z|"
        f"false|100|CZK|2|SGVsbG8sIFdvcmxkIQ==|cid|cs|600|2|3|{expiry}"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(
        sign_text,
        request.to_json(),
    )


def test_invalid_card_total_amount_rejected():
    """Test invalid card total amount rejected."""
    with pytest.raises(ValueError, match="requested total amount"):
        PaymentInitRequest(
            private_key="private_key",
            merchant_id="123456",
            order_no="2023-0001",
            total_amount=100,
            currency=_currency.Currency.CZK,
            return_url="https://example.com/return",
            cart=_cart.Cart(
                [
                    _cart.CartItem(name="Item 1", quantity=1, amount=50),
                    _cart.CartItem(name="Item 2", quantity=2, amount=60),
                ],
            ),
        )


def test_multi_quantity_cart_accepted():
    """Cart item amount is the line total, not the unit price."""
    PaymentInitRequest(
        private_key="private_key",
        merchant_id="123456",
        order_no="2023-0001",
        total_amount=300,
        currency=_currency.Currency.CZK,
        return_url="https://example.com/return",
        cart=_cart.Cart(
            [_cart.CartItem(name="Apples", quantity=2, amount=300)],
        ),
    )


def _minimal_request(**kwargs) -> PaymentInitRequest:
    """Return a request with only the mandatory params set."""
    return PaymentInitRequest(
        merchant_id="mid",
        private_key=_keys_util.PRIVATE_KEY,
        order_no="oid",
        total_amount=100,
        return_url="rurl",
        **kwargs,
    )


def _minimal_sign_text(dttm: str) -> str:
    """Return the sign text of a bare `_minimal_request`."""
    return (
        f"mid|oid|{dttm}|payment|card|100|CZK|true|rurl|POST|"
        "Payment|1|100|cs|600"
    )


def test_empty_customer_is_not_signed_nor_sent():
    """Test an all-unset customer being neither signed nor sent."""
    request = _minimal_request(customer=_customer.CustomerData())
    sign_text = request.to_sign_text()
    json_body = request.to_json()

    assert sign_text == _minimal_sign_text(request.dttm)
    assert "customer" not in json_body
    _sig_util.ensure_text_to_sign_equals_json_body(sign_text, json_body)


def test_empty_order_is_not_signed_nor_sent():
    """Test an all-unset order being neither signed nor sent."""
    request = _minimal_request(order=_order.OrderData())
    sign_text = request.to_sign_text()
    json_body = request.to_json()

    assert sign_text == _minimal_sign_text(request.dttm)
    assert "order" not in json_body
    _sig_util.ensure_text_to_sign_equals_json_body(sign_text, json_body)


def test_unset_nested_fields_are_not_sent():
    """Test the unset nested fields not being sent as nulls."""
    request = _minimal_request(
        order=_order.OrderData(
            billing=_order.AddressData(
                address="a",
                country="CZE",
                city="c",
                zip_code="1",
            ),
            gift_cards=_order.GiftCardsData(
                currency=_currency.Currency.CZK,
            ),
        ),
    )
    sign_text = request.to_sign_text()
    json_body = request.to_json()

    assert sign_text == (
        f"mid|oid|{request.dttm}|payment|card|100|CZK|true|rurl|POST|"
        "Payment|1|100|a|c|1|CZE|CZK|cs|600"
    )
    assert json_body["order"] == {
        "billing": {
            "address1": "a",
            "city": "c",
            "zip": "1",
            "country": "CZE",
        },
        "giftcards": {"currency": "CZK"},
    }
    _sig_util.ensure_text_to_sign_equals_json_body(sign_text, json_body)


def test_customer_with_only_an_empty_field_is_signed():
    """Test an empty string field being both signed and sent."""
    request = _minimal_request(customer=_customer.CustomerData(name=""))
    sign_text = request.to_sign_text()
    json_body = request.to_json()

    assert json_body["customer"] == {"name": ""}
    assert sign_text == (
        f"mid|oid|{request.dttm}|payment|card|100|CZK|true|rurl|POST|"
        "Payment|1|100||cs|600"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(sign_text, json_body)


def test_deeply_nested_only_empty_field_is_signed():
    """Test an empty string field being signed through two nested models."""
    request = _minimal_request(
        customer=_customer.CustomerData(
            login=_customer.LoginData(auth_data=""),
        ),
    )
    sign_text = request.to_sign_text()
    json_body = request.to_json()

    assert json_body["customer"] == {"login": {"authData": ""}}
    assert sign_text == (
        f"mid|oid|{request.dttm}|payment|card|100|CZK|true|rurl|POST|"
        "Payment|1|100||cs|600"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(sign_text, json_body)


def test_order_with_only_an_empty_field_is_signed():
    """Test an empty string reaching the order through delivery."""
    request = _minimal_request(
        order=_order.OrderData(delivery=_order.DeliveryData(email="")),
    )
    sign_text = request.to_sign_text()
    json_body = request.to_json()

    assert json_body["order"] == {"deliveryEmail": ""}
    assert sign_text == (
        f"mid|oid|{request.dttm}|payment|card|100|CZK|true|rurl|POST|"
        "Payment|1|100||cs|600"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(sign_text, json_body)


def test_two_empty_fields_are_signed():
    """Test two empty string fields being signed as two empty parts.

    This is the neighbour of the cases above that already holds: two
    empty parts join into "|", which is not falsy, so the model survives
    into the signature. A fix for the single-part case must keep it.
    """
    request = _minimal_request(
        customer=_customer.CustomerData(
            login=_customer.LoginData(auth_at="", auth_data=""),
        ),
    )
    sign_text = request.to_sign_text()
    json_body = request.to_json()

    assert json_body["customer"] == {"login": {"authAt": "", "authData": ""}}
    assert sign_text == (
        f"mid|oid|{request.dttm}|payment|card|100|CZK|true|rurl|POST|"
        "Payment|1|100|||cs|600"
    )
    _sig_util.ensure_text_to_sign_equals_json_body(sign_text, json_body)
