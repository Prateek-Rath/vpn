from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx
import json

from utils import create_jwt, verify_jwt
from metrics import STATUS_ALLOWED, JWT_INVALID, UPSTREAM_ERRORS
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Load creds
with open("creds.json") as f:
    CREDS = json.load(f)["creds"]

UPSTREAM = "http://app:9002"

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    with open("static/index.html") as f:
        return f.read()

# LOGIN
@app.post("/login")
async def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise HTTPException(400, "Missing username or password")

    for cred in CREDS:
        if cred["username"] == username and cred["password"] == password:
            return {"token": create_jwt(username)}

    raise HTTPException(401, "Invalid credentials")

# LOGOUT
@app.post("/logout")
async def logout(_):
    return {"detail": "Logged out"}

# STATUS (proxied)
@app.get("/status")
async def status(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        JWT_INVALID.inc()
        raise HTTPException(401, "Missing or invalid token")

    token = auth_header.split(" ")[1]
    username = verify_jwt(token)

    if not username:
        JWT_INVALID.inc()
        raise HTTPException(401, "Invalid or expired token")

    STATUS_ALLOWED.labels(user=username).inc()

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{UPSTREAM}/status")
        return JSONResponse(status_code=resp.status_code, content=resp.json())
    except Exception:
        UPSTREAM_ERRORS.inc()
        raise HTTPException(502, "Upstream error")

# METRICS
@app.get("/metrics")
def metrics():
    return HTMLResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
