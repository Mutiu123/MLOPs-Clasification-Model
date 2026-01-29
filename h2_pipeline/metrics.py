"""
Metrics collection module for H2 Pipeline Detection
"""
from prometheus_client import Counter, Histogram, Gauge
from typing import Dict, List

# Prediction metrics
predictions_total = Counter(
    "h2_pipeline_predictions_total",
    "Total number of leak detection predictions",
    ["result"],
)

prediction_duration = Histogram(
    "h2_pipeline_prediction_duration_seconds",
    "Time spent making predictions",
)

leak_confidence = Histogram(
    "h2_pipeline_leak_confidence",
    "Confidence scores for leak detections",
    buckets=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
)

# Training metrics
training_total = Counter(
    "h2_pipeline_training_total",
    "Total number of model trainings",
    ["status"],
)

training_duration = Histogram(
    "h2_pipeline_training_duration_seconds",
    "Time spent training models",
)

model_accuracy = Gauge(
    "h2_pipeline_model_accuracy",
    "Current model accuracy score",
)

# Data metrics
sensor_readings_processed = Counter(
    "h2_pipeline_sensor_readings_processed_total",
    "Total sensor readings processed",
)

data_validation_errors = Counter(
    "h2_pipeline_data_validation_errors_total",
    "Total data validation errors",
)


class MetricsCollector:
    """Metrics collection helper class"""

    @staticmethod
    def record_prediction(result: str, duration: float, confidence: float = None):
        """Record a prediction metric"""
        predictions_total.labels(result=result).inc()
        prediction_duration.observe(duration)
        if confidence is not None:
            leak_confidence.observe(confidence)

    @staticmethod
    def record_training(status: str, duration: float, accuracy: float = None):
        """Record a training metric"""
        training_total.labels(status=status).inc()
        training_duration.observe(duration)
        if accuracy is not None:
            model_accuracy.set(accuracy)

    @staticmethod
    def record_sensor_reading():
        """Record sensor reading processed"""
        sensor_readings_processed.inc()

    @staticmethod
    def record_validation_error():
        """Record validation error"""
        data_validation_errors.inc()
