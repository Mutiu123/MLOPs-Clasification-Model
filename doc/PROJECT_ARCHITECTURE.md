# Project Architecture: H2 Pipeline Leak Detection System

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES (INGESTION LAYER)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────────┐       │
│  │   Laboratory    │  │  Operational     │  │   Environmental      │       │
│  │   Experiments   │  │  Sensors         │  │   Datasets           │       │
│  │                 │  │  (Real-time)     │  │                      │       │
│  │ • 0.5% H2       │  │ • Pressure       │  │ • Temperature        │       │
│  │ • 1% H2         │  │ • Temperature    │  │ • Pressure           │       │
│  │ • 2.5% H2       │  │ • H2 Conc.       │  │ • Soil Moisture      │       │
│  │ • 5% H2         │  │ • Vibration      │  │ • Corrosion Rates    │       │
│  │                 │  │ • Flow Rate      │  │ • Pipe Conditions    │       │
│  └────────┬────────┘  └────────┬─────────┘  └──────────┬───────────┘       │
│           │                    │                       │                    │
└───────────┼────────────────────┼───────────────────────┼────────────────────┘
            │                    │                       │
            └────────────────────┼───────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MONGODB (PERSISTENT STORAGE)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Database: H2_PIPELINE_DETECTION                                            │
│  ┌──────────────────────────┐  ┌──────────────────────┐                     │
│  │  sensor_readings         │  │  model_artifacts     │                     │
│  │  (Time-series data)      │  │  (Model metadata)    │                     │
│  │                          │  │                      │                     │
│  │ • timestamp              │  │ • model_id           │                     │
│  │ • sensor readings (10)   │  │ • version            │                     │
│  │ • ground truth labels    │  │ • metrics            │                     │
│  │ • metadata               │  │ • s3_path            │                     │
│  └──────────────────────────┘  └──────────────────────┘                     │
│                                                                               │
└────┬─────────────────────────────────────────────────────────┬──────────────┘
     │                                                          │
     ▼                                                          ▼
┌──────────────────────────────────┐          ┌──────────────────────────────┐
│   DATA PROCESSING LAYER          │          │   MODEL MANAGEMENT LAYER     │
├──────────────────────────────────┤          ├──────────────────────────────┤
│                                  │          │                              │
│ ┌────────────────────────────┐   │          │ ┌─────────────────────────┐ │
│ │  Data Validation           │   │          │ │  Model Trainer          │ │
│ │  • Schema validation       │   │          │ │  • Algorithm selection  │ │
│ │  • Drift detection         │   │          │ │  • Cross-validation     │ │
│ │  • Anomaly detection       │   │          │ │  • Hyperparameter tune  │ │
│ └────────────────────────────┘   │          │ └─────────────────────────┘ │
│                 ▼                 │          │           ▼                 │
│ ┌────────────────────────────┐   │          │ ┌─────────────────────────┐ │
│ │  Feature Engineering       │   │          │ │  Model Evaluator        │ │
│ │  • Normalization           │   │          │ │  • Cross-val metrics    │ │
│ │  • Feature scaling         │   │          │ │  • Threshold tuning     │ │
│ │  • Composite indices       │   │          │ │  • Performance reports  │ │
│ └────────────────────────────┘   │          │ └─────────────────────────┘ │
│                 ▼                 │          │           ▼                 │
│ ┌────────────────────────────┐   │          │ ┌─────────────────────────┐ │
│ │  Processed Data Ready      │   │          │ │  AWS S3 (Model Storage) │ │
│ │  for Prediction/Training   │   │          │ │  • model.pkl            │ │
│ └────────────────────────────┘   │          │ │  • metadata.json        │ │
│                                  │          │ │  • artifacts/           │ │
│                                  │          │ └─────────────────────────┘ │
└──────────────────────────────────┘          └──────────────────────────────┘
             ▲                                          ▲
             │                                          │
             └──────────────────┬───────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       API & PREDICTION LAYER (FASTAPI)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌────────────────────────────────┐    ┌──────────────────────────────┐    │
│  │  REST Endpoints                │    │  Web Interface               │    │
│  │                                │    │                              │    │
│  │ • POST /predict                │    │ • HTML form (h2_pipeline.html)│   │
│  │   - JSON sensor data input     │    │ • 10 sensor fields           │    │
│  │   - Real-time leak detection   │    │ • Instant visualization      │    │
│  │                                │    │ • Risk scoring               │    │
│  │ • POST /train                  │    │ • Recommended actions        │    │
│  │   - Trigger model training     │    │                              │    │
│  │   - Return training metrics    │    │                              │    │
│  │                                │    │                              │    │
│  │ • GET /health                  │    │                              │    │
│  │   - System status              │    │                              │    │
│  │                                │    │                              │    │
│  │ • GET /metrics                 │    │                              │    │
│  │   - Prometheus metrics export  │    │                              │    │
│  │                                │    │                              │    │
│  └────────────────────────────────┘    └──────────────────────────────┘    │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
             ▲                                          ▲
             │                                          │
             └──────────────────┬───────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY & SECURITY LAYER                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌─────────────────┐  │
│  │  Prometheus Metrics  │  │  Structured Logging  │  │  Security       │  │
│  │                      │  │                      │  │                 │  │
│  │ • Prediction count   │  │ • JSON logs to file  │  │ • JWT auth      │  │
│  │ • Confidence scores  │  │ • Request tracking   │  │ • Rate limiting │  │
│  │ • Latency tracking   │  │ • Error logging      │  │ • CORS support  │  │
│  │ • Model metrics      │  │ • Audit trails       │  │ • Env variables │  │
│  │                      │  │                      │  │                 │  │
│  └──────────────────────┘  └──────────────────────┘  └─────────────────┘  │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
             ▲                                          ▲
             │                                          │
             └──────────────────┬───────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT & ORCHESTRATION                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────┐  ┌────────────────┐    │
│  │   Docker     │  │ Kubernetes  │  │  Compose   │  │  Development   │    │
│  │              │  │             │  │            │  │                │    │
│  │ • Container  │  │ • Service   │  │ • Multi-   │  │ • Local setup  │    │
│  │ • Image      │  │ • Pod       │  │   container│  │ • Hot reload   │    │
│  │ • Registry   │  │ • Ingress   │  │ • Network  │  │ • Testing env  │    │
│  │              │  │ • YAML      │  │            │  │                │    │
│  └──────────────┘  └─────────────┘  └────────────┘  └────────────────┘    │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Data Ingestion Layer
I designed this layer to handle three distinct data sources, each with different characteristics:

- **Laboratory Data**: Historical experiments with controlled H2 concentrations (0.5%, 1%, 2.5%, 5%) providing ground truth for model training
- **Operational Sensors**: Real-time pipeline sensor readings including pressure, temperature, vibration, and flow measurements
- **Environmental Data**: External factors affecting leak detection like soil conditions, ambient temperature, and pipe corrosion rates

### 2. Data Storage (MongoDB)
I chose MongoDB for its flexibility with time-series data and horizontal scalability. The database stores:
- `sensor_readings`: Raw and processed sensor data with timestamps
- `model_artifacts`: Metadata about trained models, versions, and S3 locations

### 3. Data Processing Pipeline
I implemented a modular processing pipeline with four distinct stages:

- **Validation**: Checks schema compliance, detects data drift, and identifies anomalies
- **Feature Engineering**: Normalizes sensor values, scales features, and creates composite indices (e.g., risk scores)
- **Training**: Implements multiple algorithms (scikit-learn, CatBoost, XGBoost) with cross-validation
- **Evaluation**: Computes metrics, tunes confidence thresholds, and generates performance reports

### 4. API & Prediction Layer
I built the API using FastAPI for its async capabilities and automatic OpenAPI documentation. The layer provides:
- REST endpoints for predictions and training
- Web interface for manual testing
- Health checks and metrics exports

### 5. Observability & Security
I added production-grade observability:
- **Prometheus Metrics**: Track prediction counts, confidence scores, and latency
- **Structured Logging**: JSON logs for efficient aggregation and analysis
- **Security**: JWT authentication, rate limiting, and secure credential management

### 6. Deployment Options
I included three deployment strategies:
- **Docker**: For local development and single-node deployment
- **Docker Compose**: For multi-container local development
- **Kubernetes**: For production-grade scaling and reliability

---

## Data Flow Example: Hydrogen Leak Prediction

```
1. Sensor Reading Arrives
   └─> FastAPI /predict endpoint receives JSON

2. Input Validation
   └─> Pydantic validates 10 sensor fields against schema

3. Feature Engineering
   └─> Normalize pressure, temperature, H2 concentration
   └─> Scale vibration and flow measurements
   └─> Compute composite risk indices

4. Model Prediction
   └─> Load trained model from S3
   └─> Feed engineered features to model
   └─> Get 4-class probability distribution

5. Output Generation
   └─> Select leak severity class (no_leak, minor, moderate, critical)
   └─> Calculate confidence and risk score
   └─> Generate recommended action

6. Response & Logging
   └─> Return JSON response to client
   └─> Log prediction to database
   └─> Update Prometheus metrics
   └─> Write structured JSON log
```

## Key Design Decisions

1. **Modular Architecture**: Each component (data_ingestion, validation, transformation, etc.) is independent and testable
2. **Multi-Algorithm Support**: Train multiple models and select the best performer for deployment
3. **Real-time Capability**: Sub-100ms prediction latency for production systems
4. **Cloud-Native Design**: Built for AWS S3 and Kubernetes from inception
5. **Comprehensive Observability**: Prometheus metrics and structured logging for production debugging
6. **Security-First**: JWT authentication, rate limiting, and environment-based credential management

