from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx
import json
import logging
import sys
import os
from datetime import datetime, timedelta
import jwt
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# -------------------------
# Structured JSON logger
# -------------------------
logger = logging.getLogger("vpn")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "msg": %(message)s}'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# -------------------------
# JWT utils
# -------------------------
JWT_SECRET = os.environ.get("JWT_SECRET", "devsecret")
JWT_ALGO = "HS256"
JWT_EXP_MINUTES = 10

def create_jwt(username: str):
    exp = datetime.utcnow() + timedelta(minutes=JWT_EXP_MINUTES)
    payload = {"username": username, "exp": exp}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload["username"]
    except Exception:
        return None

# -------------------------
# Prometheus metrics
# -------------------------
STATUS_ALLOWED = Counter(
    "vpn_status_allowed_total",
    "Number of /status requests allowed by VPN",
    ["user"]
)
JWT_INVALID = Counter(
    "vpn_jwt_invalid_total",
    "Number of invalid or expired JWT tokens"
)

# -------------------------
# Load credentials
# -------------------------
with open("creds.json") as f:
    CREDS = json.load(f)["creds"]

UPSTREAM = "http://app:9002"

# -------------------------
# FastAPI app
# -------------------------
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    logger.info(json.dumps({"event": "index_hit"}))
    with open("static/index.html") as f:
        return f.read()

# LOGIN
@app.post("/login")
async def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        logger.warning(json.dumps({"event": "login_fail", "reason": "missing_fields"}))
        raise HTTPException(400, "Missing username or password")

    for cred in CREDS:
        if cred["username"] == username and cred["password"] == password:
            token = create_jwt(username)
            logger.info(json.dumps({"event": "login_success", "user": username}))
            return {"token": token}

    logger.warning(json.dumps({"event": "login_fail", "user": username, "reason": "invalid_credentials"}))
    raise HTTPException(401, "Invalid credentials")

# LOGOUT
@app.post("/logout")
async def logout(_):
    logger.info(json.dumps({"event": "logout"}))
    return {"detail": "Logged out"}

# STATUS (proxied)
@app.get("/status")
async def status(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        JWT_INVALID.inc()
        logger.warning(json.dumps({"event": "status_fail", "reason": "missing_token"}))
        raise HTTPException(401, "Missing or invalid token")

    token = auth_header.split(" ")[1]
    username = verify_jwt(token)

    if not username:
        JWT_INVALID.inc()
        logger.warning(json.dumps({"event": "status_fail", "reason": "invalid_token"}))
        raise HTTPException(401, "Invalid or expired token")

    STATUS_ALLOWED.labels(user=username).inc()
    logger.info(json.dumps({"event": "status_success", "user": username}))

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{UPSTREAM}/status")
    return JSONResponse(status_code=resp.status_code, content=resp.json())

# METRICS
@app.get("/metrics")
def metrics():
    return HTMLResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
