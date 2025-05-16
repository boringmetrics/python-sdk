"""
Lives functionality for the Boring Metrics SDK
"""

from typing import Dict, List, Any, Optional, Union


class LiveMethods:
    """
    Methods for updating live metrics
    """

    def __init__(self, client):
        """
        Initialize the lives API

        Args:
            client: The client instance
        """
        self.client = client

    def update(self,
               liveId: str,
               value: Union[int, float],
               operation: str = "set",
               sentAt: Optional[str] = None) -> None:
        """
        Update a live metric value

        Args:
            liveId: The ID of the live metric
            value: The value to set or increment
            operation: The operation to perform ("set" or "increment")
            sentAt: ISO8601 date - will be automatically set if not provided
        """
        update = {
            "liveId": liveId,
            "value": value,
            "operation": operation,
        }

        if sentAt:
            update["sentAt"] = sentAt

        self.client.update_live(update)

    def update_dict(self, update: Dict[str, Any]) -> None:
        """
        Update a live metric from a dictionary

        Args:
            update: The live update to send
        """
        self.client.update_live(update)

    def update_batch(self, updates: List[Dict[str, Any]]) -> None:
        """
        Update multiple live metrics in a batch

        Args:
            updates: Array of live updates to send
        """
        for update in updates:
            self.client.update_live(update)
