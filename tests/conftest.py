"""
Test configuration and fixtures for the US Visa project
"""
import pytest
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from us_visa.logger import logging
from us_visa.config import get_settings


@pytest.fixture(scope="session")
def settings():
    """Get application settings"""
    return get_settings()


@pytest.fixture
def logger_instance():
    """Get logger instance"""
    return logging


@pytest.fixture
def sample_visa_data():
    """Sample visa prediction data for testing"""
    return {
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


@pytest.fixture
def invalid_visa_data():
    """Invalid visa prediction data for testing"""
    return {
        "continent": "invalid",
        "education_of_employee": "unknown",
        "has_job_experience": "yes",  # Should be boolean
        "requires_job_training": "no",  # Should be boolean
        "no_of_employees": -100,  # Should be positive
        "company_age": -5,  # Should be positive
        "region_of_employment": "invalid",
        "prevailing_wage": -1000,  # Should be positive
        "unit_of_wage": "invalid",
        "full_time_position": "maybe",  # Should be boolean
    }
