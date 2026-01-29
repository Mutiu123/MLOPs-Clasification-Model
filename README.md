# US Visa Decision Prediction - Production Ready MLOps Model

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![Docker](https://img.shields.io/badge/Docker-Latest-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.24+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A **production-ready MLOps classification model** that predicts US visa approval decisions using machine learning with comprehensive security, monitoring, and deployment capabilities.

[Quick Start](#quick-start) • [Documentation](#documentation) • [API Reference](#api-reference) • [Contributing](CONTRIBUTING.md) • [Deployment](DEPLOYMENT.md)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Testing](#testing)
- [Monitoring](#monitoring)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Immigration and Nationality Act (INA) of the US permits foreign workers to come to the United States to work on either a temporary or permanent basis. The Office of Foreign Labor Certification (OFLC) administers these programs.

**Problem Statement:**
With thousands of visa applications annually, the OFLC needs an intelligent machine learning model to efficiently classify and recommend visa certification decisions based on historical data.

**Solution:**
This project implements a production-ready classification model that predicts visa approval status with:
- Security: JWT authentication, rate limiting, CORS configuration
- Monitoring: Prometheus metrics, structured logging, health checks
- Scalability: Kubernetes-ready, auto-scaling, connection pooling
- Quality: Comprehensive testing (80%+ coverage), code quality tools
- Documentation: API docs, deployment guides, contributing guidelines

**Dataset:**
- Source: [Office of Foreign Labor Certification (OFLC)](https://www.kaggle.com/datasets/moro23/easyvisa-dataset)
- Size: 25,480 rows × 12 columns
- Features: Applicant and employer information for visa classification

---

## Features

### Security
- JWT-based authentication
- Rate limiting (configurable)
- CORS with restrictive origins
- Input validation with Pydantic
- HTTPS/TLS support
- Non-root container execution

### Monitoring & Observability
- Prometheus metrics at `/metrics`
- Structured JSON logging
- Request/response tracking with IDs
- Performance metrics collection
- Health check endpoint
- Grafana dashboard integration

### Testing & Quality
- 80%+ code coverage
- Unit tests with pytest
- Integration tests for API
- Automated code formatting (Black)
- Linting (Flake8, Pylint)
- Type checking (MyPy)
- Pre-commit hooks

### Deployment
- Docker multi-stage builds
- Docker Compose for development
- Kubernetes manifests (Deployment, Service, HPA, NetworkPolicy)
- CI/CD with GitHub Actions
- Auto-scaling configuration
- Blue-green deployment ready

### Database
- MongoDB connection pooling
- Singleton pattern for connections
- Retry logic and timeouts
- SSL/TLS support

### API Features
- OpenAPI/Swagger documentation
- Response models with examples
- Error handling with details
- Request validation
- API versioning ready

---

## Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (optional)
- Git
- MongoDB instance (local or cloud)
- AWS account (optional, for S3 storage)

### Local Development Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/MLOPs-Clasification-Model.git
cd MLOPs-Clasification-Model
```

#### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements-dev.txt
```

#### 4. Setup Environment Variables

```bash
cp .env.example .env

# Edit .env with your configuration
# Required: MONGODB_URL, AWS credentials (optional)
```

#### 5. Run the Application

```bash
# Development mode
python app.py

# With hot reload
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8080
```

Access the application:
- Web UI: http://localhost:8080
- API Docs: http://localhost:8080/api/docs
- ReDoc: http://localhost:8080/api/redoc
- Metrics: http://localhost:8080/metrics

### Docker Setup

#### Quick Start with Docker Compose

```bash
# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app
```

Services:
- App: http://localhost:8080
- MongoDB: localhost:27017
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

#### Stop Services

```bash
docker-compose down
```

---

## Project Structure

```
MLOPs-Clasification-Model/
├── app.py                          # FastAPI application
├── requirements.txt                # Production dependencies
├── requirements-dev.txt            # Development dependencies
├── requirements-prod.txt           # Production-only dependencies
├── .env.example                    # Environment variables template
├── Dockerfile                      # Production Docker image
├── Dockerfile.dev                  # Development Docker image
├── docker-compose.yml              # Docker Compose configuration
├── prometheus.yml                  # Prometheus configuration
├── pytest.ini                      # Pytest configuration
├── pyproject.toml                  # Python project configuration
├── .pre-commit-config.yaml         # Pre-commit hooks
├── .flake8                         # Flake8 linting config
│
├── us_visa/                        # Main package
│   ├── __init__.py
│   ├── config.py                   # Configuration management
│   ├── schemas.py                  # Pydantic models
│   ├── security.py                 # Security & authentication
│   ├── middleware.py               # FastAPI middleware
│   ├── metrics.py                  # Prometheus metrics
│   ├── logging_config.py           # Logging setup
│   │
│   ├── components/                 # ML pipeline components
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluation.py
│   │   └── model_pusher.py
│   │
│   ├── entity/                     # Data entities
│   │   ├── config_entity.py
│   │   ├── artifact_entity.py
│   │   ├── estimator.py
│   │   └── S3_estimator.py
│   │
│   ├── exception/                  # Custom exceptions
│   ├── logger/                     # Logging setup
│   ├── utils/                      # Utility functions
│   ├── pipline/                    # Training & prediction pipelines
│   └── configuration/              # Database & AWS configuration
│
├── tests/                          # Test suite
│   ├── conftest.py                 # Pytest fixtures
│   ├── test_utils.py               # Utils tests
│   ├── test_exception.py           # Exception tests
│   ├── test_schemas.py             # Pydantic models tests
│   └── test_api.py                 # API endpoint tests
│
├── k8s/                            # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
│
├── templates/                      # HTML templates
├── static/                         # Static files (CSS, JS)
├── config/                         # Configuration files (YAML)
├── notebook/                       # Jupyter notebooks
│
├── DEPLOYMENT.md                   # Deployment guide
├── CONTRIBUTING.md                 # Contributing guidelines
├── README.md                        # This file
└── LICENSE                         # MIT License
```

---

## API Documentation

### Base URL
```
http://localhost:8080
```

### Authentication
Some endpoints require JWT authentication. Get a token first:

```bash
curl -X POST http://localhost:8080/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### Endpoints

#### 1. Health Check
**GET** `/health`

```bash
curl http://localhost:8080/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-28T10:00:00"
}
```

#### 2. Predict (API)
**POST** `/predict`

Request:
```json
{
  "continent": "asia",
  "education_of_employee": "bachelor",
  "has_job_experience": true,
  "requires_job_training": false,
  "no_of_employees": 1000,
  "company_age": 15,
  "region_of_employment": "northeast",
  "prevailing_wage": 75000.00,
  "unit_of_wage": "yearly",
  "full_time_position": true
}
```

Response:
```json
{
  "prediction": "Visa-approved",
  "confidence": 0.95,
  "status": "success"
}
```

#### 3. Predict (Web Form)
**POST** `/`

HTML form submission at root endpoint

#### 4. Train Model
**GET** `/train`

Triggers the model training pipeline

Response:
```json
{
  "status": "success",
  "message": "Model training completed successfully",
  "artifacts_location": "artifact/"
}
```

#### 5. Metrics
**GET** `/metrics`

Prometheus metrics for monitoring

#### 6. API Status
**GET** `/api/status`

Get API configuration and status

---

## Configuration

### Environment Variables

See `.env.example` for all available options:

```bash
# MongoDB
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net

# AWS
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_DEFAULT_REGION=eu-west-2

# Application
APP_HOST=0.0.0.0
APP_PORT=8080
ENVIRONMENT=production
DEBUG=False

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

---

## Testing

### Run Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_schemas.py -v

# With coverage
pytest --cov=us_visa --cov-report=html

# Specific test
pytest tests/test_api.py::TestHealthEndpoint::test_health_check_success -v
```

### Test Structure

```
tests/
├── conftest.py                  # Shared fixtures
├── test_utils.py                # Utility functions tests
├── test_exception.py            # Exception handling tests
├── test_schemas.py              # Validation models tests
└── test_api.py                  # API integration tests
```

### Coverage Report

```bash
pytest --cov=us_visa --cov-report=html
open htmlcov/index.html
```

---

## Monitoring

### Prometheus Metrics

Available at: `http://localhost:8080/metrics`

Key metrics:
- `visa_predictions_total` - Total predictions by result
- `visa_prediction_latency_seconds` - Prediction latency histogram
- `model_training_total` - Total training runs
- `errors_total` - Total errors by type
- `active_requests` - Current active requests
- `model_accuracy` - Current model accuracy
- `data_drift_value` - Data drift detection

### Grafana Dashboard

1. Access Grafana: http://localhost:3000
2. Login with `admin:admin`
3. Add Prometheus data source: http://prometheus:9090
4. Import dashboard (ID: 1860 for Prometheus)

### Health Checks

```bash
# Application health
curl http://localhost:8080/health

# Database connectivity
curl http://localhost:8080/api/status
```

### Logs

Structured logs are saved to:
- `logs/*.log` - Plain text format (readable)
- `logs/*.json` - JSON format (structured)

View logs:
```bash
tail -f logs/2024-01-28_10-30-45.log
```

---

## Deployment

### Local Docker Deployment

```bash
# Build image
docker build -t usvisa-app:latest .

# Run container
docker run -d -p 8080:8080 \
  -e MONGODB_URL="mongodb://..." \
  -e AWS_ACCESS_KEY_ID="..." \
  --name usvisa-app \
  usvisa-app:latest
```

### Kubernetes Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get deployment -n usvisa-app
kubectl get pods -n usvisa-app
```

### AWS EC2 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### CI/CD with GitHub Actions

The project includes automated workflows:
- Build and push Docker image
- Run tests
- Deploy to AWS ECR/EC2

---

## Code Quality

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pre-commit install

# Run manually
pre-commit run --all-files
```

Automatically runs:
- Black (formatting)
- isort (imports)
- Flake8 (linting)
- MyPy (type checking)

### Code Style

```bash
# Format code
black us_visa tests

# Sort imports
isort us_visa tests

# Lint code
flake8 us_visa

# Type check
mypy us_visa
```

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit changes (`git commit -am 'Add my feature'`)
4. Push to branch (`git push origin feature/my-feature`)
5. Create a Pull Request

---

## Troubleshooting

### Application won't start

```bash
# Check if port is in use
lsof -i :8080

# Kill process using port
kill -9 <PID>

# Check environment variables
env | grep MONGODB_URL
```

### Database connection failed

```bash
# Test MongoDB connection
python -c "import pymongo; pymongo.MongoClient('mongodb://...')"

# Check MongoDB is running
docker ps | grep mongo
```

### Tests failing

```bash
# Run specific test with verbose output
pytest tests/test_api.py -vv

# Run with debugging
pytest tests/test_api.py -vv --pdb
```

---

## Performance Tuning

### Database
- Connection pool size: 50 max, 10 min
- Connection timeout: 10s
- Idle timeout: 45s

### API
- Request timeout: 30s
- Rate limit: 100 requests/60s
- Default page size: 100 items

### Kubernetes
- Min replicas: 2
- Max replicas: 10
- CPU limit: 500m
- Memory limit: 512Mi

---

## References

- [Dataset](https://www.kaggle.com/datasets/moro23/easyvisa-dataset)
- [OFLC Website](https://www.dol.gov/agencies/eta/foreign-labor/certification)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Data source: [Office of Foreign Labor Certification](https://www.oflc.gov/)
- ML frameworks: scikit-learn, CatBoost, XGBoost
- Web framework: FastAPI
- Infrastructure: Docker, Kubernetes

---

## Contact & Support

For questions and support:
- 📧 Email: support@example.com
- Issues: [GitHub Issues](https://github.com/yourusername/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/discussions)

---

<div align="center">

Made with dedication for production excellence

Star us on GitHub!

</div>

```bash 
conda activate visa-decision-model
```

```bash 
pip install -r requirements.txt
```


```bash
create S3 bucket to store the latest version of the trained model


```

```bash
export MONGODB_URL="mongodb+srv://<username>:<password>...."



export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>


```



## Workflow:

1. constants
2. entity
3. components
4. pipeline
5. Main file




# AWS-CICD-Deployment-with-Github-Actions

## 1. Login to AWS console.

## 2. Create IAM user for deployment

	#with specific access

	1. EC2 access : It is virtual machine

	2. ECR: Elastic Container registry to save your docker image in aws


	#Description: About the deployment

	1. Build docker image of the source code

	2. Push your docker image to ECR

	3. Launch Your EC2 

	4. Pull Your image from ECR in EC2

	5. Lauch your docker image in EC2

	#Policy:

	1. AmazonEC2ContainerRegistryFullAccess

	2. AmazonEC2FullAccess

	
## 3. Create ECR repo to store/save docker image
    - Save the URL: 024848444109.dkr.ecr.eu-west-2.amazonaws.com/visarepo

	
## 4. Create EC2 machine (Ubuntu) 

## 5. Open EC2 and Install docker in EC2 Machine:
	
	
	#optinal

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker
	
# 6. Configure EC2 as self-hosted runner:
    setting>actions>runner>new self hosted runner> choose os> then run command one by one


# 7. Setup github secrets:

   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
   - ECR_REPO
   - MONGODB_URL

    



