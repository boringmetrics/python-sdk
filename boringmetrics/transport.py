"""
Transport layer for the Boring Metrics SDK
"""

import json
from typing import Dict, List, Any

import requests

from boringmetrics.constants import API_URL
from boringmetrics.errors import TransportError
from boringmetrics.utils import with_retry


class Transport:
    """
    Transport layer for API communication
    """

    def __init__(self, token: str, maxRetryAttempts: int = 5):
        """
        Initialize the transport layer

        Args:
            token: API token for authentication
            maxRetryAttempts: Maximum number of retry attempts for failed requests
        """
        self.token = token
        self.maxRetryAttempts = maxRetryAttempts
        self.apiUrl = API_URL

    @with_retry(5)
    def send_logs(self, logs: List[Dict[str, Any]]) -> None:
        """
        Send logs to the API

        Args:
            logs: List of log objects to send

        Raises:
            TransportError: If the API request fails
        """
        response = requests.post(
            f"{self.apiUrl}/api/v1/logs",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            json={"logs": logs},
        )

        if not response.ok:
            raise TransportError(f"Failed to send logs: {response.status_code} - {response.text}")

    @with_retry(5)
    def update_live(self, liveUpdate: Dict[str, Any]) -> None:
        """
        Update a live metric

        Args:
            liveUpdate: Live update object

        Raises:
            TransportError: If the API request fails
        """
        liveId = liveUpdate.get("liveId")
        if not liveId:
            raise ValueError("liveId is required")

        response = requests.put(
            f"{self.apiUrl}/api/v1/lives/{liveId}",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            json={"live": liveUpdate},
        )

        if not response.ok:
            raise TransportError(f"Failed to update live: {response.status_code} - {response.text}")
