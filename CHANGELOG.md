# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
  * `APIInvalidResponseError` exception. Raised when the API returns something unexpected (e.g. malformed resultCode, missing signature, etc.)

### Fixed
  * `process_gateway_return` now requires a signature. **Warning**: backward-incompatible change
  * The signature is now verified before the `resultCode` is raised for. A signed response reporting a failure raises `APIInvalidSignatureError` if its signature does not match, so such a failure cannot be fabricated by anyone but the API. **Warning**: backward-incompatible change


### Changed
  * Invalid API responses now raised as `APIInvalidResponseError` instead of `HTTPError`. **Warning**: backward-incompatible change
  * Missing/empty signature now raises `APIInvalidResponseError` instead of `APIInvalidSignatureError`. **Warning**: backward-incompatible change
  * Responses the API does not sign (the ones it rejects before processing, e.g. `HTTP 401 {"resultCode": 100}`) are still reported as `APIError`. They are never turned into a result though: an unsigned response with `resultCode` = 0 raises `APIInvalidResponseError`
  * `APIError` is now a subclass of the `APIClientError`. **Warning**: backward-incompatible change
  * Raise `APIInvalidResponseError` (instead of `HTTPError`) for empty responses. **Warning**: backward-incompatible change
  * The library now raises `APIInvalidResponseError` when the `resultCode` is `0` but HTTP status code is not `200`. **Warning**: backward-incompatible change


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
