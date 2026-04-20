import logging
import os
import socket
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="okd-poc", version="0.1.0")
logger = logging.getLogger("okd-poc")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

counter = 0


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(
        "%s %s status=%s client=%s",
        request.method,
        request.url.path,
        response.status_code,
        request.client.host if request.client else "unknown",
    )
    return response


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "message": "FastAPI OKD POC running",
        "hostname": socket.gethostname(),
    }


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "OK"}


@app.get("/env")
def env() -> JSONResponse:
    relevant_env = {
        "APP_NAME": os.getenv("APP_NAME", "okd-poc"),
        "APP_ENV": os.getenv("APP_ENV", "dev"),
        "PORT": os.getenv("PORT", "8000"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    }
    return JSONResponse(content=relevant_env)


@app.get("/counter")
def in_memory_counter() -> Dict[str, int]:
    global counter
    counter += 1
    return {"counter": counter}
