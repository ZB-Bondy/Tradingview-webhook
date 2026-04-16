"""
Flask integration for tradingview-webhook.

Usage::

    from flask import Flask, request
    from tradingview_webhook import WebhookHandler, WebhookError
    from tradingview_webhook.integrations.flask_handler import from_flask_request

    app = Flask(__name__)
    handler = WebhookHandler(secret_token="my-secret")

    @app.route("/webhook", methods=["POST"])
    def webhook():
        try:
            payload = from_flask_request(request, handler)
            print(payload.raw)
            return "", 200
        except WebhookError as e:
            return str(e), 403
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Request

from ..handler import WebhookHandler
from ..models import WebhookPayload


def from_flask_request(request: "Request", handler: WebhookHandler) -> WebhookPayload:
    """
    Extract body, content-type, and sender IP from a Flask request object
    and pass them to the handler for validation and parsing.

    Args:
        request: The Flask ``request`` proxy object (imported from flask).
        handler: A configured :class:`~tradingview_webhook.WebhookHandler` instance.

    Returns:
        :class:`~tradingview_webhook.WebhookPayload`

    Raises:
        UnauthorizedIP, InvalidToken, MalformedJSON, InvalidPayload
    """
    sender_ip = request.headers.get("X-Forwarded-For", request.remote_addr) or ""
    # X-Forwarded-For may be a comma-separated list; take the first (original) IP.
    sender_ip = sender_ip.split(",")[0].strip()

    return handler.process(
        body=request.get_data(),
        content_type=request.content_type or "",
        sender_ip=sender_ip,
    )
