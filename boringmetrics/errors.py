"""
Custom exceptions for the Boring Metrics SDK
"""


class BoringMetricsError(Exception):
    """Base exception for all Boring Metrics SDK errors"""
    pass


class TransportError(BoringMetricsError):
    """Error during API communication"""
    pass


class ConfigurationError(BoringMetricsError):
    """Error in SDK configuration"""
    pass


class InitializationError(BoringMetricsError):
    """Error during SDK initialization"""
    pass
