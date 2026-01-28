"""
Middleware module for H2 Pipeline Detection
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from datetime import datetime
from uuid import uuid4
import contextvars
import time

from h2_pipeline.logging_config import logger
from h2_pipeline.metrics import MetricsCollector

# Context variable for request tracking
request_context = contextvars.ContextVar("request_context", default=None)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware to add request context"""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid4())
        request_context.set({"request_id": request_id, "timestamp": datetime.utcnow()})
        
        logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            extra={"request_id": request_id},
        )

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting"""

    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_times = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        
        if client_ip not in self.request_times:
            self.request_times[client_ip] = []

        now = time.time()
        one_minute_ago = now - 60

        # Remove old requests
        self.request_times[client_ip] = [
            req_time for req_time in self.request_times[client_ip] if req_time > one_minute_ago
        ]

        if len(self.request_times[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"},
            )

        self.request_times[client_ip].append(now)
        return await call_next(request)


class ExceptionMiddleware(BaseHTTPMiddleware):
    """Middleware for exception handling"""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "detail": str(e) if request.app.debug else "An error occurred",
                },
            )
