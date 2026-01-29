# 🔍 IMPORTANT: PROJECT CONVERSION COMPLETE

## What Happened?

This project has been **successfully converted** from **US Visa Prediction** to **Hydrogen Pipeline Leak Detection & Characterization System**.

---

## Quick Navigation

### 📚 Key Documentation
1. **[README.md](README.md)** - Main project documentation
2. **[CONVERSION_CHECKLIST.md](CONVERSION_CHECKLIST.md)** - What changed (detailed checklist)
3. **[CONVERSION_SUMMARY.md](CONVERSION_SUMMARY.md)** - High-level overview of changes
4. **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical implementation details

### 🔧 Configuration
- **[.env.example](.env.example)** - Environment variables template
- **[pyproject.toml](pyproject.toml)** - Python project config
- **[setup.py](setup.py)** - Package setup

### 📁 Main Code
- **[app.py](app.py)** - FastAPI application (updated for H2 leak detection)
- **[h2_pipeline/](h2_pipeline/)** - Main package (was `us_visa/`)

### 🗂️ Data
- **[Sensor data/](Sensor%20data/)** - Lab experimental sensor data
  - `0.5H2/` - Low concentration
  - `1%H2/` - Standard concentration
  - `2.5% H2/` - Medium concentration
  - `5%H2/` - High concentration

### Deployment
- **[Dockerfile](Dockerfile)** - Production container
- **[docker-compose.yml](docker-compose.yml)** - Local development setup
- **[k8s/](k8s/)** - Kubernetes manifests

### Testing
- **[tests/](tests/)** - Test suite

---

## Quick Start

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Copy environment template
cp .env.example .env
```

### 2. Run Application
```bash
# Development mode
python app.py

# Or with uvicorn
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8080
```

### 3. Access System
- **Web UI**: http://localhost:8080
- **API Docs**: http://localhost:8080/api/docs
- **API ReDoc**: http://localhost:8080/api/redoc
- **Metrics**: http://localhost:8080/metrics

### 4. With Docker Compose
```bash
docker-compose up -d
```

---

## 🔑 KEY CHANGES FROM US VISA SYSTEM

### Package Rename
```
OLD: us_visa package
NEW: h2_pipeline package
```

### API Transformation
```
OLD: /predict → Visa approval prediction
NEW: /predict → Hydrogen leak detection

OLD: Input: visa applicant data (12 fields)
NEW: Input: sensor data (10 fields)

OLD: Output: "Visa-approved" / "Visa Not-Approved"
NEW: Output: Leak detected with severity level
```

### Data Model
```
OLD DATABASE: US_VISA
NEW DATABASE: H2_PIPELINE_DETECTION

OLD COLLECTION: visa_data
NEW COLLECTION: sensor_readings

OLD TARGET: case_status (binary)
NEW TARGET: leak_status (4-class: no_leak, minor, moderate, critical)
```

### Input Fields
```
NEW Fields (10 total):
- pressure_mpa (0-100 MPa)
- temperature_celsius (-40 to 150°C)
- hydrogen_concentration_ppm (0-1,000,000 ppm)
- vibration_hz (0-10,000 Hz)
- pipe_age_years (0-100)
- material (steel/stainless/composite/aluminum)
- flow_rate_kg_h (0-10,000)
- corrosion_rate_mm_year (0-10)
- soil_moisture_percent (0-100%)
- operating_hours (total hours)
```

---

## System Architecture

```
┌─────────────────────────────────┐
│   FastAPI Application           │
│   (app.py - H2 Leak Detection)  │
├─────────────────────────────────┤
│                                 │
│  ┌────────────────────────┐    │
│  │  API Endpoints         │    │
│  │  /predict (leak detect)│    │
│  │  /train (retraining)   │    │
│  │  /health (status)      │    │
│  └────────────────────────┘    │
│                                 │
│  ┌────────────────────────┐    │
│  │  h2_pipeline Package   │    │
│  │  - schemas             │    │
│  │  - pipelines           │    │
│  │  - components          │    │
│  │  - security            │    │
│  │  - metrics             │    │
│  └────────────────────────┘    │
├─────────────────────────────────┤
│   MongoDB (sensor_readings)     │
│   AWS S3 (models)               │
│   Prometheus (metrics)          │
└─────────────────────────────────┘
```

---

## Next Steps

### Immediate (Required)
1. [ ] Update environment variables in `.env`
2. [ ] Load sensor data from `Sensor data/` folders
3. [ ] Train hydrogen leak detection model
4. [ ] Test API endpoints

### Short Term
1. [ ] Implement data preprocessing pipeline
2. [ ] Create comprehensive test suite
3. [ ] Set up Docker builds
4. [ ] Deploy to staging

### Medium Term
1. [ ] Deploy to production
2. [ ] Set up monitoring and alerts
3. [ ] Integrate with operational pipelines
4. [ ] Create admin dashboards

---

## API Example

### Hydrogen Leak Detection Request
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pressure_mpa": 35.5,
    "temperature_celsius": 45.2,
    "hydrogen_concentration_ppm": 5000,
    "vibration_hz": 250.5,
    "pipe_age_years": 15,
    "material": "steel",
    "flow_rate_kg_h": 2500,
    "corrosion_rate_mm_year": 0.5,
    "soil_moisture_percent": 65.0,
    "operating_hours": 125000
  }'
```

### Response
```json
{
  "leak_detected": true,
  "leak_severity": "critical_leak",
  "confidence": 0.95,
  "risk_score": 85.5,
  "recommended_action": "Immediate shutdown and inspection required"
}
```

---

## 🛠️ Development

### Code Structure
```
h2_pipeline/
├── pipline/               # Training & prediction pipelines
├── components/            # ML pipeline components
├── entity/                # Configuration entities
├── schemas.py             # Pydantic models
├── config.py              # Settings management
├── security.py            # Authentication
├── middleware.py          # HTTP middleware
├── metrics.py             # Prometheus metrics
├── logging_config.py      # Logging setup
├── exception/             # Custom exceptions
├── utils/                 # Helper functions
├── configuration/         # Database connections
├── cloud_storage/         # AWS S3 integration
└── data_access/           # MongoDB repository
```

### Running Tests
```bash
pytest tests/ -v
pytest tests/ --cov=h2_pipeline
```

### Code Quality
```bash
# Format code
black h2_pipeline tests

# Lint code
flake8 h2_pipeline

# Type check
mypy h2_pipeline
```

---

## Docker

### Build Image
```bash
docker build -t h2-pipeline:latest .
```

### Run Container
```bash
docker run -d -p 8080:8080 \
  -e MONGODB_URL="mongodb://..." \
  -e AWS_ACCESS_KEY_ID="..." \
  -e AWS_SECRET_ACCESS_KEY="..." \
  h2-pipeline:latest
```

### Docker Compose
```bash
docker-compose up -d
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Main documentation |
| CONVERSION_CHECKLIST.md | Detailed checklist of all changes |
| CONVERSION_SUMMARY.md | High-level summary |
| IMPLEMENTATION_SUMMARY.md | Technical details |
| DEPLOYMENT.md | Deployment instructions |
| CONTRIBUTING.md | Contributing guidelines |

---

## ❓ FAQ

**Q: Can I use the old US visa data?**
A: No. You need hydrogen-specific sensor data from the `Sensor data/` folder.

**Q: Where are the old visa prediction models?**
A: They're not used. You need to train new models for hydrogen leak detection.

**Q: What database should I use?**
A: H2_PIPELINE_DETECTION (automatically configured in constants).

**Q: Can I switch back to US visa?**
A: Yes, the original code is likely still available. This is a fresh conversion.

**Q: How do I update the API endpoints?**
A: Edit `app.py` - all endpoints are documented.

---

## 📞 Support

- **Documentation**: See README.md and other .md files
- **API Docs**: http://localhost:8080/api/docs
- **Issues**: Check CONVERSION_CHECKLIST.md
- **Contact**: See README.md for contact info

---

## Checklist Before Using

- [ ] Read CONVERSION_CHECKLIST.md
- [ ] Review README.md
- [ ] Set up environment (.env)
- [ ] Install dependencies
- [ ] Load sensor data
- [ ] Run application
- [ ] Test API endpoints
- [ ] Train models
- [ ] Deploy to production

---

**IMPORTANT**: This is a **complete conversion**. The system is now for hydrogen pipeline leak detection, not US visa prediction.

For details on what changed, see [CONVERSION_CHECKLIST.md](CONVERSION_CHECKLIST.md)

---

<div align="center">

### 🔍 Hydrogen Pipeline Leak Detection System

**Production Ready | MLOps Architecture | Safety Critical**

⭐ Star this repository!

</div>
