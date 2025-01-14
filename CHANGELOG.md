# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased


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
