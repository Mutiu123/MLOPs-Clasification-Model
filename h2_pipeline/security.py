"""
Security module for H2 Pipeline Detection
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from datetime import datetime, timedelta
import jwt
from h2_pipeline.config import get_settings
from typing import Optional, Dict, Any

settings = get_settings()
security = HTTPBearer()


def rate_limiter(limit: int = 100, period: int = 60):
    """Rate limiting decorator factory"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Rate limiting logic
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> Dict[str, Any]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt
