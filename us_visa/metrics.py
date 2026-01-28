"""
Monitoring and metrics module using Prometheus
"""
from prometheus_client import Counter, Histogram, Gauge
from datetime import datetime

# Prediction metrics
prediction_counter = Counter(
    "visa_predictions_total",
    "Total number of predictions",
    ["prediction_result"],
)

prediction_latency = Histogram(
    "visa_prediction_latency_seconds",
    "Prediction latency in seconds",
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

# Training metrics
training_counter = Counter(
    "model_training_total",
    "Total number of model trainings",
    ["status"],
)

training_latency = Histogram(
    "model_training_latency_seconds",
    "Training latency in seconds",
)

# Data validation metrics
data_validation_counter = Counter(
    "data_validation_total",
    "Total number of data validations",
    ["status"],
)

# Error metrics
error_counter = Counter(
    "errors_total",
    "Total number of errors",
    ["error_type"],
)

# Active requests gauge
active_requests_gauge = Gauge(
    "active_requests",
    "Number of active requests",
)

# Model performance gauge
model_accuracy_gauge = Gauge(
    "model_accuracy",
    "Current model accuracy",
)

model_f1_score_gauge = Gauge(
    "model_f1_score",
    "Current model F1 score",
)

# Data drift gauge
data_drift_gauge = Gauge(
    "data_drift_value",
    "Current data drift value",
)


class MetricsCollector:
    """Utility class for collecting metrics"""

    @staticmethod
    def record_prediction(result: str, duration: float) -> None:
        """Record prediction metric"""
        prediction_counter.labels(prediction_result=result).inc()
        prediction_latency.observe(duration)

    @staticmethod
    def record_training(status: str, duration: float) -> None:
        """Record training metric"""
        training_counter.labels(status=status).inc()
        training_latency.observe(duration)

    @staticmethod
    def record_validation(status: str) -> None:
        """Record validation metric"""
        data_validation_counter.labels(status=status).inc()

    @staticmethod
    def record_error(error_type: str) -> None:
        """Record error metric"""
        error_counter.labels(error_type=error_type).inc()

    @staticmethod
    def set_model_performance(accuracy: float, f1_score: float) -> None:
        """Set model performance metrics"""
        model_accuracy_gauge.set(accuracy)
        model_f1_score_gauge.set(f1_score)

    @staticmethod
    def set_data_drift(drift_value: float) -> None:
        """Set data drift metric"""
        data_drift_gauge.set(drift_value)

    @staticmethod
    def increment_active_requests() -> None:
        """Increment active requests gauge"""
        active_requests_gauge.inc()

    @staticmethod
    def decrement_active_requests() -> None:
        """Decrement active requests gauge"""
        active_requests_gauge.dec()
