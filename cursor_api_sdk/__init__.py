"""
Cursor API Python SDK

A comprehensive Python SDK for interacting with the Cursor API.
"""

from .cursor_api import (
    CursorAPI,
    CursorAPIError,
    CursorConfig,
    RateLimiter,
    create_cursor_client,
    rate_limit,
)

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "CursorAPI",
    "CursorAPIError", 
    "CursorConfig",
    "RateLimiter",
    "create_cursor_client",
    "rate_limit",
]