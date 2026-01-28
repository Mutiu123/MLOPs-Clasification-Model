"""
Middleware for FastAPI application
"""
import time
import uuid
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from us_visa.logging_config import logger
from us_visa.security import rate_limiter, sanitize_input
import json


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware to add request context and logging"""

    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Log request
        start_time = time.time()
        logger.info(
            json.dumps(
                {
                    "event": "request_started",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "client": request.client[0] if request.client else None,
                }
            )
        )

        try:
            response = await call_next(request)

            # Log response
            duration = time.time() - start_time
            logger.info(
                json.dumps(
                    {
                        "event": "request_completed",
                        "request_id": request_id,
                        "status_code": response.status_code,
                        "duration_seconds": round(duration, 3),
                    }
                )
            )

            response.headers["X-Request-ID"] = request_id
            return response

        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                json.dumps(
                    {
                        "event": "request_error",
                        "request_id": request_id,
                        "error": str(e),
                        "duration_seconds": round(duration, 3),
                    }
                )
            )
            raise


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting"""

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client[0] if request.client else "unknown"

        # Skip rate limiting for health check
        if request.url.path == "/health":
            return await call_next(request)

        if not rate_limiter.is_allowed(client_ip):
            logger.warning(
                f"Rate limit exceeded for client: {client_ip}"
            )
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded. Too many requests."},
            )

        response = await call_next(request)
        return response


class ExceptionMiddleware(BaseHTTPMiddleware):
    """Global exception handling middleware"""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": str(e), "request_id": request.state.request_id},
            )
        except Exception as e:
            request_id = getattr(request.state, "request_id", "unknown")
            logger.error(
                f"Unhandled exception (request_id: {request_id}): {str(e)}"
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error",
                    "request_id": request_id,
                },
            )
