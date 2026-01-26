# core/logger.py
import logging
import sys
import json
from datetime import datetime
from pythonjsonlogger import jsonlogger


class WebOpsLogger:
    """Logger JSON estructurado para aplicaciones WebOps"""

    @staticmethod
    def setup_logger(name="webops_app", level=logging.INFO):
        """
        Configura y retorna un logger en formato JSON

        Args:
            name (str): Nombre del logger
            level: Nivel de logging (INFO, DEBUG, etc.)

        Returns:
            logging.Logger: Logger configurado
        """
        # Crear logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Evitar logs duplicados
        if logger.handlers:
            return logger

        # Crear handler para stdout
        handler = logging.StreamHandler(sys.stdout)

        # Formateador JSON para cloud (AWS/Azure compatible)
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z',
            json_ensure_ascii=False
        )
        handler.setFormatter(formatter)

        # Agregar handler
        logger.addHandler(handler)

        # No propagar al logger raíz
        logger.propagate = False

        return logger


# Logger global para importar fácilmente
logger = WebOpsLogger.setup_logger()


def log_request(request_id, method, path, status_code, duration, client_ip=None):
    """Función helper para loguear peticiones HTTP"""
    logger.info(
        "http_request",
        extra={
            'request_id': request_id,
            'method': method,
            'path': path,
            'status_code': status_code,
            'duration_seconds': round(duration, 4),
            'client_ip': client_ip or 'unknown',
            'log_type': 'http_access'
        }
    )


def log_system_event(event, details=None):
    """Función helper para loguear eventos del sistema"""
    logger.info(
        event,
        extra={
            'log_type': 'system_event',
            'details': details or {}
        }
    )


def log_error(error_msg, exception=None, context=None):
    """Función helper para loguear errores"""
    extra = {
        'log_type': 'error',
        'error_message': error_msg,
        'context': context or {}
    }

    if exception:
        extra['exception_type'] = type(exception).__name__
        extra['exception_details'] = str(exception)

    logger.error("application_error", extra=extra)
