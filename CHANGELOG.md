# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
  * `APIInvalidResponseError` exception. Raised when the API returns something unexpected (e.g. malformed resultCode, missing signature, etc.)
  * `EchoResponse`. `APIClient.echo` now returns it instead of `None`. The echo response signature is verified as for any other operation. **Warning**: backward-incompatible change
  * Test suite for request bodies, response parsing and signing: `tests/utils` (signature/JSON multiset comparison, spec-derived sign-text metadata, key and response helpers) plus tests for the customer, order, cart, fingerprint models, the payment/oneclick/echo/wallet requests and the payment/echo/wallet responses

### Fixed
  * `APIClient.echo` neither verified the response signature nor raised for the `resultCode`. Now it does both. **Warning**: backward-incompatible change
  * `process_gateway_return` now requires a signature. **Warning**: backward-incompatible change
  * The signature is now verified before the `resultCode` is raised for. A signed response reporting a failure raises `APIInvalidSignatureError` if its signature does not match, so such a failure cannot be fabricated by anyone but the API. **Warning**: backward-incompatible change
  * Wrong JSON keys in the request body. `AccountData.payment_day` and `AccountData.payment_year` were sent as `paymentDay`/`paymentYear` and `OrderData.gift_cards` as `giftCards`, while the API expects `paymentsDay`, `paymentsYear` and `giftcards`. The gateway ignored the unknown keys and rebuilt the signature without them, so any payment setting those fields was rejected with an invalid signature
  * Signing desync between `as_json` and `to_sign_text`. Falsy-but-meaningful values (`False`, `0`, `""`) were dropped from the request body but still included in the signature text, so the gateway rebuilt a different string and rejected the request with an invalid signature. Affected `CartItem.description`, `AccountData` (`orderHistory`, `paymentsDay`, `paymentsYear`, `oneclickAdds`, `suspicious`), `LoginData`, `CustomerData`, `Browser` (`colorDepth`, `screenHeight`, `screenWidth`, `timezone`, `javaEnabled`), `OrderData` (`nameMatch`, `addressMatch`, `reorder`, delivery fields) and `GiftCardsData.currency`
  * Nested objects leaked `null` values into the request body (e.g. `fingerprint.sdk` always sent `appId`, `encData`, `ephemPubKey` as `null`). `None` values are now stripped recursively, and objects/lists left empty by that stripping are omitted entirely
  * `DeliveryMode` values are now strings (`"0"`–`"3"`) instead of integers, matching what the API expects in both the body and the signature. **Warning**: backward-incompatible change if you read `DeliveryMode.*.value`
  * `OrderData` and `AccountData` JSON keys (paymentDay -> paymentsDay, giftCards -> giftcards, etc.)


### Changed
  * Invalid API responses now raised as `APIInvalidResponseError` instead of `HTTPError`. **Warning**: backward-incompatible change
  * Missing/empty signature now raises `APIInvalidResponseError` instead of `APIInvalidSignatureError`. **Warning**: backward-incompatible change
  * Responses the API does not sign (the ones it rejects before processing, e.g. `HTTP 401 {"resultCode": 100}`) are still reported as `APIError`. They are never turned into a result though: an unsigned response with `resultCode` = 0 raises `APIInvalidResponseError`
  * `APIError` is now a subclass of the `APIClientError`. **Warning**: backward-incompatible change
  * Raise `APIInvalidResponseError` (instead of `HTTPError`) for empty responses. **Warning**: backward-incompatible change
  * The library now raises `APIInvalidResponseError` when the `resultCode` is `0` but HTTP status code is not `200`. **Warning**: backward-incompatible change
  * Models now return their full JSON body from `as_json()`, including `None` values; filtering happens once in `BaseRequest.as_json()`. `_as_json()` implementations must no longer filter `None` or empty objects themselves. **Warning**: relevant only if you subclass `BaseRequest`
  * `SignedModel.to_sign_text` now flattens lists and dicts returned by `_get_params_sequence` (dict values are signed in insertion order) and skips nested signed models that contribute no values, so models return their params as-is. `Endpoint.vars` and the Apple Pay / Google Pay echo network and capability lists rely on this instead of pre-joining with `|`
  * `Browser.timezone` is now typed `int | None` instead of `float | None`, matching the other numeric browser fields. The API expects the UTC offset in whole minutes (what JS `getTimezoneOffset()` returns); a float would be sent and signed as `-60.0` while the gateway rebuilds `-60` from its parsed value, so the request would be rejected with an invalid signature


## [0.5.2] - 2025-02-02
### Added
  * Support for Apple Pay methods. **Warning**: experimental

## [0.5.1] - 2025-01-14
### Fixed
  * OneClick documentation. It was also extended
  * Remove TODOs for ISO validators. For now it is decided to not validate ISO values

### Added
  * `APIClient.oneclick_init` now raises `ValueError` in case of parameters misuse
  * Support for Google Pay methods. **Warning**: experimental


## [0.5.0] - 2025-01-08
### Removed
  * `Response.raise_for_result_code` method. The APIClient now raises `APIError` if `resultCode` != 0. Clients have no access to the `raise_for_result_code` method anymore. **Warning**: backward-incompatible change

### Fixed
  * order.address has "address1" field (not "address")
  * Some models were not correctly converted into text to sign


## [0.4.0] - 2024-10-17
### Added
  * Upgrade to use `httprest` v.0.3.0


## [0.3.0] - 2024-09-25
### Added
  * Use `httprest` library for HTTP requests
  * Unit tests for the `api.py`

### Fixed
  * `APIClient.oneclick_process` method (JSON body was missing in the request)

### Changed
  * Drop support for Python 3.7
  * Add support for Python 3.12


## [0.2.0] - 2024-08-12
### Added
  * Support for OneClick payments

### Changed
  * All models (e.g. Cart, CartItem, CustomerData, etc.) are moved to the new `csobpg.v19.models` package
  * Import paths. **Warning**: backward-incompatible change

## [0.1.1] - 2024-07-19
### Added
  * Logging


## [0.1.0] - 2024-07-18
### Changed
  * Don't raise exception for resultCode != 0. Provide the `raise_for_result_code` method


## [0.0.1] - 2024-07-16
  * Initial release
