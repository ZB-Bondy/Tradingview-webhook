import json
import logging

from .constants import TRADINGVIEW_IPS
from .exceptions import InvalidPayload, InvalidToken, MalformedJSON, UnauthorizedIP
from .models import WebhookPayload

logger = logging.getLogger(__name__)


class WebhookHandler:
    """
    Core handler for TradingView webhook requests.

    Instantiate once (e.g. at app startup) and call .process() inside your route.

    Args:
        secret_token: Expected value of the ``token`` field in the JSON body.
                      Pass ``None`` to skip token validation entirely.
        verify_ip:    Check that the sender IP is in TradingView's known IP list.
                      Set to ``False`` in dev_mode / ngrok testing.
        dev_mode:     Convenience shortcut — sets ``verify_ip=False`` and logs a warning.

    Example::

        handler = WebhookHandler(secret_token="my-secret")
        payload = handler.process(body=b'...', content_type="application/json", sender_ip="52.89.214.238")
    """

    def __init__(
        self,
        secret_token: str | None = None,
        verify_ip: bool = True,
        dev_mode: bool = False,
    ) -> None:
        self.secret_token = secret_token
        self.verify_ip = verify_ip and not dev_mode

        if dev_mode:
            logger.warning(
                "tradingview-webhook: dev_mode=True — IP verification is disabled. "
                "Do not use this in production."
            )

    def process(
        self,
        body: bytes,
        content_type: str,
        sender_ip: str,
    ) -> WebhookPayload:
        """
        Validate and parse an incoming TradingView webhook request.

        Args:
            body:         Raw request body bytes.
            content_type: Value of the Content-Type header (e.g. "application/json").
            sender_ip:    IP address of the request sender.

        Returns:
            WebhookPayload with the parsed body and metadata.

        Raises:
            UnauthorizedIP:  sender_ip is not in TradingView's allowlist.
            InvalidToken:    token field missing or does not match secret_token.
            MalformedJSON:   Content-Type is JSON but body could not be parsed.
            InvalidPayload:  Body is empty or content-type is unrecognised.
        """
        logger.debug("Processing webhook from %s", sender_ip)

        if self.verify_ip:
            self._check_ip(sender_ip)

        raw = self._parse_body(body, content_type)

        if self.secret_token is not None:
            self._check_token(raw)

        logger.info("Webhook accepted from %s", sender_ip)
        return WebhookPayload(raw=raw, sender_ip=sender_ip)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _check_ip(self, sender_ip: str) -> None:
        if sender_ip not in TRADINGVIEW_IPS:
            logger.warning("Rejected request from unauthorized IP: %s", sender_ip)
            raise UnauthorizedIP(
                f"IP {sender_ip!r} is not in TradingView's known IP allowlist."
            )

    def _parse_body(self, body: bytes, content_type: str) -> dict | str:
        if not body:
            raise InvalidPayload("Request body is empty.")

        ct = content_type.lower().split(";")[0].strip()

        if ct == "application/json":
            try:
                return json.loads(body)
            except json.JSONDecodeError as exc:
                raise MalformedJSON(f"Failed to parse JSON body: {exc}") from exc

        if ct == "text/plain":
            return body.decode("utf-8", errors="replace")

        # TradingView only sends these two content types, but be lenient:
        # try JSON first, fall back to plain text.
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return body.decode("utf-8", errors="replace")

    def _check_token(self, raw: dict | str) -> None:
        if not isinstance(raw, dict):
            raise InvalidToken(
                "Token validation requires a JSON body, but received plain text."
            )
        token = raw.get("token")
        if token != self.secret_token:
            logger.warning("Rejected request with invalid token.")
            raise InvalidToken("Token in request body does not match the configured secret.")
