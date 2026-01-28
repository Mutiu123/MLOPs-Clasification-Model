"""
Unit tests for us_visa.exception module
"""
import pytest
import sys
from us_visa.exception import USvisaException


class TestUSvisaException:
    """Test custom exception handling"""

    def test_exception_message_formatting(self):
        """Test that exception formats error message correctly"""
        error_msg = "Test error message"

        with pytest.raises(USvisaException) as exc_info:
            raise USvisaException(error_msg, sys)

        exception = exc_info.value
        assert isinstance(exception.error_message, str)
        assert "Error occurred" in exception.error_message

    def test_exception_traceback_info(self):
        """Test that exception captures traceback information"""
        try:
            # Intentionally cause an error
            x = 1 / 0
        except ZeroDivisionError as e:
            with pytest.raises(USvisaException) as exc_info:
                raise USvisaException(e, sys)

            exception = exc_info.value
            assert exception.error_message is not None

    def test_exception_string_representation(self):
        """Test string representation of exception"""
        error_msg = "Test error"

        with pytest.raises(USvisaException) as exc_info:
            raise USvisaException(error_msg, sys)

        exception = exc_info.value
        assert str(exception) == exception.error_message

    def test_exception_with_nested_error(self):
        """Test exception with nested exception handling"""
        try:
            try:
                raise ValueError("Inner error")
            except ValueError as e:
                raise USvisaException(str(e), sys)
        except USvisaException as e:
            assert e.error_message is not None
            assert "Inner error" in str(e)
