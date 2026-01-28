"""
Unit tests for us_visa.utils.main_utils module
"""
import pytest
import os
import tempfile
import yaml
import numpy as np
from us_visa.utils.main_utils import (
    read_yaml_file,
    write_yaml_file,
    load_object,
    save_object,
    load_numpy_array_data,
    save_numpy_array_data,
)


class TestYamlOperations:
    """Test YAML file operations"""

    def test_write_and_read_yaml_file(self):
        """Test writing and reading YAML file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test.yaml")
            test_data = {"key1": "value1", "key2": ["item1", "item2"]}

            # Write YAML
            write_yaml_file(file_path, test_data)
            assert os.path.exists(file_path)

            # Read YAML
            loaded_data = read_yaml_file(file_path)
            assert loaded_data == test_data

    def test_write_yaml_with_replace(self):
        """Test writing YAML with replace option"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test.yaml")
            original_data = {"original": True}
            new_data = {"new": False}

            # Write original
            write_yaml_file(file_path, original_data)

            # Write with replace
            write_yaml_file(file_path, new_data, replace=True)

            # Verify replacement
            loaded_data = read_yaml_file(file_path)
            assert loaded_data == new_data

    def test_yaml_nonexistent_file(self):
        """Test reading non-existent YAML file raises error"""
        with pytest.raises(Exception):
            read_yaml_file("/nonexistent/path/file.yaml")


class TestObjectSerialization:
    """Test object serialization operations"""

    def test_save_and_load_object(self):
        """Test saving and loading Python objects"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test_object.pkl")
            test_object = {"data": [1, 2, 3], "value": 42}

            # Save object
            save_object(file_path, test_object)
            assert os.path.exists(file_path)

            # Load object
            loaded_object = load_object(file_path)
            assert loaded_object == test_object

    def test_save_object_creates_directory(self):
        """Test save_object creates missing directories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "nested", "dir", "test.pkl")
            test_object = {"test": "data"}

            save_object(file_path, test_object)
            assert os.path.exists(file_path)


class TestNumpyOperations:
    """Test numpy array file operations"""

    def test_save_and_load_numpy_array(self):
        """Test saving and loading numpy arrays"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test_array.npy")
            test_array = np.array([[1, 2, 3], [4, 5, 6]])

            # Save array
            save_numpy_array_data(file_path, test_array)
            assert os.path.exists(file_path)

            # Load array
            loaded_array = load_numpy_array_data(file_path)
            np.testing.assert_array_equal(loaded_array, test_array)

    def test_numpy_array_with_different_dtypes(self):
        """Test numpy operations with different data types"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test float array
            float_array = np.array([1.5, 2.5, 3.5], dtype=np.float32)
            float_path = os.path.join(tmpdir, "float.npy")
            save_numpy_array_data(float_path, float_array)
            loaded_float = load_numpy_array_data(float_path)
            np.testing.assert_array_equal(loaded_float, float_array)

            # Test integer array
            int_array = np.array([1, 2, 3], dtype=np.int64)
            int_path = os.path.join(tmpdir, "int.npy")
            save_numpy_array_data(int_path, int_array)
            loaded_int = load_numpy_array_data(int_path)
            np.testing.assert_array_equal(loaded_int, int_array)
