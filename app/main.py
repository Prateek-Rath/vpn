from fastapi import FastAPI
from fastapi.responses import Response
import logging
import sys
import json

logger = logging.getLogger("app")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "msg": %(message)s}'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = FastAPI()

@app.get("/status")
def status():
    logger.info(json.dumps({"event": "status_hit"}))
    return {"status": "ok"}