# Architecture Details & Design Justifications

## Introduction

In this document, I walk through the design decisions behind the Hydrogen Pipeline Leak Detection system, explaining the reasoning behind each architectural choice and why specific technologies were selected.

---

## 1. Data Ingestion Strategy

### Challenge
I needed to handle three fundamentally different data sources with varying characteristics:
- **Lab Data**: Batch historical experiments with ground truth
- **Operational Data**: Real-time streaming sensor readings
- **Environmental Data**: External factors affecting predictions

### My Approach
I designed a unified ingestion layer that normalizes all three sources into MongoDB documents with consistent schemas. Here's why:

**MongoDB Over Relational Databases:**
- Lab experiments have structured, consistent fields
- Operational sensors may have variable timestamps and occasional missing fields
- MongoDB's flexible schema allows handling both structured and semi-structured data without migrations
- Native time-series support with TTL indexes for automatic old data cleanup

**Separate Collections:**
- `sensor_readings`: All sensor data (lab + operational + environmental)
- `model_artifacts`: Model metadata and training history
This separation allows querying predictions independently from training data.

### Implementation Details

```python
# Lab data structure (batch upload)
{
  "timestamp": "2025-01-15T10:30:00Z",
  "source": "laboratory",
  "experiment_id": "EXP_0.5H2_001",
  "h2_concentration": 0.5,  # Lab experiments test specific H2 levels
  "pressure_mpa": 45.2,
  "temperature_celsius": 25.0,
  # ... other sensors
  "ground_truth": "no_leak"  # Known from controlled lab setup
}

# Operational data structure (real-time)
{
  "timestamp": "2025-01-28T14:35:22Z",
  "source": "operational_sensor_01",
  "pipeline_id": "PIPELINE_NORTH_001",
  "pressure_mpa": 48.5,
  # ... other sensors (same fields as lab)
  "metadata": {
    "sensor_health": "good",
    "last_maintenance": "2024-12-01"
  }
}
```

I chose this approach because:
1. Lab data provides ground truth for supervised learning
2. Operational data enables real-time monitoring and drift detection
3. Environmental data helps contextualize predictions
4. Single schema makes feature engineering easier

---

## 2. Feature Engineering Philosophy

### Challenge
Raw sensor readings have different units, scales, and distributions. I needed to transform them into features that:
- Are comparable across sensors
- Capture domain-specific relationships
- Improve model performance

### My Approach

**Normalization for Scale Invariance:**
```
Normalized value = (raw - mean) / std_dev
```
This centers each sensor around 0 and scales to unit variance. Why?
- Models like logistic regression and neural networks perform better with normalized inputs
- Prevents high-magnitude features from dominating
- Makes model weights interpretable

**Categorical Encoding:**
```
Material "steel" → [1, 0, 0, 0] (one-hot encoding)
```
Why one-hot instead of ordinal (steel=1, aluminum=2)?
- Material type is not ordinal—steel isn't "more" than aluminum
- One-hot prevents the model from learning false ordinal relationships

**Domain-Specific Feature Engineering:**

I created composite features based on physics and domain knowledge:

1. **Risk Index** = (H2_concentration × Pressure × Corrosion) / Pipe_Age
   - Justification: Leak risk increases with H2 (fuel concentration), pressure (force), and corrosion, but decreases with newer pipes (better integrity)
   - Units: Simplified to dimensionless risk metric

2. **Temperature-Pressure Interaction** = Normalized_Temp × Normalized_Pressure
   - Justification: High temperature + high pressure → compound stress on pipe material
   - Models often miss such interactions without explicit features

3. **Vibration-Flow Interaction** = Normalized_Vibration × Normalized_Flow
   - Justification: Unusual vibration at normal flow rates might indicate loose connection; same vibration at high flow is more concerning
   - Helps distinguish coincidental vibration from structural issues

### Why This Approach?
- Domain features often beat raw features because they encode expert knowledge
- Saves the model from learning these relationships from limited data
- Results are more interpretable for domain experts

---

## 3. Model Selection Strategy

### Challenge
Different algorithms have different strengths. How do I choose which to use?

### My Approach: Multi-Algorithm Training

I train three algorithms and compare:

**1. Random Forest (scikit-learn)**
- Pros: Fast training, parallelizable, handles missing data, feature importance
- Cons: Can overfit, less interpretable
- When it wins: Balanced accuracy-speed tradeoff

**2. CatBoost**
- Pros: Excellent with categorical variables, handles imbalanced data
- Cons: Slower training, requires tuning
- When it wins: High categorical features (like material type)

**3. XGBoost**
- Pros: State-of-the-art performance, regularization built-in
- Cons: Slower, more hyperparameters to tune
- When it wins: Maximum accuracy required

### Training Strategy
```
For each algorithm:
  1. Train with 5-fold cross-validation
  2. Record mean CV score and std
  3. Save all three models

Compare:
  1. Select model with highest F1-score
  2. If tie, prefer higher precision (avoid false alarms)
  3. Document why selected model won
```

Why not just use the "best" algorithm?
- Different datasets favor different algorithms
- Cross-validation prevents lucky results
- Comparing multiple models catches overfitting

### Hyperparameter Selection
I chose conservative defaults:
```
RandomForest(n_estimators=100)   # Standard for gradient boosting
CatBoost(iterations=100)          # Balanced for quick experiments
XGBoost(n_estimators=100)         # Common baseline
```

Why not automated tuning (GridSearch)?
- Hyperparameter tuning risks overfitting to training data
- Conservative defaults generalize better
- I tune thresholds instead (cheaper, more important)

---

## 4. Data Validation & Drift Detection

### Challenge
Real-world data changes over time (data drift). My model was trained on 2024 sensor readings, but 2026 sensors might behave differently due to:
- Calibration changes
- New sensor models
- Changed operating conditions
- System degradation

How do I detect when my model becomes unreliable?

### My Approach: Statistical Drift Detection

**For Each Numeric Feature:**
```python
# 1. Compute statistics on training data
train_mean = 45.2    # pressure mean
train_std = 5.3

# 2. On new data, run Kolmogorov-Smirnov test
ks_statistic = ks_test(new_data, train_data)

# 3. If ks_statistic > threshold (0.05), declare drift
if ks_statistic > 0.05:
    alert("Significant drift detected in pressure sensor")
```

**For Categorical Features:**
```python
# Compare class distributions with chi-square test
chi2, p_value = chi2_contingency(observed, expected)
if p_value < 0.05:
    alert("Material distribution changed significantly")
```

### Why KS Test + Chi-Square?
- KS test is model-agnostic (works on any distribution)
- Chi-square works for categorical variables
- Both detect shifts in distributions, not just mean/variance
- Threshold 0.05 = 95% confidence drift is real (not random noise)

### Action on Drift Detection
1. Stop training immediately
2. Alert data team to investigate
3. Log detailed statistics
4. Require manual review before proceeding

---

## 5. API Design Decisions

### Challenge
I need an API that is:
- Fast (< 50ms predictions)
- Reliable (correct predictions)
- Secure (no unauthorized access)
- Observable (track all requests)

### My Approach: FastAPI

**Why FastAPI?**
- **Async**: Handles many concurrent requests without threading overhead
- **Type hints**: Automatic validation via Pydantic (catches bad inputs early)
- **OpenAPI**: Automatic documentation at `/docs`
- **Performance**: One of the fastest Python frameworks

### Request Validation with Pydantic
```python
class H2SensorDataRequest(BaseModel):
    pressure_mpa: float = Field(ge=0, le=100)
    hydrogen_concentration_ppm: float = Field(ge=0, le=1000000)
    # ... other fields with range validation
```

Why validate inputs?
- Bad data → bad predictions
- Early validation prevents downstream errors
- Type hints prevent runtime crashes
- Automatic error messages help API users

### Prediction Response Design
```python
{
    "leak_detected": boolean,        # Human understands immediately
    "leak_severity": string,         # Actionable category
    "confidence": float,             # Model uncertainty
    "risk_score": 0-100,            # Familiar scale for decision-making
    "recommended_action": string     # Next step for operator
}
```

Why this response design?
- `leak_detected` answers the primary question immediately
- `confidence` lets operators gauge reliability
- `risk_score` provides continuous ranking (better than binary)
- `recommended_action` makes it actionable for non-technical users

---

## 6. Logging & Monitoring Strategy

### Challenge
In production, things fail silently. How do I:
- Debug issues after they happen?
- Detect anomalies in real-time?
- Audit all predictions?

### My Approach: Multi-Level Observability

**1. Structured JSON Logging**
```json
{
  "timestamp": "2026-01-28T14:35:22.123Z",
  "event": "prediction_made",
  "input": { /* sensor values */ },
  "output": { /* prediction */ },
  "execution_time_ms": 42,
  "model_version": "v1.2.3"
}
```

Why JSON?
- Parseable (unlike text logs)
- Searchable (index in ELK stack or similar)
- Complete (captures context for debugging)
- Timestamp for correlation

**2. Prometheus Metrics**
```python
# Increment prediction counter
h2_pipeline_predictions_total.labels(severity="critical").inc()

# Record confidence score
h2_pipeline_leak_confidence.set(0.92)

# Track latency
h2_pipeline_prediction_latency_ms.observe(42)
```

Why Prometheus?
- Time-series metrics for trending
- Alerting (e.g., "if > 1000 predictions/minute, page on-call")
- Dashboards (Grafana) for visual monitoring
- Standard in production environments

**3. MongoDB Audit Trail**
```python
# Save every prediction
db.predictions.insert_one({
    "timestamp": "2026-01-28T14:35:22Z",
    "sensor_values": { /* 10 sensors */ },
    "prediction": "no_leak",
    "model_version": "v1.2.3",
    "user_id": "sensor_01"
})
```

Why MongoDB?
- Queryable history (find all critical predictions from last week)
- Time-series TTL indexes (auto-cleanup old records)
- Flexible schema (can add fields without migration)

---

## 7. Security Implementation

### Challenge
The system makes life-critical decisions. I need:
- Authentication (only authorized systems make requests)
- Authorization (different users see different data)
- Secrets management (API keys, credentials safe)
- Rate limiting (prevent abuse/DOS)

### My Approach

**JWT Authentication**
```python
# Server creates token
token = create_access_token(data={"sub": "sensor_01"})

# Client sends token in request
headers = {"Authorization": f"Bearer {token}"}

# Server verifies token before processing
if not verify_token(token):
    raise HTTPException(status_code=401)
```

Why JWT?
- Stateless (server doesn't maintain session list)
- Scalable (works with multiple server instances)
- Standard (compatible with other services)
- Revocable (token expires, forcing re-authentication)

**Credentials Management**
```python
# Load from environment, not code
SECRET_KEY = os.getenv("SECRET_KEY")
DB_PASSWORD = os.getenv("MONGO_PASSWORD")
```

Why environment variables?
- Secrets never committed to git
- Different values per environment (dev/prod)
- Compatible with container orchestration (Kubernetes secrets)

**Rate Limiting**
```python
# Max 100 requests per minute per IP
@limiter.limit("100/minute")
def predict(request, data):
    ...
```

Why rate limiting?
- Prevents accidental DOS
- Protects against brute force (if using API for something)
- Fair resource sharing across users

---

## 8. Deployment Strategy

### Challenge
I need to:
- Develop locally
- Test thoroughly
- Deploy to production
- Scale under load

### My Approach: Docker + Kubernetes

**Docker (Containerization)**
```dockerfile
FROM python:3.10
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

Why Docker?
- "Works on my machine" → "works everywhere"
- Consistent environment (dev = prod)
- Isolation (multiple versions simultaneously)

**Kubernetes (Orchestration)**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: h2-leak-detection
spec:
  selector:
    app: h2-pipeline
  ports:
    - port: 80
      targetPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: h2-leak-detection
spec:
  replicas: 3  # Three instances for availability
  template:
    spec:
      containers:
        - name: app
          image: my-registry/h2-pipeline:v1.2.3
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
```

Why Kubernetes?
- **Replication**: Automatic restart if pod crashes
- **Load balancing**: Distribute requests across instances
- **Scaling**: Add/remove instances based on load
- **Health checks**: Detect and restart unhealthy pods
- **Rolling updates**: New version → 0 downtime deployment

### Three-Tier Deployment
1. **Development** (Docker Compose local)
   - Fast iteration
   - All services running

2. **Staging** (Kubernetes, same as prod)
   - Full integration testing
   - Performance testing
   - Data-driven testing

3. **Production** (Kubernetes)
   - High availability (3+ replicas)
   - Auto-scaling
   - Monitoring & alerting

---

## 9. Database Design

### Challenge
I need to store:
- Time-series sensor data (millions of readings)
- Model artifacts and versions
- Prediction history

Requirements:
- Fast queries ("get all readings from last hour")
- Efficient storage ("don't store everything forever")
- Flexible schema ("new sensors shouldn't require migration")

### My Approach: MongoDB + Indexes

**Collection: sensor_readings**
```json
{
  "_id": ObjectId,
  "timestamp": ISODate("2026-01-28T14:35:22Z"),
  "source": "operational_sensor_01",
  "pipeline_id": "PIPELINE_NORTH_001",
  "pressure_mpa": 45.2,
  // ... 9 more sensor fields
  "metadata": {
    "sensor_health": "good",
    "calibrated_date": ISODate("2025-12-01")
  }
}
```

**Indexes for Performance**
```python
# Time-series queries (most common)
db.sensor_readings.create_index([("timestamp", -1)])

# Pipeline-specific queries
db.sensor_readings.create_index([("pipeline_id", 1), ("timestamp", -1)])

# TTL index (auto-delete old data after 2 years)
db.sensor_readings.create_index([("timestamp", 1)], expireAfterSeconds=63072000)
```

Why these indexes?
- Timestamp index: O(log n) query by time instead of O(n) full scan
- Compound index: Fast queries filtering by pipeline AND time
- TTL index: Automatic cleanup prevents database bloat

### Why MongoDB Over PostgreSQL?

| Feature | MongoDB | PostgreSQL |
|---------|---------|-----------|
| Flexible schema | Yes | No (requires migration) |
| Time-series support | Native | Via extension |
| Horizontal scaling | Easy (sharding) | Complex |
| Document structure | Natural | Requires normalization |

For time-series sensor data, MongoDB is better.

---

## 10. Training Data Strategy

### Challenge
How much data do I need? What quality?

### My Approach

**Data Collection**
- Lab experiments: 500-1000 samples (controlled conditions)
- Operational data: 10,000+ samples (real-world variability)
- Environmental data: Time-aligned with sensors

**Data Quality**
- Missing values: Drop rows with > 2 missing sensors
- Outliers: Keep (represent real anomalies)
- Imbalance: Use stratified train-test split, class weights in model

**Training Set Size Decision**
- Started with 80-20 train-test split (standard)
- Used 5-fold cross-validation (reduces overfitting risk)
- Increased training data until CV score plateaued

Why 5-fold CV?
- Tests model on 5 different train-test combinations
- Gives mean accuracy ± std (confidence interval)
- Uses 80% of data for training (good learning)

---

## 11. Error Handling & Graceful Degradation

### Challenge
What happens when:
- S3 is unreachable (model can't load)?
- Database is down (can't save predictions)?
- Input validation fails?

### My Approach: Layered Error Handling

**Input Validation**
```python
try:
    data = H2SensorDataRequest(**request_json)
except ValidationError as e:
    return {"error": "Invalid input", "details": e.errors()}, 422
```

**Model Loading**
```python
try:
    model = load_model_from_s3()
except Exception as e:
    logger.error(f"Model load failed: {e}")
    model = load_fallback_model()  # Keep latest in memory
```

**Database Failures**
```python
try:
    db.predictions.insert_one(prediction)
except Exception as e:
    logger.error(f"DB insert failed: {e}")
    # Still return prediction (data loss better than service loss)
```

Why graceful degradation?
- System continues working even if non-critical components fail
- Users get predictions even if logging is down
- Better to miss audit trail than block operator action

---

## 12. Cost Optimization

### Challenge
Hydrogen leak detection must be cost-effective to deploy widely.

### My Optimizations

**Model Inference Speed**
- Threshold of 100ms inference latency (vs 5 second batch processing)
- Faster = fewer compute instances needed
- Faster = better user experience

**Database Optimization**
- TTL indexes auto-delete data > 2 years
- Compression in MongoDB (default)
- Sharding ready (for future when data grows)

**Cloud Storage**
- Store only production models (not intermediate training artifacts)
- Versioning (keep 3 recent versions, delete older)
- Compress models (pickle + gzip reduces size ~60%)

**API Scaling**
- Horizontal scaling: Add more pods, not bigger machines
- Stateless design: Any pod can handle any request
- Cache model in memory (avoid S3 hit per request)

---

## Summary of Architectural Principles

| Principle | How I Applied It |
|-----------|------------------|
| **Modularity** | Separate components (ingestion, validation, transformation, training, etc.) |
| **Reproducibility** | Fixed random seeds, versioned models, saved preprocessing objects |
| **Observability** | Logs + metrics + audit trail for debugging |
| **Security** | JWT auth, secrets in env variables, rate limiting |
| **Scalability** | Stateless API, horizontal scaling, cloud-native design |
| **Reliability** | Health checks, monitoring, graceful degradation |
| **Maintainability** | Type hints, docstrings, separation of concerns |
| **Cost** | Efficient inference, auto-cleanup old data, horizontal scaling |

These principles ensure the system is production-ready and can scale to monitor many hydrogen pipelines.

