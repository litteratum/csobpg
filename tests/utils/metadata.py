"""Shared metadata for the signing tests.

The SIGN_TEXT constants are derived from the CSOB specification field
order, not from the implementation:

* customer / order: "Purchase metadata" wiki page
* fingerprint: "Methods for OneClick Payment" wiki page
* actions: "Methods for OneClick Payment" wiki page
"""

from csobpg.v19.models import currency as _currency
from csobpg.v19.models import customer as _customer
from csobpg.v19.models import fingerprint as _fingerprint
from csobpg.v19.models import order as _order

MERCHANT_DATA = b"Hello, World!"
MERCHANT_DATA_SIGN_TEXT = "SGVsbG8sIFdvcmxkIQ=="

# name|email|homePhone|workPhone|mobilePhone
# |account.createdAt|account.changedAt|account.changedPwdAt
# |account.orderHistory|account.paymentsDay|account.paymentsYear
# |account.oneclickAdds|account.suspicious
# |login.auth|login.authAt|login.authData
CUSTOMER_SIGN_TEXT = (
    "John Doe|john@example.com|+420.111111111|+420.222222222|"
    "+420.333333333|2023-01-01T00:00:00Z|2023-01-02T00:00:00Z|"
    "2023-01-03T00:00:00Z|11|12|13|14|true|federated|"
    "2023-01-04T00:00:00Z|ad"
)

# type|availability|delivery|deliveryMode|deliveryEmail|nameMatch
# |addressMatch
# |billing.address1|billing.address2|billing.address3|billing.city
# |billing.zip|billing.state|billing.country
# |shipping.address1|shipping.address2|shipping.address3|shipping.city
# |shipping.zip|shipping.state|shipping.country
# |shippingAddedAt|reorder
# |giftcards.totalAmount|giftcards.currency|giftcards.quantity
# |trxUsage
ORDER_SIGN_TEXT = (
    "cash|preorder|other|3|de@example.com|true|false|"
    "ba1|ba2|ba3|bc|11000|CZ-PR|CZE|"
    "sa1|sa2|sa3|sc|22000|CZ-ST|CZE|"
    "2023-01-05T00:00:00Z|true|15|CZK|16|crypto"
)

# browser.userAgent|browser.acceptHeader|browser.language
# |browser.javascriptEnabled|browser.colorDepth|browser.screenHeight
# |browser.screenWidth|browser.timezone|browser.javaEnabled
# |browser.challengeWindowSize
# |sdk.appID|sdk.encData|sdk.ephemPubKey|sdk.maxTimeout
# |sdk.referenceNumber|sdk.transID
FINGERPRINT_SIGN_TEXT = (
    "ua|ah|cs|true|24|1080|1920|-60|true|05|aid|ed|epk|5|rn|stid"
)

ACTIONS_JSON = {
    "fingerprint": {
        "browserInit": {
            "url": "https://fp.example.com",
            "method": "GET",
            "vars": {"fv1": "fvv1", "fv2": "fvv2"},
        },
        "sdkInit": {
            "directoryServerID": "dsid",
            "schemeId": "schid",
            "messageVersion": "2.2.0",
        },
    },
    "authenticate": {
        "browserChallenge": {
            "url": "https://ch.example.com",
            "method": "POST",
            "vars": {"cv1": "cvv1"},
        },
        "sdkChallenge": {
            "threeDSServerTransID": "tdstid",
            "acsReferenceNumber": "arn",
            "acsTransID": "atid",
            "acsSignedContent": "asc",
        },
    },
}

# fingerprint.browserInit.url|.method|.vars
# |fingerprint.sdkInit.directoryServerID|.schemeId|.messageVersion
# |authenticate.browserChallenge.url|.method|.vars
# |authenticate.sdkChallenge.threeDSServerTransID|.acsReferenceNumber
# |.acsTransID|.acsSignedContent
ACTIONS_SIGN_TEXT = (
    "https://fp.example.com|GET|fvv1|fvv2|dsid|schid|2.2.0|"
    "https://ch.example.com|POST|cvv1|tdstid|arn|atid|asc"
)


def customer_data() -> _customer.CustomerData:
    """Return customer data with every parameter set."""
    return _customer.CustomerData(
        name="John Doe",
        email="john@example.com",
        home_phone=_customer.PhoneNumber(
            prefix="+420",
            subscriber="111111111",
        ),
        work_phone=_customer.PhoneNumber(
            prefix="+420",
            subscriber="222222222",
        ),
        mobile_phone=_customer.PhoneNumber(
            prefix="+420",
            subscriber="333333333",
        ),
        account=_customer.AccountData(
            created_at="2023-01-01T00:00:00Z",
            changed_at="2023-01-02T00:00:00Z",
            changed_pwd_at="2023-01-03T00:00:00Z",
            order_history=11,
            payment_day=12,
            payment_year=13,
            oneclick_adds=14,
            suspicious=True,
        ),
        login=_customer.LoginData(
            auth=_customer.AuthMethod.FEDERATED,
            auth_at="2023-01-04T00:00:00Z",
            auth_data="ad",
        ),
    )


def order_data() -> _order.OrderData:
    """Return order data with every parameter set."""
    return _order.OrderData(
        order_type=_order.OrderType.CASH,
        availability=_order.OrderAvailability.PREORDER,
        delivery=_order.DeliveryData(
            indicator=_order.DeliveryIndicator.OTHER,
            mode=_order.DeliveryMode.LATER,
            email="de@example.com",
        ),
        name_match=True,
        address_match=False,
        billing=_order.AddressData(
            address="ba1",
            country="CZE",
            city="bc",
            zip_code="11000",
            state="CZ-PR",
            address2="ba2",
            address3="ba3",
        ),
        shipping=_order.AddressData(
            address="sa1",
            country="CZE",
            city="sc",
            zip_code="22000",
            state="CZ-ST",
            address2="sa2",
            address3="sa3",
        ),
        shipping_added_at="2023-01-05T00:00:00Z",
        reorder=True,
        gift_cards=_order.GiftCardsData(
            total_amount=15,
            currency=_currency.Currency.CZK,
            quantity=16,
        ),
        trx_usage=_order.TrxUsage.CRYPTO,
    )


def fingerprint() -> _fingerprint.Fingerprint:
    """Return a fingerprint with every parameter set."""
    return _fingerprint.Fingerprint(
        browser=_fingerprint.Browser(
            user_agent="ua",
            accept_header="ah",
            language="cs",
            js_enabled=True,
            color_depth=24,
            screen_height=1080,
            screen_width=1920,
            timezone=-60,
            java_enabled=True,
            challenge_window_size="05",
        ),
        sdk=_fingerprint.SDK(
            max_timeout=5,
            reference_number="rn",
            transaction_id="stid",
            app_id="aid",
            enc_data="ed",
            ephem_pub_key="epk",
        ),
    )


NEW_ACCOUNT_CUSTOMER_SIGN_TEXT = (
    "John Doe|john@example.com|+420.111111111|+420.222222222|"
    "+420.333333333|2023-01-01T00:00:00Z|2023-01-02T00:00:00Z|"
    "2023-01-03T00:00:00Z|0|0|0|0|false|federated|"
    "2023-01-04T00:00:00Z|ad"
)

UTC_BROWSER_FINGERPRINT_SIGN_TEXT = (
    "ua|ah|cs|true|24|1080|1920|0|false|05|aid|ed|epk|5|rn|stid"
)


def new_account_customer_data() -> _customer.CustomerData:
    """Return customer data of a brand new account.

    Zero is a legal value for every account counter: the customer has
    made no orders or payments yet. `suspicious` is legally false.
    """
    customer = customer_data()
    customer.account = _customer.AccountData(
        created_at="2023-01-01T00:00:00Z",
        changed_at="2023-01-02T00:00:00Z",
        changed_pwd_at="2023-01-03T00:00:00Z",
        order_history=0,
        payment_day=0,
        payment_year=0,
        oneclick_adds=0,
        suspicious=False,
    )
    return customer


def utc_browser_fingerprint() -> _fingerprint.Fingerprint:
    """Return a fingerprint of a UTC browser without Java.

    Zero is a legal timezone offset (UTC) and `javaEnabled` is legally
    false.
    """
    result = fingerprint()
    result.browser = _fingerprint.Browser(
        user_agent="ua",
        accept_header="ah",
        language="cs",
        js_enabled=True,
        color_depth=24,
        screen_height=1080,
        screen_width=1920,
        timezone=0,
        java_enabled=False,
        challenge_window_size="05",
    )
    return result
