"""
Security and authentication module
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import JWTError, jwt
from us_visa.config import get_settings
from us_visa.logging_config import logger

security = HTTPBearer()
settings = get_settings()


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Verify JWT token and return decoded payload
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def sanitize_input(input_string: str, max_length: int = 1000) -> str:
    """
    Sanitize user input to prevent injection attacks
    """
    if len(input_string) > max_length:
        raise ValueError(f"Input exceeds maximum length of {max_length}")

    # Remove potential harmful characters
    dangerous_chars = ["<", ">", "&", '"', "'", "%", ";", "\\"]
    sanitized = input_string
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "")

    return sanitized.strip()


class RateLimiter:
    """
    Simple in-memory rate limiter
    For production, use redis-based rate limiting
    """

    def __init__(self, requests: int = 100, period: int = 60):
        self.requests = requests
        self.period = period
        self.requests_history: Dict[str, list] = {}

    def is_allowed(self, client_id: str) -> bool:
        """
        Check if client is within rate limit
        """
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=self.period)

        if client_id not in self.requests_history:
            self.requests_history[client_id] = []

        # Remove old requests outside the period
        self.requests_history[client_id] = [
            req_time
            for req_time in self.requests_history[client_id]
            if req_time > cutoff
        ]

        # Check if limit exceeded
        if len(self.requests_history[client_id]) >= self.requests:
            return False

        # Add current request
        self.requests_history[client_id].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter(
    requests=settings.RATE_LIMIT_REQUESTS, period=settings.RATE_LIMIT_PERIOD
)
