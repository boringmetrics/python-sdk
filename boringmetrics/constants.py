"""
Constants for the Boring Metrics SDK
"""

API_URL = "https://api.getboringmetrics.com"

DEFAULT_CONFIG = {
    "maxRetryAttempts": 5,
    "logsMaxBatchSize": 100,
    "logsSendInterval": 5,  # seconds
    "livesMaxBatchSize": 20,
    "livesDebounceTime": 1,  # seconds
}
