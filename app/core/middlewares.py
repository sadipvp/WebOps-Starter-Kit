from uuid import uuid4
from time import time
from fastapi import Request


def setup_middlewares(app):
    """Configura middlewares de monitoreo para la aplicación"""

    @app.middleware("http")
    async def monitoring_middleware(request: Request, call_next):
        request_id = str(uuid4())
        start_time = time()

        # Guardar en el estado de request
        request.state.request_id = request_id

        response = await call_next(request)
        duration = time() - start_time

        # Importar logger aquí para evitar dependencias circulares
        from .logger import logger

        logger.info(
            "http_request",
            extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.url.path,
                'status_code': response.status_code,
                'duration_seconds': round(duration, 4),
                'client_ip': request.client.host if request.client else None
            }
        )

        # Headers de trazabilidad
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = str(round(duration, 4))

        return response

    return app
