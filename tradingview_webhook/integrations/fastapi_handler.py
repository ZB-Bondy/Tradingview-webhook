"""
FastAPI integration for tradingview-webhook.

Usage::

    from fastapi import FastAPI, Request
    from tradingview_webhook import WebhookHandler, WebhookError
    from tradingview_webhook.integrations.fastapi_handler import from_fastapi_request

    app = FastAPI()
    handler = WebhookHandler(secret_token="my-secret")

    @app.post("/webhook")
    async def webhook(request: Request):
        try:
            payload = await from_fastapi_request(request, handler)
            print(payload.raw)
            return {"status": "ok"}
        except WebhookError as e:
            from fastapi import HTTPException
            raise HTTPException(status_code=403, detail=str(e))
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import Request

from ..handler import WebhookHandler
from ..models import WebhookPayload


async def from_fastapi_request(request: "Request", handler: WebhookHandler) -> WebhookPayload:
    """
    Extract body, content-type, and sender IP from a FastAPI Request object
    and pass them to the handler for validation and parsing.

    This is an async function — await it inside your async route.

    Args:
        request: The FastAPI ``Request`` object.
        handler: A configured :class:`~tradingview_webhook.WebhookHandler` instance.

    Returns:
        :class:`~tradingview_webhook.WebhookPayload`

    Raises:
        UnauthorizedIP, InvalidToken, MalformedJSON, InvalidPayload
    """
    forwarded_for = request.headers.get("x-forwarded-for", "")
    sender_ip = forwarded_for.split(",")[0].strip() if forwarded_for else (request.client.host if request.client else "")

    body = await request.body()
    content_type = request.headers.get("content-type", "")

    return handler.process(
        body=body,
        content_type=content_type,
        sender_ip=sender_ip,
    )
