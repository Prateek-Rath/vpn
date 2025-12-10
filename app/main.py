from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import logging
import sys
import json

# Structured JSON logger
logger = logging.getLogger("app")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "msg": %(message)s}'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = FastAPI()

STATUS_TOTAL = Counter("status_requests_total", "Total /status requests received")


@app.get("/status")
def status():
    STATUS_TOTAL.inc()
    logger.info(json.dumps({"event": "status_hit"}))
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
