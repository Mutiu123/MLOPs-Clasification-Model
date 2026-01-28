# Quick Start Guide

## Get Started in 5 Minutes

### Option 1: Local Development (No Docker)

#### 1. Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

#### 2. Configure
```bash
cp .env.example .env
# Edit .env and add your MONGODB_URL
```

#### 3. Run Application
```bash
python app.py
```

#### 4. Access
- Web UI: http://localhost:8080
- API Docs: http://localhost:8080/api/docs
- ReDoc: http://localhost:8080/api/redoc
- Health: http://localhost:8080/health

---

### Option 2: Docker Development

#### 1. Setup
```bash
cp .env.example .env
# Edit .env with your configuration
```

#### 2. Run
```bash
docker-compose up -d
```

#### 3. Access
- App: http://localhost:8080
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin:admin)
- MongoDB: localhost:27017

#### 4. Stop
```bash
docker-compose down
```

---

## Common Tasks

### Run Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=us_visa

# Specific test
pytest tests/test_api.py -v
```

### Format Code
```bash
# Format with Black
black us_visa tests

# Sort imports
isort us_visa tests

# Lint with Flake8
flake8 us_visa
```

### Build Docker Image
```bash
docker build -t usvisa-app:latest .
```

### Deploy to Kubernetes
```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify
kubectl get pods -n usvisa-app
```

### View Logs
```bash
# Local file
tail -f logs/*.log

# Docker
docker logs -f <container-id>

# Kubernetes
kubectl logs -f -n usvisa-app -l app=usvisa-app
```

---

## 🔌 API Examples

### Health Check
```bash
curl http://localhost:8080/health
```

### Make Prediction (API)
```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "continent": "asia",
    "education_of_employee": "bachelor",
    "has_job_experience": true,
    "requires_job_training": false,
    "no_of_employees": 1000,
    "company_age": 15,
    "region_of_employment": "northeast",
    "prevailing_wage": 75000,
    "unit_of_wage": "yearly",
    "full_time_position": true
  }'
```

### Start Training
```bash
curl http://localhost:8080/train
```

### Get Metrics
```bash
curl http://localhost:8080/metrics
```

### API Status
```bash
curl http://localhost:8080/api/status
```

---

## Project Structure

```
├── app.py                    # FastAPI application
├── requirements.txt          # Dependencies
├── .env.example             # Environment template
├── Dockerfile               # Production image
├── docker-compose.yml       # Development stack
├── pytest.ini              # Test configuration
│
├── us_visa/                # Main package
│   ├── config.py           # Configuration
│   ├── schemas.py          # Validation models
│   ├── security.py         # Security
│   ├── middleware.py       # Middleware
│   ├── metrics.py          # Monitoring
│   ├── logging_config.py   # Logging
│   └── ...
│
├── tests/                  # Test suite
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_schemas.py
│   └── ...
│
├── k8s/                    # Kubernetes
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
│
├── README.md               # Full docs
├── CONTRIBUTING.md         # Guidelines
├── DEPLOYMENT.md          # Deployment
└── PRODUCTION_READY.md    # Checklist
```

---

## 🔑 Environment Variables

Essential variables (copy from `.env.example`):

```
# MongoDB
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net

# AWS (optional)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_DEFAULT_REGION=eu-west-2

# App
APP_HOST=0.0.0.0
APP_PORT=8080
ENVIRONMENT=development
DEBUG=True

# Security
SECRET_KEY=your-secret-key-change-me
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8080
lsof -i :8080

# Kill process
kill -9 <PID>
```

### MongoDB Connection Failed
```bash
# Test connection
python -c "import pymongo; pymongo.MongoClient('mongodb://...')"

# Check Docker
docker ps | grep mongo
```

### Tests Failing
```bash
# Run with verbose output
pytest tests/ -vv

# Run specific test
pytest tests/test_api.py::TestHealthEndpoint -vv
```

### Docker Issues
```bash
# Clean up containers
docker system prune -a

# Rebuild image
docker build --no-cache -t usvisa-app:latest .
```

---

## Documentation

- **Full Setup**: See [README.md](README.md)
- **Development**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Production**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Checklist**: See [PRODUCTION_READY.md](PRODUCTION_READY.md)
- **Summary**: See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

---

## What's New

- Security: JWT auth, rate limiting, input validation
- Monitoring: Prometheus, Grafana, structured logging
- Testing: 25+ test cases, 80%+ coverage
- Deployment: Docker, K8s, CI/CD ready
- Code Quality: Black, Flake8, MyPy, pre-commit
- Documentation: 4 comprehensive guides
- Database: Connection pooling
- API: OpenAPI documentation

---

## Production Deployment

### Step 1: Build Image
```bash
docker build -t your-registry/usvisa-app:v1.0.0 .
docker push your-registry/usvisa-app:v1.0.0
```

### Step 2: Deploy to K8s
```bash
# Update image in k8s/deployment.yaml
kubectl apply -f k8s/
```

### Step 3: Verify
```bash
kubectl get pods -n usvisa-app
curl http://localhost:8080/health
```

---

## Performance Tips

### Optimize Locally
1. Use requirements-prod.txt for minimal size
2. Enable caching in Docker
3. Use connection pooling (already configured)
4. Monitor metrics at `/metrics`

### Optimize in Production
1. Set resource limits in K8s
2. Enable auto-scaling (configured, min: 2, max: 10)
3. Use CDN for static files
4. Implement request caching

---

## Security Reminders

- [ ] Change SECRET_KEY before production
- [ ] Update CORS_ORIGINS to your domain
- [ ] Enable HTTPS/TLS certificates
- [ ] Use strong MongoDB password
- [ ] Rotate AWS credentials regularly
- [ ] Enable logging and monitoring
- [ ] Regular security audits

---

## Monitoring

### Local Development
```bash
# View metrics
curl http://localhost:8080/metrics

# Check health
curl http://localhost:8080/health

# View logs
tail -f logs/*.log
```

### Docker Compose
```bash
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
# MongoDB: mongosh mongodb://admin:admin@localhost:27017
```

---

## Getting Help

1. **Check Documentation**
   - README.md - Project overview
   - CONTRIBUTING.md - Development guide
   - DEPLOYMENT.md - Deployment steps

2. **Review Examples**
   - tests/ - Test cases with examples
   - docs/ - API documentation

3. **Check Logs**
   - logs/ - Application logs
   - docker logs - Docker container logs

4. **Test Locally**
   - Run tests: `pytest`
   - Use API docs: http://localhost:8080/api/docs

---

## 📞 Support

For questions or issues:
- Read the documentation files
- Check existing GitHub issues
- Create a GitHub discussion
- 📧 Contact: support@example.com

---

## You're Ready!

Your production-ready MLOps application is now set up and ready to deploy.

Next steps:
1. Setup local environment
2. Run tests to verify installation
3. Review documentation
4. Configure for your deployment
5. Deploy to production!

---

**Happy Coding!**
