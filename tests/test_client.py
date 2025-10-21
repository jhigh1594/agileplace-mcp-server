"""Tests for API client module."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from agileplace_mcp.src.auth import AgilePlaceAuth
from agileplace_mcp.src.client import (
    AgilePlaceAPIError,
    AgilePlaceClient,
    RateLimitError,
)


@pytest.fixture
def auth():
    """Create test auth object."""
    return AgilePlaceAuth(domain="test.agileplace.com", api_token="test_token")


@pytest.fixture
def client(auth):
    """Create test client."""
    return AgilePlaceClient(auth)


@pytest.mark.asyncio
async def test_successful_get_request(client):
    """Test successful GET request."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    mock_response.text = '{"data": "test"}'
    mock_response.headers = {}

    with patch.object(client, "_get_client") as mock_get_client:
        mock_http_client = AsyncMock()
        mock_http_client.request = AsyncMock(return_value=mock_response)
        mock_get_client.return_value = mock_http_client

        result = await client.get("/test")
        assert result == {"data": "test"}


@pytest.mark.asyncio
async def test_rate_limit_error(client):
    """Test rate limit error handling."""
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_response.headers = {"retry-after": "Fri, 01 Jan 2024 12:00:00 GMT"}

    with patch.object(client, "_get_client") as mock_get_client:
        mock_http_client = AsyncMock()
        mock_http_client.request = AsyncMock(return_value=mock_response)
        mock_get_client.return_value = mock_http_client

        with pytest.raises(RateLimitError):
            await client._handle_response(mock_response)


@pytest.mark.asyncio
async def test_api_error_handling(client):
    """Test API error handling."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not found"
    mock_response.json.side_effect = Exception()
    mock_response.headers = {}

    with pytest.raises(AgilePlaceAPIError) as exc_info:
        await client._handle_response(mock_response)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_no_content_response(client):
    """Test 204 No Content response."""
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_response.headers = {}

    result = await client._handle_response(mock_response)
    assert result == {}

