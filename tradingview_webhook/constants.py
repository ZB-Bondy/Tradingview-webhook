# TradingView's known webhook source IPs.
# https://www.tradingview.com/support/solutions/43000529348/
TRADINGVIEW_IPS: frozenset[str] = frozenset({
    "52.89.214.238",
    "34.212.75.30",
    "54.218.53.128",
    "52.32.178.7",
})

# SSL certificate CN sent by TradingView's webhook server.
# Can be used for mutual TLS verification if needed.
TV_CERT_CN = "webhook-server@tradingview.com"

# TradingView retries on 5xx (except 504), up to 3 retries = 4 total deliveries.
TV_MAX_DELIVERIES = 4
