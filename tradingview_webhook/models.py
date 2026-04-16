from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class WebhookPayload:
    """
    Parsed and validated payload from a TradingView webhook alert.

    Attributes:
        raw:         Parsed JSON body as a dict, or plain text as a str.
        sender_ip:   IP address of the request sender.
        received_at: UTC timestamp when the payload was processed.
    """
    raw: dict | str
    sender_ip: str
    received_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
