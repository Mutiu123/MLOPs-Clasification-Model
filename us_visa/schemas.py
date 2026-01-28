"""
Pydantic models for API request/response validation
"""
from typing import Optional, Literal
from pydantic import BaseModel, Field, validator
from enum import Enum


class ContinentEnum(str, Enum):
    """Continent options"""
    ASIA = "asia"
    EUROPE = "europe"
    AMERICA = "america"
    AFRICA = "africa"
    OCEANIA = "oceania"


class EducationEnum(str, Enum):
    """Education level options"""
    HIGH_SCHOOL = "high school"
    BACHELOR = "bachelor"
    MASTER = "master"
    DOCTORATE = "doctorate"


class RegionEnum(str, Enum):
    """Employment region options"""
    NORTHEAST = "northeast"
    MIDWEST = "midwest"
    SOUTH = "south"
    WEST = "west"


class WageUnitEnum(str, Enum):
    """Wage unit options"""
    HOURLY = "hourly"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class USVisaPredictionRequest(BaseModel):
    """Request model for visa prediction"""
    continent: ContinentEnum = Field(..., description="Applicant's continent")
    education_of_employee: EducationEnum = Field(..., description="Employee's education level")
    has_job_experience: bool = Field(..., description="Whether applicant has job experience")
    requires_job_training: bool = Field(..., description="Whether job training is required")
    no_of_employees: int = Field(..., ge=1, le=50000, description="Number of employees in company")
    company_age: int = Field(..., ge=0, le=200, description="Company age in years")
    region_of_employment: RegionEnum = Field(..., description="Employment region")
    prevailing_wage: float = Field(..., gt=0, description="Prevailing wage amount")
    unit_of_wage: WageUnitEnum = Field(..., description="Unit of wage")
    full_time_position: bool = Field(..., description="Whether position is full-time")

    class Config:
        """Model configuration"""
        schema_extra = {
            "example": {
                "continent": "asia",
                "education_of_employee": "bachelor",
                "has_job_experience": True,
                "requires_job_training": False,
                "no_of_employees": 1000,
                "company_age": 15,
                "region_of_employment": "northeast",
                "prevailing_wage": 75000.00,
                "unit_of_wage": "yearly",
                "full_time_position": True,
            }
        }


class USVisaPredictionResponse(BaseModel):
    """Response model for visa prediction"""
    prediction: Literal["Visa-approved", "Visa Not-Approved"] = Field(
        ..., description="Prediction result"
    )
    confidence: Optional[float] = Field(
        None, description="Confidence score of prediction", ge=0.0, le=1.0
    )
    status: Literal["success", "failure"] = Field(..., description="Status of prediction")

    class Config:
        """Model configuration"""
        schema_extra = {
            "example": {
                "prediction": "Visa-approved",
                "confidence": 0.95,
                "status": "success",
            }
        }


class TrainingResponse(BaseModel):
    """Response model for training endpoint"""
    status: Literal["success", "failure"] = Field(..., description="Training status")
    message: str = Field(..., description="Training result message")
    artifacts_location: Optional[str] = Field(None, description="Location of saved artifacts")


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Current timestamp")


class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = Field("failure", description="Response status")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    request_id: Optional[str] = Field(None, description="Unique request identifier")
