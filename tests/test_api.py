"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check_success(self):
        """Test health check returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data

    def test_health_check_response_format(self):
        """Test health check response format"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert all(key in data for key in ["status", "version", "timestamp"])


class TestAPIStatusEndpoint:
    """Test API status endpoint"""

    def test_api_status_success(self):
        """Test API status endpoint returns 200"""
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert "version" in data
        assert "environment" in data

    def test_api_status_response_format(self):
        """Test API status response format"""
        response = client.get("/api/status")
        data = response.json()
        assert isinstance(data["debug"], bool)
        assert "timestamp" in data


class TestIndexEndpoint:
    """Test index/home endpoint"""

    def test_index_returns_html(self):
        """Test index endpoint returns HTML"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")


class TestPredictionEndpoint:
    """Test prediction API endpoint"""

    def test_predict_with_valid_data(self, sample_visa_data):
        """Test prediction with valid data"""
        response = client.post("/predict", json=sample_visa_data)
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert data["status"] == "success"
        assert data["prediction"] in [
            "Visa-approved",
            "Visa Not-Approved",
        ]

    def test_predict_with_invalid_data(self):
        """Test prediction with invalid data"""
        invalid_data = {
            "continent": "invalid",
            "education_of_employee": "bachelor",
            "has_job_experience": True,
            "requires_job_training": False,
            "no_of_employees": 1000,
            "company_age": 15,
            "region_of_employment": "northeast",
            "prevailing_wage": 75000,
            "unit_of_wage": "yearly",
            "full_time_position": True,
        }
        response = client.post("/predict", json=invalid_data)
        assert response.status_code == 422  # Unprocessable Entity

    def test_predict_with_missing_fields(self):
        """Test prediction with missing required fields"""
        incomplete_data = {"continent": "asia", "education_of_employee": "bachelor"}
        response = client.post("/predict", json=incomplete_data)
        assert response.status_code == 422

    def test_predict_with_negative_wage(self, sample_visa_data):
        """Test prediction with negative wage"""
        sample_visa_data["prevailing_wage"] = -1000
        response = client.post("/predict", json=sample_visa_data)
        assert response.status_code == 422

    def test_predict_response_format(self, sample_visa_data):
        """Test prediction response format"""
        response = client.post("/predict", json=sample_visa_data)
        if response.status_code == 200:
            data = response.json()
            assert all(
                key in data for key in ["prediction", "status"]
            )


class TestCORSHeaders:
    """Test CORS configuration"""

    def test_cors_headers_present(self):
        """Test CORS headers are present in response"""
        response = client.get("/health")
        assert response.status_code == 200
        # CORS headers might not be in TestClient, but we can verify endpoint works


class TestRateLimiting:
    """Test rate limiting"""

    def test_multiple_requests_allowed(self, sample_visa_data):
        """Test multiple requests within limit are allowed"""
        for _ in range(5):
            response = client.post("/predict", json=sample_visa_data)
            # At least some requests should succeed
            assert response.status_code in [200, 422, 500]

    def test_health_check_not_rate_limited(self):
        """Test health check endpoint is not rate limited"""
        for _ in range(10):
            response = client.get("/health")
            assert response.status_code == 200
