"""
tradingview-webhook
~~~~~~~~~~~~~~~~~~~
Framework-agnostic package for receiving and validating TradingView webhook alerts.

Quick start::

    from tradingview_webhook import WebhookHandler, WebhookPayload, WebhookError

    handler = WebhookHandler(secret_token="my-secret")
"""
from .exceptions import (
    InvalidPayload,
    InvalidToken,
    MalformedJSON,
    UnauthorizedIP,
    WebhookError,
)
from .handler import WebhookHandler
from .models import WebhookPayload

__all__ = [
    "WebhookHandler",
    "WebhookPayload",
    "WebhookError",
    "UnauthorizedIP",
    "InvalidToken",
    "MalformedJSON",
    "InvalidPayload",
]

__version__ = "0.1.0"
