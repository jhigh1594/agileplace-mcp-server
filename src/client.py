"""HTTP client for AgilePlace API with rate limiting and error handling."""

import asyncio
import logging
from datetime import datetime
from typing import Any, Optional

import httpx

from .auth import AgilePlaceAuth

logger = logging.getLogger(__name__)


class AgilePlaceAPIError(Exception):
    """Base exception for AgilePlace API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[dict] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class RateLimitError(AgilePlaceAPIError):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, retry_after: Optional[datetime] = None, **kwargs):
        self.retry_after = retry_after
        super().__init__(**kwargs)


class AgilePlaceClient:
    """
    HTTP client for AgilePlace API with automatic rate limiting and retry logic.
    """

    def __init__(
        self,
        auth: AgilePlaceAuth,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """
        Initialize the API client.

        Args:
            auth: Authentication handler.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for rate-limited requests.
        """
        self.auth = auth
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            base_url=self.auth.base_url,
            headers=self.auth.get_headers(),
            timeout=self.timeout,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.auth.base_url,
                headers=self.auth.get_headers(),
                timeout=self.timeout,
            )
        return self._client

    async def _handle_response(self, response: httpx.Response) -> dict | list:
        """
        Handle API response and raise appropriate exceptions.

        Args:
            response: HTTP response object.

        Returns:
            Parsed JSON response.

        Raises:
            RateLimitError: If rate limit is exceeded.
            AgilePlaceAPIError: For other API errors.
        """
        # Log rate limit headers for monitoring
        if "x-ratelimit-remaining" in response.headers:
            remaining = response.headers.get("x-ratelimit-remaining")
            limit = response.headers.get("x-ratelimit-limit")
            logger.debug(f"Rate limit: {remaining}/{limit} remaining")

        # Handle success
        if response.status_code in (200, 201, 202):
            if response.text:
                return response.json()
            return {}

        # Handle no content
        if response.status_code == 204:
            return {}

        # Handle rate limiting
        if response.status_code == 429:
            retry_after_header = response.headers.get("retry-after")
            retry_after = None
            if retry_after_header:
                try:
                    # Parse date format
                    retry_after = datetime.strptime(
                        retry_after_header, "%a, %d %b %Y %H:%M:%S %Z"
                    )
                except ValueError:
                    pass

            raise RateLimitError(
                message="Rate limit exceeded",
                status_code=429,
                retry_after=retry_after,
            )

        # Handle other errors
        error_message = f"API request failed with status {response.status_code}"
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                error_message = error_data.get("message", error_message)
        except Exception:
            error_message = response.text or error_message

        raise AgilePlaceAPIError(
            message=error_message,
            status_code=response.status_code,
            response=error_data if 'error_data' in locals() else None,
        )

    async def _request_with_retry(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> dict | list:
        """
        Make HTTP request with automatic retry on rate limit.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for httpx request

        Returns:
            Parsed JSON response

        Raises:
            AgilePlaceAPIError: If request fails after retries
        """
        client = self._get_client()
        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = await client.request(method, endpoint, **kwargs)
                return await self._handle_response(response)

            except RateLimitError as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    # Calculate wait time
                    if e.retry_after:
                        wait_time = (e.retry_after - datetime.utcnow()).total_seconds()
                        wait_time = max(0, min(wait_time, 60))  # Cap at 60 seconds
                    else:
                        # Exponential backoff: 2, 4, 8 seconds
                        wait_time = 2 ** (attempt + 1)

                    logger.warning(
                        f"Rate limit hit, retrying in {wait_time:.1f}s (attempt {attempt + 1}/{self.max_retries})"
                    )
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    logger.error("Rate limit exceeded after all retries")
                    raise

        if last_error:
            raise last_error

    async def get(self, endpoint: str, params: Optional[dict] = None) -> dict | list:
        """
        Make GET request.

        Args:
            endpoint: API endpoint path (e.g., '/board/123')
            params: Query parameters

        Returns:
            Parsed JSON response
        """
        return await self._request_with_retry("GET", endpoint, params=params)

    async def post(
        self,
        endpoint: str,
        json: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> dict | list:
        """
        Make POST request.

        Args:
            endpoint: API endpoint path
            json: JSON body
            data: Form data

        Returns:
            Parsed JSON response
        """
        return await self._request_with_retry("POST", endpoint, json=json, data=data)

    async def patch(self, endpoint: str, json: dict) -> dict | list:
        """
        Make PATCH request.

        Args:
            endpoint: API endpoint path
            json: JSON body

        Returns:
            Parsed JSON response
        """
        return await self._request_with_retry("PATCH", endpoint, json=json)

    async def put(self, endpoint: str, json: dict) -> dict | list:
        """
        Make PUT request.

        Args:
            endpoint: API endpoint path
            json: JSON body

        Returns:
            Parsed JSON response
        """
        return await self._request_with_retry("PUT", endpoint, json=json)

    async def delete(self, endpoint: str) -> dict | list:
        """
        Make DELETE request.

        Args:
            endpoint: API endpoint path

        Returns:
            Parsed JSON response
        """
        return await self._request_with_retry("DELETE", endpoint)

    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

