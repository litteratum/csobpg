[![Codecov](https://codecov.io/gh/litteratum/csobpg/branch/master/graph/badge.svg)](https://codecov.io/gh/litteratum/csobpg)
# CSOB client
Python library for communicating with ČSOB (<https://platbakartou.csob.cz/>) payment gateway API. The API is described here: <https://github.com/csob/paymentgateway>.

The library currently implements ČSOB API v.1.9.


## Installation
```bash
pip install csobpg
```

## Basic usage
### API client initialization
The `APIClient` provides the interface to communicate with the API.

```python
from csobpg.v19 import APIClient

client = APIClient("merchantId", "merch_private.key", "csob.pub", base_url=..., http_client=...)

# Use the client to interact with the API:
client.init_payment(...)
```

### HTTP client
The library uses the [httprest](https://github.com/litteratum/httprest) library for making HTTP requests.
By default it will use `httprest.http.urllib_client.UrllibHTTPClient`.

But you may use any other `httprest's` HTTP client, or even write your own client.

## Base methods
The library supports all base API methods.
For example, that's how to initialize a payment:
```python
from csobpg.v19.models import cart

response = client.init_payment(
    order_no="2233823251",
    total_amount=100,
    return_url="http://127.0.0.1:5000",
    cart=cart.Cart([cart.CartItem("Apples", 1, 100)]),
    merchant_data=b"Hello, World!",
)
```

## OneClick methods
Here are the steps to perform a OneClick payment.

### Step 1 - make a regular payment
First, make a regular payment using the "payment/init":
```python
response = client.init_payment(
    ...,
    # this is important. It will tell the bank to create a OneClick template
    payment_operation=PaymentOperation.ONE_CLICK_PAYMENT,
)
# redirect to the payment page and finalize payment
client.get_payment_process_url(pid)
```

Preserve the `response.pay_id`, it will be used to refer to the OneClick template.

### Step 2 - initialize OneClick payment
Now, having the template ID, initialize the OneClick payment.
First, check that the template ID exists (optional, but recommended):
```python
response = client.oneclick_echo(template_id)
if not response.success:
    # OneClick template not found! handle it somehow
```

If the template exists, initiate the payment:
```python
response = client.oneclick_init_payment(
    pid, # this is the template ID (the ID of the initial payment, retrieved in Step 1)
    ...,
    client_ip="127.0.0.1", # this is mandatory when client_initiated=True
    client_initiated=True, # whether it is initiated in the presence of client or not
)
```

### Step 3 - process OneClick payment
Finally, process the payment:
```python
response = client.oneclick_process(
    pid, # this is the payment ID retrieved in Step 2
    Fingerprint( # mandatory only for client_initiated=True
        Browser( # the following values must be taken from the client's browser
            user_agent="requests",
            accept_header="application/json",
            language="eng",
            js_enabled=False,
        ),
    ),
)
```

## Google Pay methods
```python
# echo
response = client.googlepay_echo()

# payment Initialization
client.googlepay_init(
    pid, "127.0.0.1", 10000, {"Google Pay": "payload"}, "http://localhost"
)

# payment process
client.googlepay_process(pid, Fingerprint())
```

## Exceptions handling
```python
from csobpg.v19.errors import APIError, APIClientError
from httprest.http import HTTPRequestError

try:
    response = client.<operation>(...)
except APIError as exc:
    # handle API error
    # it is raised on any API error. You may also catch the specific API error
except APIClientError as exc:
    # handle API client error
    # it is raised when API returns unexpected response (e.g. invalid JSON, invalid signature)
except HTTPRequestError as exc:
    # handle HTTP error
    # it is raised on any HTTP error
except ValueError as exc:
    # handle value error
    # it is raised on any library's misuse (e.g. passing invalid parameters)
    # it always means developer's mistake
```

## RSA keys management
The simples way to pass RSA keys is to pass their file paths:

```python
from csobpg.v19 import APIClient

client = APIClient(..., "merch_private.key", "csob.pub")
```

The library will read the private key from the file when needed. The public key will be cached into the RAM.

If you want to change it, use special classes:

```python
from csobpg.v19 import APIClient
from csobpg.v19.key import FileRSAKey, CachedRSAKey

client = APIClient(..., FileRSAKey("merch_private.key"), FileRSAKey("csob.pub"))
```

You may also override the base RSAKey class to define your own key access strategy:

```python
from csobpg.v19.key import RSAKey

class MyRSAKey(RSAKey):

    def __str__(self) -> str:
        return "my key"
```
