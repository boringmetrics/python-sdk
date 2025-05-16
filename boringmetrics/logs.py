"""
Logs functionality for the Boring Metrics SDK
"""

from typing import Dict, List, Any, Optional, Union


class LogMethods:
    """
    Methods for sending logs
    """

    def __init__(self, client):
        """
        Initialize the logs API

        Args:
            client: The client instance
        """
        self.client = client

    def send(self,
             type: str = "log",
             level: str = "info",
             message: str = "",
             data: Optional[Dict[str, Any]] = None,
             sessionId: Optional[str] = None,
             sentAt: Optional[str] = None) -> None:
        """
        Send a single log event

        Args:
            type: The type of log (default: "log")
            level: The log level (trace, debug, info, warn, error, fatal)
            message: The log message
            data: Additional structured data (optional)
            sessionId: Session identifier for grouping related logs (optional)
            sentAt: ISO8601 date - will be automatically set if not provided
        """
        log = {
            "type": type,
            "level": level,
            "message": message,
        }

        if data:
            log["data"] = data

        if sessionId:
            log["sessionId"] = sessionId

        if sentAt:
            log["sentAt"] = sentAt

        self.client.add_log(log)

    def send_dict(self, log: Dict[str, Any]) -> None:
        """
        Send a single log event from a dictionary

        Args:
            log: The log event to send
        """
        self.client.add_log(log)

    def send_batch(self, logs: List[Dict[str, Any]]) -> None:
        """
        Send multiple log events in a batch

        Args:
            logs: Array of log events to send
        """
        for log in logs:
            self.client.add_log(log)
