"""
Artifact entity for H2 pipeline leak detection
"""
from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str


@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_file_path: str


@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: dict


@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float


@dataclass
class ModelPusherArtifact:
    bucket_name: str
    s3_model_path: str
