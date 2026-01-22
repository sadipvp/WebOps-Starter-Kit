import logging
import sys
from pythonjsonlogger import jsonlogger
from uuid import uuid4
from datetime import datetime
from time import time


from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles


""" Logging Configuration """
log_handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s'






app=FastAPI(title="WebOps Starter Kit", version="0.1.0")
START_TS=time()
templates=Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")



@ app.middleware("http")
async def monitor_requests(request: Request, call_next):
    request_id=str(uuid4())
    start_time=time()

    response=await call_next(request)

    duration=round(time() - start_time, 4)

    logger.info(
        f"request_id={request_id} "
        f"method={request.method} "
        f"path={request.url.path} "
        f"status={response.status_code} "
        f"duration={duration}s"
    )

    response.headers["X-Request-ID"]=request_id
    response.headers["X-Response-Time"]=str(duration)

    return response




@ app.get("/")
def dashboard(request: Request):
    uptime_seconds=int(time() - START_TS)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "service": "WebOps Starter Kit",
            "status": "UP",
            "uptime_seconds":   uptime_seconds,
            "now":  datetime.utcnow().isoformat(),
            "version": app.version,

        },
    )


@ app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@ app.get("/health")
async def health_check():
    return {"status": "UP"}


@ app.get("/metrics")
async def metrics():
    uptime_seconds=int(time() - START_TS)
    return (
        "web_ops_uptime_seconds " + str(uptime_seconds) + "\n"
    )


@ app.get("/debug/headers")
def debug_headers(request: Request):
    return dict(request.headers)
