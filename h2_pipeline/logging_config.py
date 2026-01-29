"""
Enhanced structured logging module for H2 Pipeline Detection
"""
import logging
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from pythonjsonlogger import jsonlogger
from h2_pipeline.config import get_settings

settings = get_settings()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional metadata"""

    def add_fields(
        self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]
    ) -> None:
        """Add custom fields to log record"""
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record["timestamp"] = datetime.utcnow().isoformat()
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record["module"] = record.module
        log_record["function"] = record.funcName
        log_record["line"] = record.lineno


def setup_logging() -> logging.Logger:
    """
    Setup structured logging with both file and console handlers
    Returns the configured logger instance
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    json_log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

    logger = logging.getLogger("h2_pipeline")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Remove existing handlers
    logger.handlers = []

    # JSON File Handler - for structured logs
    json_handler = logging.FileHandler(json_log_file)
    json_handler.setFormatter(
        CustomJsonFormatter("%(timestamp)s %(level)s %(name)s %(message)s")
    )
    logger.addHandler(json_handler)

    # Plain Text File Handler - for readability
    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter(
        "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console Handler - for development
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(file_formatter)
    logger.addHandler(console_handler)

    return logger


# Initialize logger
logger = setup_logging()


def log_prediction(
    input_data: Dict[str, Any],
    prediction: str,
    confidence: Optional[float] = None,
    request_id: Optional[str] = None,
) -> None:
    """
    Log prediction with audit trail
    """
    logger.info(
        json.dumps(
            {
                "event": "leak_detection",
                "request_id": request_id,
                "input": input_data,
                "prediction": prediction,
                "confidence": confidence,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
    )


def log_model_training(status: str, details: Dict[str, Any]) -> None:
    """
    Log model training events
    """
    logger.info(
        json.dumps(
            {
                "event": "model_training",
                "status": status,
                "details": details,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
    )


def log_error_event(error: str, context: Optional[Dict[str, Any]] = None) -> None:
    """
    Log error events with context
    """
    logger.error(
        json.dumps(
            {
                "event": "error",
                "error": error,
                "context": context,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
    )
