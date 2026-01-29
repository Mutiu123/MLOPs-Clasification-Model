# Workflow Diagrams: H2 Pipeline Leak Detection System

## 1. Model Training Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     MODEL TRAINING PIPELINE (BATCH PROCESS)                 │
└─────────────────────────────────────────────────────────────────────────────┘

START
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ DATA INGESTION COMPONENT                                                    │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Query MongoDB for sensor_readings                                          │
│  ├─ Filter by date range (e.g., last 3 months)                             │
│  ├─ Include ground truth labels from lab experiments                        │
│  └─ Fetch 10 sensor fields per reading                                      │
│                                                                              │
│  Output: Raw sensor data DataFrame                                          │
│  ├─ Rows: N sensor readings                                                 │
│  └─ Columns: 10 sensors + 1 target variable (leak_severity)                │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ DATA VALIDATION COMPONENT                                                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Schema Validation                                                          │
│  ├─ Verify all 10 sensor fields present                                     │
│  ├─ Check data types (float, int)                                          │
│  └─ Flag missing values and outliers                                        │
│                                                                              │
│  Drift Detection                                                            │
│  ├─ Compare current data distribution vs training data                      │
│  ├─ Use KL divergence for drift scoring                                    │
│  └─ Alert if drift detected (e.g., > 0.05 threshold)                       │
│                                                                              │
│  Data Quality Report                                                        │
│  ├─ Missing value percentage per column                                     │
│  ├─ Statistical summaries (mean, std, min, max)                            │
│  └─ Record quality metrics                                                  │
│                                                                              │
│ Output: Validated, clean data ready for training                           │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ DATA TRANSFORMATION COMPONENT                                               │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Numerical Preprocessing                                                    │
│  ├─ StandardScaler: pressure (0-100 MPa) → zero mean, unit variance        │
│  ├─ StandardScaler: temperature (-40 to 150°C) → normalized                │
│  ├─ StandardScaler: H2 concentration (0-1M ppm) → scaled                   │
│  └─ StandardScaler: other sensors (vibration, flow, etc.)                  │
│                                                                              │
│  Categorical Encoding                                                       │
│  ├─ OneHotEncoder: material (steel, stainless, composite, aluminum)        │
│  └─ Result: 4 new binary columns                                            │
│                                                                              │
│  Feature Engineering                                                        │
│  ├─ Pressure × Temperature interaction term                                │
│  ├─ H2 concentration × Vibration interaction                               │
│  ├─ Risk Index = (H2_conc × pressure × corrosion) / pipe_age              │
│  └─ Normalized risk score (0-100)                                          │
│                                                                              │
│  Train/Test Split                                                           │
│  ├─ Split: 80% training, 20% testing (stratified)                         │
│  ├─ Random seed = 42 (for reproducibility)                                │
│  └─ Preserve class distribution across splits                              │
│                                                                              │
│ Output: Transformed feature matrices + split indices                        │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ MODEL TRAINER COMPONENT (PARALLEL TRAINING)                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Algorithm 1: scikit-learn RandomForest                                     │
│  ├─ Train with n_estimators=100                                             │
│  ├─ 5-fold cross-validation                                                │
│  └─ Compute mean CV score                                                  │
│      │                                                                      │
│      ▼                                                                      │
│  Algorithm 2: CatBoost                                                      │
│  ├─ Train with iterations=100                                              │
│  ├─ 5-fold cross-validation                                                │
│  └─ Compute mean CV score                                                  │
│      │                                                                      │
│      ▼                                                                      │
│  Algorithm 3: XGBoost                                                       │
│  ├─ Train with n_estimators=100                                             │
│  ├─ 5-fold cross-validation                                                │
│  └─ Compute mean CV score                                                  │
│                                                                              │
│ Output: Three trained models with CV scores                                │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ MODEL EVALUATION COMPONENT                                                  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  For Each Model:                                                            │
│  ├─ Evaluate on hold-out test set                                          │
│  ├─ Compute metrics:                                                        │
│  │  ├─ Accuracy: (TP + TN) / (TP + TN + FP + FN)                          │
│  │  ├─ Precision: TP / (TP + FP)                                           │
│  │  ├─ Recall: TP / (TP + FN)                                              │
│  │  ├─ F1-Score: 2 × (Precision × Recall) / (Precision + Recall)          │
│  │  ├─ AUC-ROC: Area under ROC curve (for binary problems)                │
│  │  └─ Confusion matrix visualization                                      │
│  │                                                                          │
│  ├─ Threshold Tuning (for critical leak detection):                        │
│  │  ├─ Test thresholds: 0.5, 0.6, 0.7, 0.8, 0.9                          │
│  │  ├─ Find threshold that maximizes F1-Score                             │
│  │  └─ Record optimal threshold for deployment                             │
│  │                                                                          │
│  └─ Feature Importance Analysis:                                           │
│     ├─ Identify most important sensors for leak detection                  │
│     └─ Visualize feature importance rankings                               │
│                                                                              │
│  Compare All Models                                                        │
│  ├─ Select model with highest F1-Score                                     │
│  ├─ Fallback: Pick model with best precision (fewer false alarms)         │
│  └─ Champion Model Selected                                                │
│                                                                              │
│ Output: Selected model, metrics report, feature importance                 │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ MODEL PUSHER COMPONENT                                                      │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Serialize Model                                                            │
│  ├─ Save model to pickle format (model.pkl)                                │
│  ├─ Save preprocessing objects (scaler.pkl, encoder.pkl)                   │
│  └─ Save metadata:                                                          │
│     ├─ Training date & time                                                │
│     ├─ Data version & size                                                 │
│     ├─ Model version (e.g., v1.2.3)                                       │
│     ├─ Metrics (accuracy, F1, AUC)                                         │
│     ├─ Optimal threshold                                                    │
│     └─ Feature importance scores                                            │
│                                                                              │
│  Upload to AWS S3                                                           │
│  ├─ S3 Bucket: h2-leak-detection-models                                    │
│  ├─ Path: models/v1.2.3/model.pkl                                         │
│  ├─ Path: models/v1.2.3/metadata.json                                     │
│  └─ Path: models/v1.2.3/artifacts/                                        │
│                                                                              │
│  Register in MongoDB                                                        │
│  ├─ Insert document in model_artifacts collection                          │
│  ├─ Mark as "CANDIDATE" status                                             │
│  └─ Link to S3 location                                                     │
│                                                                              │
│ Output: Model accessible for predictions (but not yet in production)       │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ ARTIFACTS CREATED                                                           │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ MongoDB Documents:                                                          │
│ ├─ Training metrics and history                                             │
│ ├─ Data quality report                                                      │
│ ├─ Model evaluation results                                                 │
│ └─ Model artifact metadata                                                  │
│                                                                              │
│ AWS S3 Objects:                                                             │
│ ├─ Trained model (pickle)                                                   │
│ ├─ Feature preprocessors (pickle)                                           │
│ ├─ Training metadata (JSON)                                                 │
│ ├─ Confusion matrix image                                                   │
│ └─ Feature importance plot                                                  │
│                                                                              │
│ Logs:                                                                       │
│ ├─ Training logs (time, data size, parameters)                             │
│ ├─ Error logs (if validation/drift issues)                                 │
│ └─ Structured JSON logs (timestamp, status, metrics)                       │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
END - Model Ready for Testing
```

---

## 2. Prediction Workflow (Real-time)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      REAL-TIME PREDICTION PIPELINE                          │
└─────────────────────────────────────────────────────────────────────────────┘

CLIENT REQUEST (API or Web Form)
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ FASTAPI ENDPOINT: POST /predict                                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Receive JSON payload:                                                       │
│ {                                                                            │
│   "pressure_mpa": 45.2,              // Pressure in MPa (0-100)            │
│   "temperature_celsius": 25.5,       // Ambient temp (-40 to 150)          │
│   "hydrogen_concentration_ppm": 850, // H2 level (0-1,000,000)             │
│   "vibration_hz": 120,               // Vibration (0-10,000 Hz)            │
│   "pipe_age_years": 5,               // Pipe age (0-100 years)             │
│   "material": "steel",               // Material type                       │
│   "flow_rate_kg_h": 2500,            // Flow rate (0-10,000)               │
│   "corrosion_rate_mm_year": 0.3,     // Corrosion (0-10 mm/year)          │
│   "soil_moisture_percent": 45,       // Soil moisture (0-100%)             │
│   "operating_hours": 8760            // Total operating hours              │
│ }                                                                            │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ INPUT VALIDATION (Pydantic)                                                 │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Validate each field:                                                        │
│ ├─ pressure_mpa: float, min=0, max=100                                     │
│ ├─ temperature_celsius: float, min=-40, max=150                            │
│ ├─ hydrogen_concentration_ppm: float, min=0, max=1000000                   │
│ ├─ vibration_hz: float, min=0, max=10000                                   │
│ ├─ pipe_age_years: float, min=0, max=100                                   │
│ ├─ material: str, enum=['steel','stainless_steel','composite','aluminum']  │
│ ├─ flow_rate_kg_h: float, min=0, max=10000                                 │
│ ├─ corrosion_rate_mm_year: float, min=0, max=10                            │
│ ├─ soil_moisture_percent: float, min=0, max=100                            │
│ └─ operating_hours: float, min=0                                            │
│                                                                              │
│ If validation fails: Return 422 error with detailed messages               │
│ If validation passes: Continue to feature preparation                       │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ FEATURE PREPARATION                                                         │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ 1. Convert to DataFrame                                                    │
│    └─ Create single-row DataFrame from input dict                          │
│                                                                              │
│ 2. Apply Scaling (using saved StandardScaler)                              │
│    ├─ Pressure: (45.2 - 50) / 25 = -0.192                                  │
│    ├─ Temperature: (25.5 - 20) / 35 = 0.157                                │
│    └─ (Repeat for all numerical fields)                                    │
│                                                                              │
│ 3. Encode Categorical Variables (using saved OneHotEncoder)               │
│    ├─ material "steel" → [1, 0, 0, 0]                                      │
│    └─ (Creates 4 columns for 4 material types)                             │
│                                                                              │
│ 4. Feature Engineering (using saved transformers)                          │
│    ├─ Interaction 1: pressure × temperature                                │
│    ├─ Interaction 2: hydrogen × vibration                                  │
│    ├─ Risk Index: (H2 × pressure × corrosion) / pipe_age                  │
│    └─ Normalized risk: min-max scale to 0-100                             │
│                                                                              │
│ Output: Feature vector ready for model                                     │
│ Shape: (1, 20)  # 10 original + 4 one-hot + 6 engineered features         │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ MODEL LOADING & PREDICTION                                                  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ 1. Load Model from S3 (if not cached)                                      │
│    ├─ Bucket: h2-leak-detection-models                                     │
│    ├─ Path: models/v1.2.3/model.pkl                                       │
│    └─ Cache in memory (avoid repeated S3 calls)                            │
│                                                                              │
│ 2. Get Model Predictions                                                   │
│    ├─ Call model.predict(feature_vector)                                   │
│    │  └─ Returns: predicted class (0, 1, 2, or 3)                         │
│    │     0 = no_leak                                                       │
│    │     1 = minor_leak                                                    │
│    │     2 = moderate_leak                                                 │
│    │     3 = critical_leak                                                 │
│    │                                                                        │
│    └─ Call model.predict_proba(feature_vector)                            │
│       └─ Returns: probability for each class                               │
│          [0.92, 0.05, 0.02, 0.01]  # 92% no_leak, 5% minor, etc.         │
│                                                                              │
│ 3. Apply Confidence Threshold                                              │
│    ├─ Threshold (from training): 0.75                                      │
│    ├─ Max probability: 0.92                                                │
│    ├─ Confidence = 0.92 > 0.75 → PASS                                     │
│    └─ Use predicted class (no_leak)                                        │
│                                                                              │
│ Execution Time: < 50ms (including S3 cache lookup)                         │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ POST-PROCESSING & RISK SCORING                                              │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Calculate Risk Score (0-100)                                               │
│ ├─ Base score = min(max_probability * 100, 100)                            │
│ ├─ H2 factor = hydrogen_conc / 1000000 * 30  (max +30 points)             │
│ ├─ Corrosion factor = corrosion_rate / 10 * 20  (max +20 points)          │
│ ├─ Age factor = min(pipe_age / 50 * 10, 10)  (max +10 points)             │
│ └─ Total risk_score = base + H2 + corrosion + age                         │
│    Example: 92 + 25.5 + 6 + 5 = 128.5 → capped at 100                     │
│                                                                              │
│ Generate Recommended Action                                                 │
│ ├─ If prediction = critical_leak → "IMMEDIATE SHUTDOWN"                   │
│ ├─ If prediction = moderate_leak → "SCHEDULE MAINTENANCE"                 │
│ ├─ If prediction = minor_leak → "MONITOR CLOSELY"                         │
│ └─ If prediction = no_leak → "ROUTINE MONITORING"                         │
│                                                                              │
│ Map to Human-Readable Output                                               │
│ ├─ leak_detected: boolean (any leak class or confidence < threshold)       │
│ ├─ leak_severity: string (no_leak, minor_leak, moderate_leak, critical)   │
│ ├─ confidence: float (max probability in decimal)                          │
│ ├─ risk_score: float (0-100 scale)                                         │
│ └─ recommended_action: string (user-friendly instruction)                  │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ RESPONSE GENERATION                                                         │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ JSON Response:                                                              │
│ {                                                                            │
│   "leak_detected": false,                                                   │
│   "leak_severity": "no_leak",                                               │
│   "confidence": 0.92,                                                       │
│   "risk_score": 28.5,                                                       │
│   "recommended_action": "ROUTINE MONITORING",                               │
│   "timestamp": "2026-01-28T14:35:22Z",                                      │
│   "model_version": "v1.2.3"                                                 │
│ }                                                                            │
│                                                                              │
│ HTTP Status: 200 OK                                                         │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ LOGGING & MONITORING                                                        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ Structured JSON Log Entry (to logs/app.log):                              │
│ {                                                                            │
│   "timestamp": "2026-01-28T14:35:22.123Z",                                  │
│   "event": "prediction_made",                                               │
│   "input": {                                                                │
│     "pressure_mpa": 45.2,                                                   │
│     ... (all 10 sensor values)                                              │
│   },                                                                         │
│   "prediction": "no_leak",                                                  │
│   "confidence": 0.92,                                                       │
│   "execution_time_ms": 42,                                                  │
│   "model_version": "v1.2.3"                                                 │
│ }                                                                            │
│                                                                              │
│ Prometheus Metrics:                                                         │
│ ├─ h2_pipeline_predictions_total{severity="no_leak"} += 1                 │
│ ├─ h2_pipeline_leak_confidence{prediction="no_leak"} = 0.92                │
│ ├─ h2_pipeline_prediction_latency_ms = 42                                  │
│ └─ h2_pipeline_risk_score = 28.5                                           │
│                                                                              │
│ Save to MongoDB (predictions collection):                                   │
│ ├─ Sensor input values                                                      │
│ ├─ Prediction result                                                        │
│ ├─ Confidence and risk score                                                │
│ ├─ Execution timestamp                                                      │
│ └─ Model version used                                                       │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
RETURN RESPONSE TO CLIENT
```

---

## 3. Model Deployment Workflow

```
Candidate Model (from training)
  │
  ├─ Initial Validation Testing
  │  ├─ Run on sample of new data
  │  ├─ Check performance metrics
  │  └─ Manual review if needed
  │
  ├─ A/B Testing (Shadow Deployment)
  │  ├─ Run alongside current production model
  │  ├─ Log predictions from both models
  │  ├─ Compare metrics for 1-2 weeks
  │  └─ Verify no degradation
  │
  ├─ Canary Deployment
  │  ├─ Send 10% of requests to new model
  │  ├─ Monitor error rates and latency
  │  ├─ Gradually increase to 50%, then 100%
  │  └─ Rollback if issues detected
  │
  └─ Full Production Deployment
     ├─ Update S3 path in configuration
     ├─ Restart FastAPI application
     ├─ Monitor metrics closely
     └─ Keep previous version available for rollback
```

---

## 4. Data Drift Detection Workflow

```
On Each Training Run:

┌─ Collect Data Statistics
│  ├─ Mean, std, min, max for each sensor
│  ├─ Class distribution (leak types)
│  └─ Correlation matrix
│
├─ Compare vs Previous Data
│  ├─ KL divergence for each feature
│  ├─ Chi-square test for categorical variables
│  └─ Kolmogorov-Smirnov test for distributions
│
└─ Generate Alert if:
   ├─ Any feature drift > 0.05 (threshold)
   ├─ New abnormal patterns detected
   └─ Missing value rate > 10%
       → Notify data team
       → Stop training until investigated
       → Create incident report
```

---

## Summary of Workflows

| Workflow | Trigger | Duration | Output |
|----------|---------|----------|--------|
| Training | Manual trigger or scheduled | 5-30 min | Trained model, metrics |
| Prediction | API request | < 50ms | Leak prediction, risk score |
| Deployment | Manual approval | 5-10 min | Live model in production |
| Drift Detection | Each training cycle | < 1 min | Alert if issues found |

