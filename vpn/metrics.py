from prometheus_client import Counter

# Total allowed /status requests
STATUS_ALLOWED = Counter(
    "vpn_status_allowed_total",
    "Number of /status requests allowed by VPN",
    ["user"]
)

# JWT failures
JWT_INVALID = Counter(
    "vpn_jwt_invalid_total",
    "Number of invalid or expired JWT tokens"
)

# Upstream (app) failures
UPSTREAM_ERRORS = Counter(
    "vpn_upstream_errors_total",
    "Number of upstream app failures during /status proxy"
)
