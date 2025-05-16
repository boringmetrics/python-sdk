"""
Utility functions for the Boring Metrics SDK
"""

import time
from datetime import datetime
from functools import wraps
from typing import Any, Callable, TypeVar

from boringmetrics.errors import TransportError

T = TypeVar('T')


def with_retry(max_retries: int) -> Callable:
    """
    Decorator to retry a function with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retries >= max_retries:
                        raise TransportError(f"Failed after {max_retries} retries: {str(e)}")
                    
                    # Exponential backoff
                    delay = 2 ** retries * 0.1
                    time.sleep(delay)
                    retries += 1
        return wrapper
    return decorator


def get_iso_timestamp() -> str:
    """
    Get current time as ISO 8601 string
    
    Returns:
        ISO 8601 formatted timestamp
    """
    return datetime.utcnow().isoformat() + "Z"
