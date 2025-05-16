"""
Main client for the Boring Metrics SDK
"""

import threading
import time
from typing import Dict, List, Any, Optional, ClassVar

from boringmetrics.constants import DEFAULT_CONFIG
from boringmetrics.errors import InitializationError
from boringmetrics.lives import LiveMethods
from boringmetrics.logs import LogMethods
from boringmetrics.transport import Transport
from boringmetrics.utils import get_iso_timestamp


class BoringMetrics:
    """
    Main client for the Boring Metrics SDK
    """
    _instance: ClassVar[Optional['BoringMetrics']] = None

    @classmethod
    def initialize(cls, token: str, **config) -> 'BoringMetrics':
        """
        Initialize the SDK with your API token

        Args:
            token: Your Boring Metrics API token
            **config: Optional configuration options

        Returns:
            The configured client instance
        """
        if cls._instance is None:
            cls._instance = cls(token, **config)
        return cls._instance

    @classmethod
    def get_instance(cls) -> 'BoringMetrics':
        """
        Get the configured client instance

        Returns:
            The configured client instance

        Raises:
            InitializationError: If the SDK is not initialized
        """
        if cls._instance is None:
            raise InitializationError("BoringMetrics SDK is not initialized. Call initialize() first.")
        return cls._instance

    def __init__(self, token: str, **config):
        """
        Initialize a new client

        Args:
            token: Your Boring Metrics API token
            **config: Optional configuration options
        """
        self.config = {**DEFAULT_CONFIG, **config}
        self.config['token'] = token

        self.transport = Transport(token, self.config['maxRetryAttempts'])

        # Initialize queues and locks
        self.logs_queue: List[Dict[str, Any]] = []
        self.logs_lock = threading.Lock()
        self.logs_timer = None

        self.lives_queue: List[Dict[str, Any]] = []
        self.lives_lock = threading.Lock()
        self.lives_timer = None

        # Initialize API methods
        self._logs = LogMethods(self)
        self._lives = LiveMethods(self)

    @property
    def logs(self) -> LogMethods:
        """
        Access logs functionality

        Returns:
            LogMethods instance
        """
        return self._logs

    @property
    def lives(self) -> LiveMethods:
        """
        Access lives functionality

        Returns:
            LiveMethods instance
        """
        return self._lives

    def add_log(self, log: Dict[str, Any]) -> None:
        """
        Add a log to the queue

        Args:
            log: The log to add
        """
        logWithSentAt = log.copy()

        # Add sentAt if not provided
        if 'sentAt' not in logWithSentAt:
            logWithSentAt['sentAt'] = get_iso_timestamp()

        with self.logs_lock:
            self.logs_queue.append(logWithSentAt)

            if len(self.logs_queue) >= self.config['logsMaxBatchSize']:
                self.flush_logs()
            elif self.logs_timer is None:
                self.schedule_logs_flush()

    def update_live(self, update: Dict[str, Any]) -> None:
        """
        Update a live metric

        Args:
            update: The live update
        """
        updateWithSentAt = update.copy()

        # Add sentAt if not provided
        if 'sentAt' not in updateWithSentAt:
            updateWithSentAt['sentAt'] = get_iso_timestamp()

        with self.lives_lock:
            self.lives_queue.append(updateWithSentAt)

            if len(self.lives_queue) >= self.config['livesMaxBatchSize']:
                self.flush_lives()
            elif self.lives_timer is None:
                self.schedule_lives_flush()

    def schedule_logs_flush(self) -> None:
        """Schedule a logs flush after the configured interval"""
        self.logs_timer = threading.Timer(self.config['logsSendInterval'], self.flush_logs)
        self.logs_timer.daemon = True
        self.logs_timer.start()

    def flush_logs(self) -> None:
        """Flush the logs queue to the API"""
        with self.logs_lock:
            if self.logs_timer:
                self.logs_timer.cancel()
                self.logs_timer = None

            if not self.logs_queue:
                return

            logs_to_send = self.logs_queue.copy()
            self.logs_queue.clear()

        # Send logs in a separate thread
        threading.Thread(target=self._send_logs, args=(logs_to_send,), daemon=True).start()

    def _send_logs(self, logs: List[Dict[str, Any]]) -> None:
        """
        Send logs to the API

        Args:
            logs: List of logs to send
        """
        try:
            self.transport.send_logs(logs)
        except Exception as e:
            print(f"[BoringMetrics] Error sending logs: {str(e)}")

    def schedule_lives_flush(self) -> None:
        """Schedule a lives flush after the configured interval"""
        self.lives_timer = threading.Timer(self.config['livesDebounceTime'], self.flush_lives)
        self.lives_timer.daemon = True
        self.lives_timer.start()

    def flush_lives(self) -> None:
        """Flush the lives queue to the API"""
        with self.lives_lock:
            if self.lives_timer:
                self.lives_timer.cancel()
                self.lives_timer = None

            if not self.lives_queue:
                return

            lives_to_send = self.lives_queue.copy()
            self.lives_queue.clear()

        # Send lives in a separate thread
        threading.Thread(target=self._send_lives, args=(lives_to_send,), daemon=True).start()

    def _send_lives(self, lives: List[Dict[str, Any]]) -> None:
        """
        Send lives to the API

        Args:
            lives: List of live updates to send
        """
        try:
            for live in lives:
                self.transport.update_live(live)
        except Exception as e:
            print(f"[BoringMetrics] Error sending live updates: {str(e)}")
