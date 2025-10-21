"""Authentication handling for AgilePlace API."""

import os
from typing import Optional


class AgilePlaceAuthError(Exception):
    """Exception raised for authentication errors."""

    pass


class AgilePlaceAuth:
    """Handles authentication for AgilePlace API requests."""

    def __init__(
        self,
        domain: Optional[str] = None,
        api_token: Optional[str] = None,
    ):
        """
        Initialize authentication handler.

        Args:
            domain: AgilePlace domain (e.g., 'mycompany.leankit.com').
                   If None, reads from AGILEPLACE_DOMAIN environment variable.
            api_token: API token for authentication.
                      If None, reads from AGILEPLACE_API_TOKEN environment variable.

        Raises:
            AgilePlaceAuthError: If required credentials are missing.
        """
        self.domain = domain or os.getenv("AGILEPLACE_DOMAIN")
        self.api_token = api_token or os.getenv("AGILEPLACE_API_TOKEN")

        if not self.domain:
            raise AgilePlaceAuthError(
                "AGILEPLACE_DOMAIN environment variable is required. "
                "Set it to your AgilePlace domain (e.g., 'mycompany.leankit.com')"
            )

        if not self.api_token:
            raise AgilePlaceAuthError(
                "AGILEPLACE_API_TOKEN environment variable is required. "
                "Create a token at: https://{}/account/api".format(self.domain)
            )

        # Ensure domain doesn't have protocol
        self.domain = self.domain.replace("https://", "").replace("http://", "")

    @property
    def base_url(self) -> str:
        """Get the base URL for API requests."""
        return f"https://{self.domain}/io"

    def get_headers(self) -> dict[str, str]:
        """
        Get authentication headers for API requests.

        Returns:
            Dictionary of headers including Authorization with Bearer token.
        """
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def validate(self) -> bool:
        """
        Validate that credentials are present.

        Returns:
            True if credentials are valid (present).
        """
        return bool(self.domain and self.api_token)

