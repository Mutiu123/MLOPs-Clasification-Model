"""
Unit tests for us_visa.schemas module
"""
import pytest
from pydantic import ValidationError
from us_visa.schemas import (
    ContinentEnum,
    EducationEnum,
    RegionEnum,
    WageUnitEnum,
    USVisaPredictionRequest,
    USVisaPredictionResponse,
    TrainingResponse,
    HealthCheckResponse,
    ErrorResponse,
)


class TestEnums:
    """Test enum definitions"""

    def test_continent_enum_values(self):
        """Test continent enum has correct values"""
        assert ContinentEnum.ASIA.value == "asia"
        assert ContinentEnum.EUROPE.value == "europe"
        assert ContinentEnum.AMERICA.value == "america"

    def test_education_enum_values(self):
        """Test education enum has correct values"""
        assert EducationEnum.HIGH_SCHOOL.value == "high school"
        assert EducationEnum.BACHELOR.value == "bachelor"

    def test_region_enum_values(self):
        """Test region enum has correct values"""
        assert RegionEnum.NORTHEAST.value == "northeast"
        assert RegionEnum.SOUTH.value == "south"

    def test_wage_unit_enum_values(self):
        """Test wage unit enum has correct values"""
        assert WageUnitEnum.HOURLY.value == "hourly"
        assert WageUnitEnum.YEARLY.value == "yearly"


class TestUSVisaPredictionRequest:
    """Test visa prediction request model"""

    def test_valid_request(self, sample_visa_data):
        """Test creating valid prediction request"""
        request = USVisaPredictionRequest(**sample_visa_data)
        assert request.continent == "asia"
        assert request.education_of_employee == "bachelor"
        assert request.has_job_experience is True

    def test_invalid_continent(self, sample_visa_data):
        """Test validation with invalid continent"""
        sample_visa_data["continent"] = "invalid"
        with pytest.raises(ValidationError):
            USVisaPredictionRequest(**sample_visa_data)

    def test_negative_no_of_employees(self, sample_visa_data):
        """Test validation with negative employee count"""
        sample_visa_data["no_of_employees"] = -100
        with pytest.raises(ValidationError):
            USVisaPredictionRequest(**sample_visa_data)

    def test_negative_prevailing_wage(self, sample_visa_data):
        """Test validation with negative prevailing wage"""
        sample_visa_data["prevailing_wage"] = -1000
        with pytest.raises(ValidationError):
            USVisaPredictionRequest(**sample_visa_data)

    def test_invalid_education_level(self, sample_visa_data):
        """Test validation with invalid education level"""
        sample_visa_data["education_of_employee"] = "phd"
        with pytest.raises(ValidationError):
            USVisaPredictionRequest(**sample_visa_data)

    def test_required_fields(self):
        """Test that all fields are required"""
        with pytest.raises(ValidationError):
            USVisaPredictionRequest()

    def test_boolean_field_validation(self, sample_visa_data):
        """Test boolean field validation"""
        sample_visa_data["has_job_experience"] = "yes"
        request = USVisaPredictionRequest(**sample_visa_data)
        # Pydantic converts truthy values to boolean
        assert isinstance(request.has_job_experience, bool)

    def test_numeric_field_validation(self, sample_visa_data):
        """Test numeric field validation"""
        sample_visa_data["no_of_employees"] = "1000"
        request = USVisaPredictionRequest(**sample_visa_data)
        # Pydantic converts string numbers to int
        assert isinstance(request.no_of_employees, int)
        assert request.no_of_employees == 1000


class TestUSVisaPredictionResponse:
    """Test visa prediction response model"""

    def test_valid_response(self):
        """Test creating valid prediction response"""
        response = USVisaPredictionResponse(
            prediction="Visa-approved",
            confidence=0.95,
            status="success",
        )
        assert response.prediction == "Visa-approved"
        assert response.confidence == 0.95
        assert response.status == "success"

    def test_response_without_confidence(self):
        """Test response without confidence score"""
        response = USVisaPredictionResponse(
            prediction="Visa Not-Approved",
            status="success",
        )
        assert response.prediction == "Visa Not-Approved"
        assert response.confidence is None

    def test_invalid_prediction_value(self):
        """Test validation with invalid prediction value"""
        with pytest.raises(ValidationError):
            USVisaPredictionResponse(
                prediction="Maybe-Approved",
                status="success",
            )

    def test_confidence_bounds(self):
        """Test confidence score bounds validation"""
        with pytest.raises(ValidationError):
            USVisaPredictionResponse(
                prediction="Visa-approved",
                confidence=1.5,  # > 1.0
                status="success",
            )

        with pytest.raises(ValidationError):
            USVisaPredictionResponse(
                prediction="Visa-approved",
                confidence=-0.1,  # < 0.0
                status="success",
            )


class TestHealthCheckResponse:
    """Test health check response model"""

    def test_valid_health_check(self):
        """Test creating valid health check response"""
        response = HealthCheckResponse(
            status="healthy",
            version="1.0.0",
            timestamp="2024-01-28T10:00:00",
        )
        assert response.status == "healthy"
        assert response.version == "1.0.0"


class TestErrorResponse:
    """Test error response model"""

    def test_valid_error_response(self):
        """Test creating valid error response"""
        response = ErrorResponse(
            error="Validation error",
            detail="Invalid input data",
            request_id="abc123",
        )
        assert response.status == "failure"
        assert response.error == "Validation error"
        assert response.detail == "Invalid input data"

    def test_error_response_defaults(self):
        """Test error response with default values"""
        response = ErrorResponse(error="Test error")
        assert response.status == "failure"
        assert response.detail is None
        assert response.request_id is None
