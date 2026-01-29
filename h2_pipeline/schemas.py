"""
Pydantic models for API request/response validation
"""
from typing import Optional, Literal
from pydantic import BaseModel, Field, validator
from enum import Enum


class PipelineMaterialEnum(str, Enum):
    """Pipeline material options"""
    STEEL = "steel"
    STAINLESS_STEEL = "stainless_steel"
    COMPOSITE = "composite"
    ALUMINUM = "aluminum"


class LeakSeverityEnum(str, Enum):
    """Leak severity classification"""
    NO_LEAK = "no_leak"
    MINOR_LEAK = "minor_leak"
    MODERATE_LEAK = "moderate_leak"
    CRITICAL_LEAK = "critical_leak"


class H2SensorDataRequest(BaseModel):
    """Request model for hydrogen pipeline leak detection"""
    pressure_mpa: float = Field(..., gt=0, le=100, description="Pipeline pressure in MPa")
    temperature_celsius: float = Field(..., ge=-40, le=150, description="Temperature in Celsius")
    hydrogen_concentration_ppm: float = Field(..., ge=0, le=1000000, description="H2 concentration in ppm")
    vibration_hz: float = Field(..., ge=0, le=10000, description="Vibration frequency in Hz")
    pipe_age_years: int = Field(..., ge=0, le=100, description="Pipe age in years")
    material: PipelineMaterialEnum = Field(..., description="Pipeline material")
    flow_rate_kg_h: float = Field(..., gt=0, le=10000, description="Hydrogen flow rate in kg/h")
    corrosion_rate_mm_year: float = Field(..., ge=0, le=10, description="Corrosion rate in mm/year")
    soil_moisture_percent: float = Field(..., ge=0, le=100, description="Soil moisture percentage")
    operating_hours: int = Field(..., ge=0, description="Total operating hours")

    class Config:
        """Model configuration"""
        schema_extra = {
            "example": {
                "pressure_mpa": 35.5,
                "temperature_celsius": 45.2,
                "hydrogen_concentration_ppm": 5000,
                "vibration_hz": 250.5,
                "pipe_age_years": 15,
                "material": "steel",
                "flow_rate_kg_h": 2500,
                "corrosion_rate_mm_year": 0.5,
                "soil_moisture_percent": 65.0,
                "operating_hours": 125000,
            }
        }


class H2SensorDataResponse(BaseModel):
    """Response model for hydrogen pipeline leak detection"""
    leak_detected: bool = Field(..., description="Whether leak is detected")
    leak_severity: LeakSeverityEnum = Field(..., description="Severity of detected leak")
    confidence: Optional[float] = Field(
        None, description="Confidence score of prediction", ge=0.0, le=1.0
    )
    risk_score: Optional[float] = Field(
        None, description="Overall risk assessment score", ge=0.0, le=100.0
    )
    recommended_action: Optional[str] = Field(
        None, description="Recommended action based on prediction"
    )


class TrainingResponse(BaseModel):
    """Response model for training requests"""
    training_id: str
    status: str
    message: str
    timestamp: str


class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str
    version: str
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: str
