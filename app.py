"""
Production-ready FastAPI application for US Visa Prediction
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

from us_visa.constants import APP_HOST, APP_PORT
from us_visa.pipline.prediction_pipeline import USvisaData, USvisaClassifier
from us_visa.pipline.training_pipeline import TrainPipeline
from us_visa.schemas import (
    USVisaPredictionRequest,
    USVisaPredictionResponse,
    TrainingResponse,
    HealthCheckResponse,
    ErrorResponse,
)
from us_visa.config import get_settings
from us_visa.logging_config import logger, log_prediction, log_model_training, log_error_event
from us_visa.middleware import (
    RequestContextMiddleware,
    RateLimitMiddleware,
    ExceptionMiddleware,
)
from us_visa.metrics import MetricsCollector
from us_visa.security import rate_limiter

# Initialize settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title="US Visa Prediction API",
    description="Production-ready ML model for visa approval prediction",
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
    Serve the main prediction form
    
    Args:
        request: FastAPI Request object
        
    Returns:
        HTML template response
    """
    return templates.TemplateResponse(
        "usvisa.html", {"request": request, "context": "Rendering"}
    )


@app.get("/train", tags=["training"], response_model=TrainingResponse)
async def train_route_client():
    """
    Trigger model training pipeline
    
    Returns:
        TrainingResponse: Training status and message
        
    Raises:
        HTTPException: If training fails
    """
    request_id = None
    start_time = time.time()
    
    try:
        logger.info("Training pipeline initiated")
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        
        duration = time.time() - start_time
        MetricsCollector.record_training("success", duration)
        
        log_model_training(
            "success",
            {"duration_seconds": duration, "timestamp": datetime.utcnow().isoformat()}
        )
        
        return TrainingResponse(
            status="success",
            message="Model training completed successfully",
            artifacts_location="artifact/",
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
    response_model=USVisaPredictionResponse,
    responses={422: {"model": ErrorResponse}},
)
async def predict_api(request: USVisaPredictionRequest):
    """
    API endpoint for visa prediction using JSON input
    
    Args:
        request: USVisaPredictionRequest with all required features
        
    Returns:
        USVisaPredictionResponse: Prediction result and confidence
        
    Raises:
        HTTPException: If prediction fails
    """
    start_time = time.time()
    request_id = None
    
    try:
        logger.info(f"Prediction request received: {request.dict()}")
        
        # Create USvisaData object from request
        usvisa_data = USvisaData(
            continent=request.continent,
            education_of_employee=request.education_of_employee,
            has_job_experience=request.has_job_experience,
            requires_job_training=request.requires_job_training,
            no_of_employees=request.no_of_employees,
            company_age=request.company_age,
            region_of_employment=request.region_of_employment,
            prevailing_wage=request.prevailing_wage,
            unit_of_wage=request.unit_of_wage,
            full_time_position=request.full_time_position,
        )

        usvisa_df = usvisa_data.get_usvisa_input_data_frame()

        # Make prediction
        model_predictor = USvisaClassifier()
        prediction_value = model_predictor.predict(dataframe=usvisa_df)[0]

        # Convert to readable format
        prediction_result = "Visa-approved" if prediction_value == 1 else "Visa Not-Approved"
        
        duration = time.time() - start_time
        
        # Record metrics
        MetricsCollector.record_prediction(prediction_result, duration)
        
        # Log prediction
        log_prediction(
            input_data=request.dict(),
            prediction=prediction_result,
            confidence=None,
            request_id=request_id,
        )

        return USVisaPredictionResponse(
            prediction=prediction_result,
            confidence=None,
            status="success",
        )

    except ValueError as e:
        log_error_event(str(e), {"type": "validation_error"})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        error_msg = f"Prediction failed: {str(e)}"
        log_error_event(error_msg)
        MetricsCollector.record_error("prediction_error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg,
        )


@app.post("/", tags=["web"])
async def predict_route_client(request: Request):
    """
    Web form endpoint for visa prediction
    
    Args:
        request: FastAPI Request object with form data
        
    Returns:
        HTML template response with prediction result
    """
    start_time = time.time()
    
    try:
        form = await request.form()
        
        # Extract form data
        usvisa_data = USvisaData(
            continent=form.get("continent"),
            education_of_employee=form.get("education_of_employee"),
            has_job_experience=form.get("has_job_experience") == "on",
            requires_job_training=form.get("requires_job_training") == "on",
            no_of_employees=int(form.get("no_of_employees")),
            company_age=int(form.get("company_age")),
            region_of_employment=form.get("region_of_employment"),
            prevailing_wage=float(form.get("prevailing_wage")),
            unit_of_wage=form.get("unit_of_wage"),
            full_time_position=form.get("full_time_position") == "on",
        )

        usvisa_df = usvisa_data.get_usvisa_input_data_frame()

        model_predictor = USvisaClassifier()
        prediction_value = model_predictor.predict(dataframe=usvisa_df)[0]

        status_result = "Visa-approved" if prediction_value == 1 else "Visa Not-Approved"
        
        duration = time.time() - start_time
        MetricsCollector.record_prediction(status_result, duration)
        
        log_prediction(
            input_data=usvisa_data.get_usvisa_data_as_dict(),
            prediction=status_result,
        )

        return templates.TemplateResponse(
            "usvisa.html",
            {"request": request, "context": status_result},
        )

    except Exception as e:
        error_msg = f"Web prediction failed: {str(e)}"
        log_error_event(error_msg)
        MetricsCollector.record_error("web_prediction_error")
        
        return templates.TemplateResponse(
            "usvisa.html",
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
        "environment": settings.ENVIRONMENT,
        "version": settings.API_VERSION,
        "debug": settings.DEBUG,
        "timestamp": datetime.utcnow().isoformat(),
    }


if __name__ == "__main__":
    logger.info(
        f"Starting application on {settings.APP_HOST}:{settings.APP_PORT}"
    )
    app_run(app, host=settings.APP_HOST, port=settings.APP_PORT, reload=settings.DEBUG)