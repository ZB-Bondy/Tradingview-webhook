class WebhookError(Exception):
    """Base exception for all tradingview-webhook errors."""


class UnauthorizedIP(WebhookError):
    """Request came from an IP not in TradingView's known IP allowlist."""


class InvalidToken(WebhookError):
    """The token in the request body does not match the configured secret."""


class MalformedJSON(WebhookError):
    """The request body could not be parsed as JSON despite a JSON content-type."""


class InvalidPayload(WebhookError):
    """The request body is empty or in an unsupported format."""
