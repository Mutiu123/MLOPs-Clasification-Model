"""
Production-ready FastAPI application for Hydrogen Pipeline Leak Detection
"""
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run
from prometheus_client import make_asgi_app
import uvicorn

from typing import Optional
from datetime import datetime

from h2_pipeline.constants import APP_HOST, APP_PORT
from h2_pipeline.pipline.prediction_pipeline import H2SensorData, H2PipelineLeakDetector
from h2_pipeline.pipline.training_pipeline import TrainPipeline
from h2_pipeline.schemas import (
    H2SensorDataRequest,
    H2SensorDataResponse,
    TrainingResponse,
    HealthCheckResponse,
    ErrorResponse,
)
from h2_pipeline.config import get_settings
from h2_pipeline.logging_config import logger, log_prediction, log_model_training, log_error_event
from h2_pipeline.middleware import (
    RequestContextMiddleware,
    RateLimitMiddleware,
    ExceptionMiddleware,
)
from h2_pipeline.metrics import MetricsCollector
from h2_pipeline.security import rate_limiter

# Initialize settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title="Hydrogen Pipeline Leak Detection API",
    description="Production-ready ML model for hydrogen pipeline leak detection and characterization",
    version=settings.API_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Add middleware - order matters!
app.add_middleware(ExceptionMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestContextMiddleware)

# Add CORS middleware with restrictive settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=600,
)


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Application starting up")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Application shutting down")


@app.get("/health", tags=["health"], response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns:
        HealthCheckResponse: Service status and version
    """
    return HealthCheckResponse(
        status="healthy",
        version=settings.API_VERSION,
        timestamp=datetime.utcnow().isoformat(),
    )


@app.get("/", tags=["web"])
async def index(request: Request):
    """
    Serve the main hydrogen pipeline leak detection form
    
    Args:
        request: FastAPI Request object
        
    Returns:
        HTML template response
    """
    return templates.TemplateResponse(
        "h2_pipeline.html", {"request": request, "context": "Rendering"}
    )


@app.get("/train", tags=["training"], response_model=TrainingResponse)
async def train_route_client():
    """
    Trigger model training pipeline for hydrogen leak detection
    
    Returns:
        TrainingResponse: Training status and message
        
    Raises:
        HTTPException: If training fails
    """
    request_id = None
    start_time = time.time()
    
    try:
        logger.info("Hydrogen pipeline training pipeline initiated")
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        
        duration = time.time() - start_time
        MetricsCollector.record_training("success", duration)
        
        log_model_training(
            "success",
            {"duration_seconds": duration, "timestamp": datetime.utcnow().isoformat()}
        )
        
        return TrainingResponse(
            training_id="h2_pipeline_training",
            status="success",
            message="Model training completed successfully for hydrogen pipeline leak detection",
            timestamp=datetime.utcnow().isoformat(),
        )

    except Exception as e:
        duration = time.time() - start_time
        MetricsCollector.record_training("failure", duration)
        
        error_msg = f"Training failed: {str(e)}"
        log_error_event(error_msg)
        logger.error(error_msg)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg,
        )


@app.post(
    "/predict",
    tags=["prediction"],
    response_model=H2SensorDataResponse,
    responses={422: {"model": ErrorResponse}},
)
async def predict_api(request: H2SensorDataRequest):
    """
    API endpoint for hydrogen pipeline leak detection using JSON input
    
    Args:
        request: H2SensorDataRequest with all sensor data
        
    Returns:
        H2SensorDataResponse: Leak detection result and confidence
        
    Raises:
        HTTPException: If prediction fails
    """
    start_time = time.time()
    request_id = None
    
    try:
        logger.info(f"Leak detection request received: {request.dict()}")
        
        # Create H2SensorData object from request
        h2_data = H2SensorData(
            pressure_mpa=request.pressure_mpa,
            temperature_celsius=request.temperature_celsius,
            hydrogen_concentration_ppm=request.hydrogen_concentration_ppm,
            vibration_hz=request.vibration_hz,
            pipe_age_years=request.pipe_age_years,
            material=request.material,
            flow_rate_kg_h=request.flow_rate_kg_h,
            corrosion_rate_mm_year=request.corrosion_rate_mm_year,
            soil_moisture_percent=request.soil_moisture_percent,
            operating_hours=request.operating_hours,
        )

        h2_df = h2_data.get_h2_input_data_frame()

        # Make prediction
        model_predictor = H2PipelineLeakDetector()
        prediction_value = model_predictor.predict(dataframe=h2_df)[0]

        # Convert to readable format
        leak_detected = prediction_value == 1
        leak_severity = "critical_leak" if leak_detected else "no_leak"
        
        duration = time.time() - start_time
        
        # Record metrics
        MetricsCollector.record_prediction(leak_severity, duration)
        
        # Log prediction
        log_prediction(
            input_data=request.dict(),
            prediction=leak_severity,
            confidence=None,
            request_id=request_id,
        )

        return H2SensorDataResponse(
            leak_detected=leak_detected,
            leak_severity=leak_severity,
            confidence=None,
            risk_score=None,
            recommended_action="Monitor pipeline" if leak_detected else "Continue normal operations",
        )

    except ValueError as e:
        log_error_event(str(e), {"type": "validation_error"})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        error_msg = f"Leak detection failed: {str(e)}"
        log_error_event(error_msg)
        MetricsCollector.record_validation_error()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg,
        )


@app.post("/", tags=["web"])
async def predict_route_client(request: Request):
    """
    Web form endpoint for hydrogen pipeline leak detection
    
    Args:
        request: FastAPI Request object with form data
        
    Returns:
        HTML template response with leak detection result
    """
    start_time = time.time()
    
    try:
        form = await request.form()
        
        # Extract form data
        h2_data = H2SensorData(
            pressure_mpa=float(form.get("pressure_mpa")),
            temperature_celsius=float(form.get("temperature_celsius")),
            hydrogen_concentration_ppm=float(form.get("hydrogen_concentration_ppm")),
            vibration_hz=float(form.get("vibration_hz")),
            pipe_age_years=int(form.get("pipe_age_years")),
            material=form.get("material"),
            flow_rate_kg_h=float(form.get("flow_rate_kg_h")),
            corrosion_rate_mm_year=float(form.get("corrosion_rate_mm_year")),
            soil_moisture_percent=float(form.get("soil_moisture_percent")),
            operating_hours=int(form.get("operating_hours")),
        )

        h2_df = h2_data.get_h2_input_data_frame()

        model_predictor = H2PipelineLeakDetector()
        prediction_value = model_predictor.predict(dataframe=h2_df)[0]

        leak_detected = prediction_value == 1
        leak_status = "LEAK DETECTED" if leak_detected else "NO LEAK"
        
        duration = time.time() - start_time
        MetricsCollector.record_prediction(leak_status, duration)
        
        log_prediction(
            input_data=h2_data.get_h2_data_as_dict(),
            prediction=leak_status,
        )

        return templates.TemplateResponse(
            "h2_pipeline.html",
            {"request": request, "context": leak_status},
        )

    except Exception as e:
        error_msg = f"Web leak detection failed: {str(e)}"
        log_error_event(error_msg)
        MetricsCollector.record_validation_error()
        
        return templates.TemplateResponse(
            "h2_pipeline.html",
            {
                "request": request,
                "context": f"Error: {str(e)}",
                "error": True,
            },
        )


@app.get("/api/status", tags=["monitoring"])
async def api_status():
    """
    Get API status and configuration information
    
    Returns:
        dict: Status information
    """
    return {
        "status": "running",
        "service": "Hydrogen Pipeline Leak Detection",
        "environment": settings.ENVIRONMENT,
        "version": settings.API_VERSION,
        "debug": settings.DEBUG,
        "timestamp": datetime.utcnow().isoformat(),
    }


if __name__ == "__main__":
    logger.info(
        f"Starting Hydrogen Pipeline Leak Detection application on {settings.APP_HOST}:{settings.APP_PORT}"
    )
    app_run(app, host=settings.APP_HOST, port=settings.APP_PORT, reload=settings.DEBUG)