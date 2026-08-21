"""Tests for the actions models."""

from csobpg.v19.models import actions as _a


class TestActions:
    """Tests for the `Actions`."""

    def test_from_empty_json(self):
        """Test init from an empty JSON."""
        _a.Actions.from_json({})

    def test_to_sign_text(self):
        """Test to_sign_text()."""
        assert _a.Actions.from_json(
            {
                "fingerprint": {
                    "browserInit": {
                        "url": "https://example.com",
                        "method": "POST",
                        "vars": {"key": "value"},
                    },
                    "sdkInit": {
                        "directoryServerID": "directory_server_id",
                        "schemeId": "scheme_id",
                        "messageVersion": "message_version",
                    },
                },
                "authenticate": {
                    "browserChallenge": {
                        "url": "https://example2.com",
                        "method": "POST",
                        "vars": {"key2": "value2"},
                    },
                    "sdkChallenge": {
                        "threeDSServerTransID": "three_ds_server_trans_id",
                        "acsReferenceNumber": "acs_reference_number",
                        "acsTransID": "acs_trans_id",
                        "acsSignedContent": "acs_signed_content",
                    },
                },
            },
        ).to_sign_text() == (
            "https://example.com|POST|value"
            "|directory_server_id|scheme_id|message_version"
            "|https://example2.com|POST|value2"
            "|three_ds_server_trans_id|acs_reference_number"
            "|acs_trans_id|acs_signed_content"
        )
