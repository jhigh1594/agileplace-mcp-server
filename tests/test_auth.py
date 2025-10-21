"""Tests for authentication module."""

import os
from unittest.mock import patch

import pytest

from agileplace_mcp.src.auth import AgilePlaceAuth, AgilePlaceAuthError


def test_auth_from_env_vars():
    """Test authentication with environment variables."""
    with patch.dict(
        os.environ,
        {
            "AGILEPLACE_DOMAIN": "test.leankit.com",
            "AGILEPLACE_API_TOKEN": "test_token_123",
        },
    ):
        auth = AgilePlaceAuth()
        assert auth.domain == "test.leankit.com"
        assert auth.api_token == "test_token_123"
        assert auth.base_url == "https://test.leankit.com/io"


def test_auth_from_parameters():
    """Test authentication with direct parameters."""
    auth = AgilePlaceAuth(domain="custom.leankit.com", api_token="custom_token")
    assert auth.domain == "custom.leankit.com"
    assert auth.api_token == "custom_token"


def test_auth_strips_protocol():
    """Test that https:// is stripped from domain."""
    auth = AgilePlaceAuth(
        domain="https://test.leankit.com", api_token="test_token"
    )
    assert auth.domain == "test.leankit.com"
    assert "https://" not in auth.domain


def test_auth_missing_domain():
    """Test that missing domain raises error."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(AgilePlaceAuthError, match="AGILEPLACE_DOMAIN"):
            AgilePlaceAuth()


def test_auth_missing_token():
    """Test that missing token raises error."""
    with patch.dict(os.environ, {"AGILEPLACE_DOMAIN": "test.leankit.com"}):
        with pytest.raises(AgilePlaceAuthError, match="AGILEPLACE_API_TOKEN"):
            AgilePlaceAuth()


def test_auth_headers():
    """Test authentication headers are correct."""
    auth = AgilePlaceAuth(domain="test.leankit.com", api_token="test_token")
    headers = auth.get_headers()

    assert headers["Authorization"] == "Bearer test_token"
    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"


def test_auth_validate():
    """Test validation of credentials."""
    auth = AgilePlaceAuth(domain="test.leankit.com", api_token="test_token")
    assert auth.validate() is True

