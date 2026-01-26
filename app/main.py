

from .core.middlewares import setup_middlewares
from .core.logger import logger, log_system_event, log_error
from datetime import datetime
from time import time


from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles


app = FastAPI(title="WebOps Starter Kit", version="0.1.0")
START_TS = time()
templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def dashboard(request: Request):
    uptime_seconds = int(time() - START_TS)
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


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/health")
async def health_check():
    return {"status": "UP"}


@app.get("/metrics")
async def metrics():
    uptime_seconds = int(time() - START_TS)
    return (
        "web_ops_uptime_seconds " + str(uptime_seconds) + "\n"
    )


@app.get("/debug/headers")
def debug_headers(request: Request):
    return dict(request.headers)


@app.get("/test-log")
def test_log():
    # Prueba de logging
    logger.info("Este es un mensaje de prueba desde el endpoint /test-log", extra={
        'test': True,
        'mi_campo': 'valor_ejemplo'
    })
    return {"message": "Test log realizado"}
