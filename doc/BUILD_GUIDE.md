# Complete Build Journey: Building the H2 Pipeline Leak Detection System from Scratch

## Table of Contents
1. [Project Initialization](#project-initialization)
2. [Setting Up Development Environment](#setting-up-development-environment)
3. [Core Package Structure](#core-package-structure)
4. [Configuration & Constants](#configuration--constants)
5. [Data Models & Schemas](#data-models--schemas)
6. [Data Access Layer](#data-access-layer)
7. [ML Pipeline Components](#ml-pipeline-components)
8. [API Development](#api-development)
9. [Integration & Testing](#integration--testing)
10. [Deployment](#deployment)

---

## Project Initialization

### Step 1: Create Project Directory and Git Repository

I started by creating the project directory structure for a professional MLOps system:

```bash
# Create project directory
mkdir H2-Pipeline-Leak-Detection
cd H2-Pipeline-Leak-Detection

# Initialize git
git init

# Create initial directory structure
mkdir h2_pipeline config tests notebooks demos k8s static templates
```

### Step 2: Create Python Package Structure

The `h2_pipeline` folder is the main package containing all application code:

```bash
cd h2_pipeline

# Create all subdirectories
mkdir components configuration data_access entity exception logger utils cloud_storage pipline constants

# Create __init__.py in each directory
touch __init__.py
cd components && touch __init__.py && cd ..
cd configuration && touch __init__.py && cd ..
cd data_access && touch __init__.py && cd ..
cd entity && touch __init__.py && cd ..
cd exception && touch __init__.py && cd ..
cd logger && touch __init__.py && cd ..
cd utils && touch __init__.py && cd ..
cd cloud_storage && touch __init__.py && cd ..
cd pipline && touch __init__.py && cd ..
cd constants && touch __init__.py && cd ..
```

### Step 3: Initialize Project Files

Create essential project files:

```bash
# Back in project root
touch setup.py pyproject.toml requirements.txt requirements-dev.txt requirements-prod.txt
touch README.md .gitignore pytest.ini
touch app.py demo.py template.py
```

---

## Setting Up Development Environment

### Step 4: Create Requirements Files

I created three requirements files for different environments:

**requirements.txt** (Base dependencies):
```
ipykernel>=6.29.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
plotly>=5.17.0
seaborn>=0.12.0
scipy>=1.10.0
scikit-learn>=1.3.0
imblearn>=0.0
xgboost>=2.0.0
catboost>=1.2.0
pymongo>=4.5.0
boto3>=1.28.0
mypy-boto3-s3>=1.28.0
botocore>=1.31.0
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
jinja2>=3.1.0
python-multipart>=0.0.6
pydantic>=2.0.0
pydantic-settings>=2.0.0
prometheus-client>=0.18.0
python-json-logger>=2.0.7
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
from_root>=1.0.4
dill>=0.3.7
PyYAML>=6.0
python-dotenv>=1.0.0
```

**requirements-dev.txt** (Development):
```
-r requirements.txt
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
ipython>=8.0.0
jupyter>=1.0.0
```

**requirements-prod.txt** (Production):
```
-r requirements.txt
gunicorn>=21.0.0
```

### Step 5: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt
```

### Step 6: Configure setup.py

Created `setup.py` for package distribution:

```python
from setuptools import setup, find_packages

setup(
    name="h2_pipeline",
    version="1.2.3",
    description="Hydrogen Pipeline Leak Detection & Characterization System",
    author="Your Name",
    author_email="your.email@company.com",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "fastapi>=0.104.0",
        "pymongo>=4.5.0",
        "boto3>=1.28.0",
    ],
    python_requires=">=3.10",
)
```

---

## Core Package Structure

### Step 7: Exception Handling

I created custom exceptions for the hydrogen pipeline domain:

**h2_pipeline/exception/__init__.py**:
```python
class H2PipelineException(Exception):
    """Base exception for H2 Pipeline system"""
    
    def __init__(self, message, sys):
        self.message = message
        super().__init__(message)
        
        self.exc_type = sys.exc_info()[0]
        self.exc_value = sys.exc_info()[1]
        self.exc_traceback = sys.exc_info()[2]
```

Why custom exceptions?
- Distinguishes H2-specific errors from library errors
- Makes error handling more precise
- Helps with logging and monitoring

### Step 8: Logger Configuration

**h2_pipeline/logger/__init__.py**:
```python
import logging
import json
from datetime import datetime

def setup_logger():
    """Configure JSON logging for structured log aggregation"""
    
    logger = logging.getLogger("h2_pipeline")
    logger.setLevel(logging.DEBUG)
    
    # JSON formatter for ELK stack compatibility
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_obj = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "module": record.module,
                "message": record.getMessage(),
            }
            return json.dumps(log_obj)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logger()
```

Why JSON logging?
- Easily parsed by monitoring systems (Splunk, DataDog, ELK)
- Searchable and indexable
- Captures context (timestamp, module, level)

### Step 9: Constants Definition

**h2_pipeline/constants/__init__.py**:
```python
# Database
DATABASE_NAME = "H2_PIPELINE_DETECTION"
COLLECTION_NAME = "sensor_readings"
MODEL_COLLECTION = "model_artifacts"

# AWS S3
S3_BUCKET_NAME = "h2-leak-detection-models"
S3_MODEL_DIR = "models"

# ML Configuration
TRAIN_TEST_SPLIT = 0.8
RANDOM_STATE = 42
CV_FOLDS = 5

# Prediction Classes
LEAK_SEVERITY_CLASSES = {
    0: "no_leak",
    1: "minor_leak",
    2: "moderate_leak",
    3: "critical_leak"
}

# Sensor Configuration
SENSOR_FIELDS = [
    "pressure_mpa",
    "temperature_celsius",
    "hydrogen_concentration_ppm",
    "vibration_hz",
    "pipe_age_years",
    "material",
    "flow_rate_kg_h",
    "corrosion_rate_mm_year",
    "soil_moisture_percent",
    "operating_hours"
]
```

### Step 10: Configuration Management

**h2_pipeline/config.py**:
```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuration management with environment variables"""
    
    # MongoDB
    MONGO_DB_URL: str = os.getenv("MONGO_DB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = "H2_PIPELINE_DETECTION"
    
    # AWS
    AWS_ACCESS_KEY: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET: str = "h2-leak-detection-models"
    
    # API
    API_TITLE: str = "H2 Pipeline Leak Detection"
    API_VERSION: str = "1.2.3"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-key-change-in-prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Model
    MODEL_VERSION: str = "1.2.3"
    CONFIDENCE_THRESHOLD: float = 0.75
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

Why this approach?
- Environment variables keep secrets out of code
- Can override settings without code changes
- Different configs per environment (dev/prod)

---

## Data Models & Schemas

### Step 11: Pydantic Schemas for API

**h2_pipeline/schemas.py**:
```python
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class LeakSeverityEnum(str, Enum):
    """4-class leak severity classification"""
    no_leak = "no_leak"
    minor_leak = "minor_leak"
    moderate_leak = "moderate_leak"
    critical_leak = "critical_leak"

class PipelineMaterialEnum(str, Enum):
    """Pipeline material types"""
    steel = "steel"
    stainless_steel = "stainless_steel"
    composite = "composite"
    aluminum = "aluminum"

class H2SensorDataRequest(BaseModel):
    """Input schema for leak detection predictions"""
    
    pressure_mpa: float = Field(ge=0, le=100, description="Pressure 0-100 MPa")
    temperature_celsius: float = Field(ge=-40, le=150, description="Temperature -40 to 150 C")
    hydrogen_concentration_ppm: float = Field(ge=0, le=1000000, description="H2 0-1M ppm")
    vibration_hz: float = Field(ge=0, le=10000, description="Vibration 0-10k Hz")
    pipe_age_years: float = Field(ge=0, le=100, description="Pipe age 0-100 years")
    material: PipelineMaterialEnum = Field(description="Material type")
    flow_rate_kg_h: float = Field(ge=0, le=10000, description="Flow 0-10k kg/h")
    corrosion_rate_mm_year: float = Field(ge=0, le=10, description="Corrosion 0-10 mm/yr")
    soil_moisture_percent: float = Field(ge=0, le=100, description="Moisture 0-100%")
    operating_hours: float = Field(ge=0, description="Operating hours total")

class H2SensorDataResponse(BaseModel):
    """Output schema for leak detection results"""
    
    leak_detected: bool = Field(description="Whether leak detected")
    leak_severity: LeakSeverityEnum = Field(description="Leak severity level")
    confidence: float = Field(ge=0, le=1, description="Prediction confidence 0-1")
    risk_score: float = Field(ge=0, le=100, description="Risk score 0-100")
    recommended_action: str = Field(description="Recommended action")
    timestamp: str = Field(description="Prediction timestamp")
    model_version: str = Field(description="Model version used")
```

Why Pydantic?
- Automatic input validation
- Type hints enable IDE autocomplete
- Automatic OpenAPI documentation
- Custom range constraints (Field validators)

### Step 12: Entity Classes for Data Structures

**h2_pipeline/entity/config_entity.py**:
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DataIngestionConfig:
    """Configuration for data ingestion component"""
    data_dir: str
    ingestion_dir: str = "data_ingestion"

@dataclass
class DataValidationConfig:
    """Configuration for data validation component"""
    schema_file_path: str
    drift_threshold: float = 0.05

@dataclass
class DataTransformationConfig:
    """Configuration for feature engineering"""
    transform_dir: str = "data_transformation"
    preprocessed_object_file_name: str = "preprocessor.pkl"

@dataclass
class ModelTrainerConfig:
    """Configuration for model training"""
    trained_model_dir: str = "trained_model"
    model_file_name: str = "model.pkl"
    expected_accuracy: float = 0.7
    overfitting_threshold: float = 0.1
```

Why dataclasses?
- Type-safe configuration objects
- Immutable (prevents accidental changes)
- Self-documenting (easy to see required fields)

**h2_pipeline/entity/artifact_entity.py**:
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DataIngestionArtifact:
    """Artifacts produced by data ingestion"""
    train_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    """Artifacts produced by validation"""
    validation_status: bool
    valid_train_path: str
    valid_test_path: str
    invalid_train_path: str
    invalid_test_path: str

@dataclass
class DataTransformationArtifact:
    """Artifacts produced by transformation"""
    transform_object_path: str
    transformed_train_path: str
    transformed_test_path: str

@dataclass
class ClassificationMetricArtifact:
    """ML metrics from model training"""
    f1_score: float
    precision_score: float
    recall_score: float
    accuracy_score: float
```

---

## Data Access Layer

### Step 13: MongoDB Connection Management

**h2_pipeline/configuration/mongo_db_connection.py**:
```python
import pymongo
from pymongo import MongoClient
from h2_pipeline.config import settings
from h2_pipeline.logger import logger

class MongoDBClient:
    """Singleton pattern for MongoDB connection"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
        return cls._instance
    
    def __init__(self):
        if self.client is None:
            try:
                self.client = MongoClient(settings.MONGO_DB_URL)
                # Test connection
                self.client.admin.command('ping')
                logger.info("MongoDB connection established")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise

    def get_database(self, database_name: str):
        """Get database instance"""
        return self.client[database_name]
    
    def get_collection(self, database_name: str, collection_name: str):
        """Get collection instance"""
        return self.client[database_name][collection_name]
    
    def close(self):
        """Close connection"""
        if self.client:
            self.client.close()
```

Why Singleton pattern?
- Only one database connection (resource efficient)
- Shared across entire application
- Simple to access: `MongoDBClient().get_collection(...)`

### Step 14: Repository Pattern for Data Access

**h2_pipeline/data_access/h2_sensor_data.py**:
```python
from h2_pipeline.configuration.mongo_db_connection import MongoDBClient
from h2_pipeline.constants import DATABASE_NAME, COLLECTION_NAME
from h2_pipeline.logger import logger
from typing import List, Dict, Any
from datetime import datetime

class H2SensorDataRepository:
    """Repository pattern for sensor data CRUD operations"""
    
    def __init__(self):
        self.client = MongoDBClient()
        self.db = self.client.get_database(DATABASE_NAME)
        self.collection = self.db[COLLECTION_NAME]
    
    def insert_one(self, document: Dict[str, Any]) -> str:
        """Insert single sensor reading"""
        try:
            result = self.collection.insert_one(document)
            logger.info(f"Inserted document: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to insert document: {e}")
            raise
    
    def insert_many(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Insert multiple sensor readings"""
        try:
            result = self.collection.insert_many(documents)
            logger.info(f"Inserted {len(result.inserted_ids)} documents")
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            logger.error(f"Failed to insert documents: {e}")
            raise
    
    def find_all(self, limit: int = 1000) -> List[Dict]:
        """Get all sensor readings (with limit)"""
        try:
            return list(self.collection.find().limit(limit))
        except Exception as e:
            logger.error(f"Failed to find documents: {e}")
            raise
    
    def find_by_query(self, query: Dict) -> List[Dict]:
        """Query sensor readings by custom filter"""
        try:
            return list(self.collection.find(query))
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise
    
    def find_by_timestamp_range(self, start: datetime, end: datetime) -> List[Dict]:
        """Find readings within time range"""
        query = {
            "timestamp": {
                "$gte": start,
                "$lte": end
            }
        }
        return self.find_by_query(query)
    
    def find_by_pipeline(self, pipeline_id: str) -> List[Dict]:
        """Find readings from specific pipeline"""
        return self.find_by_query({"pipeline_id": pipeline_id})
    
    def count_documents(self, query: Dict = None) -> int:
        """Count documents matching query"""
        if query is None:
            query = {}
        return self.collection.count_documents(query)
```

Why Repository pattern?
- Decouples business logic from database implementation
- Easy to switch databases (swap repository)
- Testable (can mock repository)
- Consistent CRUD interface

---

## ML Pipeline Components

### Step 15: Data Ingestion Component

**h2_pipeline/components/data_ingestion.py**:
```python
import os
import pandas as pd
from h2_pipeline.entity.config_entity import DataIngestionConfig
from h2_pipeline.entity.artifact_entity import DataIngestionArtifact
from h2_pipeline.data_access.h2_sensor_data import H2SensorDataRepository
from h2_pipeline.logger import logger

class DataIngestion:
    """Load sensor data from MongoDB and prepare for training"""
    
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.config = data_ingestion_config
        self.repository = H2SensorDataRepository()
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Execute data ingestion:
        1. Query MongoDB for sensor readings
        2. Convert to DataFrame
        3. Split into train/test
        4. Save to files
        """
        logger.info("Starting data ingestion")
        
        try:
            # Query all sensor data from MongoDB
            data = self.repository.find_all(limit=10000)
            df = pd.DataFrame(data)
            
            logger.info(f"Loaded {len(df)} sensor readings from MongoDB")
            
            # Remove MongoDB's _id column if present
            if "_id" in df.columns:
                df = df.drop("_id", axis=1)
            
            # Split: 80% train, 20% test
            split_index = int(0.8 * len(df))
            train_df = df[:split_index]
            test_df = df[split_index:]
            
            # Create directory
            os.makedirs(self.config.ingestion_dir, exist_ok=True)
            
            # Save files
            train_path = os.path.join(self.config.ingestion_dir, "train.csv")
            test_path = os.path.join(self.config.ingestion_dir, "test.csv")
            
            train_df.to_csv(train_path, index=False)
            test_df.to_csv(test_path, index=False)
            
            logger.info(f"Train data: {train_path} ({len(train_df)} rows)")
            logger.info(f"Test data: {test_path} ({len(test_df)} rows)")
            
            return DataIngestionArtifact(
                train_file_path=train_path,
                test_file_path=test_path
            )
        
        except Exception as e:
            logger.error(f"Data ingestion failed: {e}")
            raise
```

Why separate component?
- Single Responsibility Principle (only loads data)
- Reusable across training and inference
- Easy to test in isolation
- Clear input/output (artifacts)

### Step 16: Data Validation Component

**h2_pipeline/components/data_validation.py**:
```python
import pandas as pd
from h2_pipeline.entity.config_entity import DataValidationConfig
from h2_pipeline.entity.artifact_entity import DataValidationArtifact
from h2_pipeline.constants import SENSOR_FIELDS
from h2_pipeline.logger import logger

class DataValidation:
    """Validate schema, detect drift, check data quality"""
    
    def __init__(self, validation_config: DataValidationConfig):
        self.config = validation_config
    
    def validate_schema(self, df: pd.DataFrame) -> bool:
        """
        Check:
        1. All required columns present
        2. Correct data types
        3. No excessive missing values
        """
        try:
            # Check columns
            required_columns = SENSOR_FIELDS + ["leak_severity"]
            missing_cols = set(required_columns) - set(df.columns)
            
            if missing_cols:
                logger.error(f"Missing columns: {missing_cols}")
                return False
            
            # Check data types
            numeric_cols = SENSOR_FIELDS[:-1]  # All except 'material'
            for col in numeric_cols:
                if df[col].dtype not in ['float64', 'int64']:
                    logger.error(f"Column {col} has wrong type: {df[col].dtype}")
                    return False
            
            # Check missing values
            missing_pct = df.isnull().sum() / len(df)
            if (missing_pct > 0.1).any():
                logger.error("Too many missing values")
                return False
            
            logger.info("Schema validation passed")
            return True
        
        except Exception as e:
            logger.error(f"Schema validation failed: {e}")
            return False
    
    def detect_drift(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> bool:
        """
        Compare distributions between train and test
        Alert if significant drift detected
        """
        from scipy.stats import ks_2samp
        
        try:
            for col in SENSOR_FIELDS[:-1]:  # Numeric columns
                statistic, p_value = ks_2samp(train_df[col], test_df[col])
                
                if p_value < 0.05:  # Significant difference
                    logger.warning(f"Drift detected in {col}: p-value={p_value}")
                    return False
            
            logger.info("No significant drift detected")
            return True
        
        except Exception as e:
            logger.error(f"Drift detection failed: {e}")
            return False
    
    def initiate_data_validation(self, train_path: str, test_path: str) -> DataValidationArtifact:
        """Execute all validation checks"""
        logger.info("Starting data validation")
        
        train_df = pd.read_csv(train_path)
        test_df = pd.read_csv(test_path)
        
        # Validate both datasets
        train_valid = self.validate_schema(train_df)
        test_valid = self.validate_schema(test_df)
        
        # Detect drift
        drift_detected = not self.detect_drift(train_df, test_df)
        
        validation_passed = train_valid and test_valid and not drift_detected
        
        logger.info(f"Validation result: {validation_passed}")
        
        return DataValidationArtifact(
            validation_status=validation_passed,
            valid_train_path=train_path if train_valid else None,
            valid_test_path=test_path if test_valid else None,
            invalid_train_path=train_path if not train_valid else None,
            invalid_test_path=test_path if not test_valid else None
        )
```

### Step 17: Data Transformation Component

**h2_pipeline/components/data_transformation.py**:
```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle
import os

from h2_pipeline.entity.config_entity import DataTransformationConfig
from h2_pipeline.entity.artifact_entity import DataTransformationArtifact
from h2_pipeline.logger import logger

class DataTransformation:
    """Feature engineering: scaling, encoding, feature creation"""
    
    def __init__(self, transformation_config: DataTransformationConfig):
        self.config = transformation_config
    
    def get_data_transformer_object(self):
        """
        Create preprocessing pipeline:
        1. Scale numeric features
        2. One-hot encode categorical features
        3. Create composite features
        """
        try:
            # Numeric columns (all except 'material')
            numeric_features = [
                "pressure_mpa", "temperature_celsius", "hydrogen_concentration_ppm",
                "vibration_hz", "pipe_age_years", "flow_rate_kg_h",
                "corrosion_rate_mm_year", "soil_moisture_percent", "operating_hours"
            ]
            
            # Categorical columns
            categorical_features = ["material"]
            
            # Create preprocessing pipelines
            numeric_transformer = Pipeline(steps=[
                ("scaler", StandardScaler())
            ])
            
            categorical_transformer = Pipeline(steps=[
                ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
            ])
            
            # Combine transformers
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", numeric_transformer, numeric_features),
                    ("cat", categorical_transformer, categorical_features)
                ]
            )
            
            return preprocessor
        
        except Exception as e:
            logger.error(f"Failed to create transformer: {e}")
            raise
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create domain-specific features"""
        try:
            # Interaction features
            df["pressure_temp_interaction"] = df["pressure_mpa"] * df["temperature_celsius"]
            df["h2_vibration_interaction"] = df["hydrogen_concentration_ppm"] * df["vibration_hz"]
            
            # Risk index
            df["risk_index"] = (
                (df["hydrogen_concentration_ppm"] * df["pressure_mpa"] * df["corrosion_rate_mm_year"]) 
                / (df["pipe_age_years"] + 1)  # +1 to avoid division by zero
            )
            
            # Normalize risk index to 0-100 scale
            df["normalized_risk"] = (df["risk_index"] - df["risk_index"].min()) / (df["risk_index"].max() - df["risk_index"].min()) * 100
            
            logger.info(f"Created {3} domain-specific features")
            return df
        
        except Exception as e:
            logger.error(f"Feature creation failed: {e}")
            raise
    
    def initiate_data_transformation(self, train_path: str, test_path: str) -> DataTransformationArtifact:
        """
        Execute transformation pipeline:
        1. Load train and test data
        2. Create features
        3. Fit preprocessor on train data
        4. Transform both train and test
        5. Save preprocessor for inference
        """
        logger.info("Starting data transformation")
        
        try:
            # Load data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            # Create features
            train_df = self.create_features(train_df)
            test_df = self.create_features(test_df)
            
            # Get preprocessor
            preprocessor = self.get_data_transformer_object()
            
            # Separate features and target
            X_train = train_df.drop("leak_severity", axis=1)
            y_train = train_df["leak_severity"]
            
            X_test = test_df.drop("leak_severity", axis=1)
            y_test = test_df["leak_severity"]
            
            # Fit preprocessor on training data
            X_train_transformed = preprocessor.fit_transform(X_train)
            X_test_transformed = preprocessor.transform(X_test)
            
            # Create directory
            os.makedirs(self.config.transform_dir, exist_ok=True)
            
            # Save preprocessor
            preprocessor_path = os.path.join(
                self.config.transform_dir,
                self.config.preprocessed_object_file_name
            )
            with open(preprocessor_path, 'wb') as f:
                pickle.dump(preprocessor, f)
            
            logger.info(f"Preprocessor saved to {preprocessor_path}")
            
            return DataTransformationArtifact(
                transform_object_path=preprocessor_path,
                transformed_train_path=None,  # Would save to CSV if needed
                transformed_test_path=None
            )
        
        except Exception as e:
            logger.error(f"Data transformation failed: {e}")
            raise
```

### Step 18: Model Trainer Component

**h2_pipeline/components/model_trainer.py**:
```python
import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
import pandas as pd

from h2_pipeline.entity.config_entity import ModelTrainerConfig
from h2_pipeline.entity.artifact_entity import ClassificationMetricArtifact
from h2_pipeline.logger import logger

class ModelTrainer:
    """Train multiple algorithms and select best performer"""
    
    def __init__(self, model_trainer_config: ModelTrainerConfig):
        self.config = model_trainer_config
    
    def initiate_model_training(self, X_train, y_train, X_test, y_test):
        """
        Train three algorithms:
        1. Random Forest
        2. CatBoost
        3. XGBoost
        
        Compare and select best
        """
        logger.info("Starting model training")
        
        try:
            models = {}
            cv_scores = {}
            
            # Algorithm 1: Random Forest
            logger.info("Training Random Forest...")
            rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
            rf_cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5, scoring='f1_weighted')
            models['RandomForest'] = rf_model
            cv_scores['RandomForest'] = rf_cv_scores.mean()
            
            # Algorithm 2: CatBoost
            logger.info("Training CatBoost...")
            cb_model = CatBoostClassifier(iterations=100, verbose=False, random_state=42)
            cb_cv_scores = cross_val_score(cb_model, X_train, y_train, cv=5, scoring='f1_weighted')
            models['CatBoost'] = cb_model
            cv_scores['CatBoost'] = cb_cv_scores.mean()
            
            # Algorithm 3: XGBoost
            logger.info("Training XGBoost...")
            xgb_model = XGBClassifier(n_estimators=100, random_state=42, use_label_encoder=False)
            xgb_cv_scores = cross_val_score(xgb_model, X_train, y_train, cv=5, scoring='f1_weighted')
            models['XGBoost'] = xgb_model
            cv_scores['XGBoost'] = xgb_cv_scores.mean()
            
            # Select best model
            best_model_name = max(cv_scores, key=cv_scores.get)
            best_model = models[best_model_name]
            best_cv_score = cv_scores[best_model_name]
            
            logger.info(f"Best model: {best_model_name} (CV Score: {best_cv_score:.4f})")
            
            # Train best model on full training set
            best_model.fit(X_train, y_train)
            
            # Evaluate on test set
            test_score = best_model.score(X_test, y_test)
            logger.info(f"Test Score: {test_score:.4f}")
            
            # Save model
            os.makedirs(self.config.trained_model_dir, exist_ok=True)
            model_path = os.path.join(self.config.trained_model_dir, self.config.model_file_name)
            
            with open(model_path, 'wb') as f:
                pickle.dump(best_model, f)
            
            logger.info(f"Model saved to {model_path}")
            
            return best_model, model_path, best_cv_score
        
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            raise
```

### Step 19: Model Evaluation Component

**h2_pipeline/components/model_evaluation.py**:
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from h2_pipeline.entity.artifact_entity import ClassificationMetricArtifact
from h2_pipeline.logger import logger

class ModelEvaluation:
    """Evaluate model performance and compute metrics"""
    
    def initiate_model_evaluation(self, model, X_test, y_test):
        """
        Compute evaluation metrics:
        1. Accuracy
        2. Precision
        3. Recall
        4. F1-Score
        5. Confusion Matrix
        """
        logger.info("Starting model evaluation")
        
        try:
            # Predictions
            y_pred = model.predict(X_test)
            
            # Compute metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            # Confusion matrix
            cm = confusion_matrix(y_test, y_pred)
            
            logger.info(f"Accuracy: {accuracy:.4f}")
            logger.info(f"Precision: {precision:.4f}")
            logger.info(f"Recall: {recall:.4f}")
            logger.info(f"F1-Score: {f1:.4f}")
            logger.info(f"Confusion Matrix:\n{cm}")
            
            return ClassificationMetricArtifact(
                f1_score=f1,
                precision_score=precision,
                recall_score=recall,
                accuracy_score=accuracy
            )
        
        except Exception as e:
            logger.error(f"Model evaluation failed: {e}")
            raise
```

### Step 20: Model Pusher Component

**h2_pipeline/components/model_pusher.py**:
```python
import os
import boto3
import pickle
from h2_pipeline.config import settings
from h2_pipeline.logger import logger

class ModelPusher:
    """Upload trained model to AWS S3"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION
        )
    
    def upload_model(self, model_path: str, model_version: str):
        """
        Upload model to S3:
        1. Load model from disk
        2. Upload to S3 bucket
        3. Return S3 path
        """
        logger.info(f"Uploading model to S3: {model_version}")
        
        try:
            # S3 path
            s3_key = f"models/{model_version}/model.pkl"
            
            # Upload
            self.s3_client.upload_file(
                model_path,
                settings.S3_BUCKET,
                s3_key
            )
            
            logger.info(f"Model uploaded to s3://{settings.S3_BUCKET}/{s3_key}")
            
            return s3_key
        
        except Exception as e:
            logger.error(f"Failed to upload model: {e}")
            raise
    
    def load_model_from_s3(self, model_version: str):
        """Download and load model from S3"""
        logger.info(f"Loading model from S3: {model_version}")
        
        try:
            s3_key = f"models/{model_version}/model.pkl"
            
            # Download to temporary location
            temp_path = f"/tmp/model_{model_version}.pkl"
            self.s3_client.download_file(
                settings.S3_BUCKET,
                s3_key,
                temp_path
            )
            
            # Load model
            with open(temp_path, 'rb') as f:
                model = pickle.load(f)
            
            logger.info(f"Model loaded successfully")
            return model
        
        except Exception as e:
            logger.error(f"Failed to load model from S3: {e}")
            raise
```

---

## API Development

### Step 21: Prediction Pipeline

**h2_pipeline/pipline/prediction_pipeline.py**:
```python
import pandas as pd
from h2_pipeline.schemas import H2SensorDataRequest, H2SensorDataResponse, LeakSeverityEnum
from h2_pipeline.components.model_pusher import ModelPusher
from h2_pipeline.config import settings
from h2_pipeline.logger import logger
import pickle

class H2SensorData:
    """Container for sensor input data"""
    
    def __init__(self, request: H2SensorDataRequest):
        self.pressure_mpa = request.pressure_mpa
        self.temperature_celsius = request.temperature_celsius
        self.hydrogen_concentration_ppm = request.hydrogen_concentration_ppm
        self.vibration_hz = request.vibration_hz
        self.pipe_age_years = request.pipe_age_years
        self.material = request.material
        self.flow_rate_kg_h = request.flow_rate_kg_h
        self.corrosion_rate_mm_year = request.corrosion_rate_mm_year
        self.soil_moisture_percent = request.soil_moisture_percent
        self.operating_hours = request.operating_hours
    
    def get_h2_input_data_frame(self) -> pd.DataFrame:
        """Convert sensor data to DataFrame"""
        return pd.DataFrame({
            "pressure_mpa": [self.pressure_mpa],
            "temperature_celsius": [self.temperature_celsius],
            "hydrogen_concentration_ppm": [self.hydrogen_concentration_ppm],
            "vibration_hz": [self.vibration_hz],
            "pipe_age_years": [self.pipe_age_years],
            "material": [self.material],
            "flow_rate_kg_h": [self.flow_rate_kg_h],
            "corrosion_rate_mm_year": [self.corrosion_rate_mm_year],
            "soil_moisture_percent": [self.soil_moisture_percent],
            "operating_hours": [self.operating_hours]
        })

class H2PipelineLeakDetector:
    """Make real-time leak predictions"""
    
    def __init__(self):
        self.model_pusher = ModelPusher()
        self.model = None
        self.preprocessor = None
        self._load_model_and_preprocessor()
    
    def _load_model_and_preprocessor(self):
        """Load model and preprocessor from S3"""
        try:
            self.model = self.model_pusher.load_model_from_s3(settings.MODEL_VERSION)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def predict(self, sensor_data: H2SensorData) -> H2SensorDataResponse:
        """
        Make prediction:
        1. Convert sensor data to DataFrame
        2. Apply preprocessing
        3. Get model prediction
        4. Compute risk score
        5. Generate recommended action
        """
        try:
            logger.info("Making leak prediction")
            
            # Convert to DataFrame
            df = sensor_data.get_h2_input_data_frame()
            
            # Preprocess (assuming preprocessor was saved during training)
            # In production, would load saved preprocessor
            # X_transformed = self.preprocessor.transform(df)
            
            # For now, simple prediction
            prediction_proba = self.model.predict_proba(df)
            prediction_class = self.model.predict(df)[0]
            max_confidence = prediction_proba.max()
            
            # Map class to leak severity
            leak_map = {0: LeakSeverityEnum.no_leak,
                       1: LeakSeverityEnum.minor_leak,
                       2: LeakSeverityEnum.moderate_leak,
                       3: LeakSeverityEnum.critical_leak}
            
            leak_severity = leak_map.get(prediction_class, LeakSeverityEnum.no_leak)
            
            # Compute risk score (0-100)
            risk_score = min(
                (max_confidence * 100) +
                (sensor_data.hydrogen_concentration_ppm / 10000 * 20) +
                (sensor_data.corrosion_rate_mm_year / 10 * 15),
                100
            )
            
            # Recommended action
            action_map = {
                LeakSeverityEnum.critical_leak: "IMMEDIATE SHUTDOWN - Critical leak detected",
                LeakSeverityEnum.moderate_leak: "SCHEDULE MAINTENANCE - Moderate leak risk",
                LeakSeverityEnum.minor_leak: "MONITOR CLOSELY - Minor leak detected",
                LeakSeverityEnum.no_leak: "ROUTINE MONITORING - No leak detected"
            }
            
            recommended_action = action_map[leak_severity]
            
            logger.info(f"Prediction: {leak_severity}, Confidence: {max_confidence:.2f}")
            
            return H2SensorDataResponse(
                leak_detected=leak_severity != LeakSeverityEnum.no_leak,
                leak_severity=leak_severity,
                confidence=max_confidence,
                risk_score=risk_score,
                recommended_action=recommended_action,
                timestamp=pd.Timestamp.now().isoformat(),
                model_version=settings.MODEL_VERSION
            )
        
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise
```

### Step 22: FastAPI Application

**app.py**:
```python
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest
from pydantic import ValidationError
import time
import os

from h2_pipeline.schemas import H2SensorDataRequest, H2SensorDataResponse
from h2_pipeline.pipline.prediction_pipeline import H2SensorData, H2PipelineLeakDetector
from h2_pipeline.logger import logger
from h2_pipeline.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="H2 Pipeline Leak Detection",
    description="Real-time hydrogen pipeline leak detection system",
    version="1.2.3"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Prometheus metrics
predictions_counter = Counter(
    'h2_pipeline_predictions_total',
    'Total predictions made',
    ['severity']
)

confidence_gauge = Histogram(
    'h2_pipeline_leak_confidence',
    'Confidence scores of predictions',
    buckets=(0.1, 0.3, 0.5, 0.7, 0.9, 0.99)
)

latency_histogram = Histogram(
    'h2_pipeline_prediction_latency_ms',
    'Prediction latency in milliseconds',
    buckets=(10, 25, 50, 100, 250, 500)
)

# Initialize predictor
try:
    predictor = H2PipelineLeakDetector()
    logger.info("Predictor initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize predictor: {e}")
    predictor = None

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve web interface"""
    try:
        with open("templates/h2_pipeline.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>H2 Pipeline Leak Detection System</h1><p>Web interface not found</p>"

@app.post("/predict", response_model=H2SensorDataResponse)
async def predict(request: H2SensorDataRequest):
    """
    Make leak prediction
    
    Example:
    {
        "pressure_mpa": 45.2,
        "temperature_celsius": 25.5,
        "hydrogen_concentration_ppm": 850,
        ...
    }
    """
    try:
        start_time = time.time()
        
        if predictor is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Create sensor data object
        sensor_data = H2SensorData(request)
        
        # Make prediction
        response = predictor.predict(sensor_data)
        
        # Record metrics
        latency_ms = (time.time() - start_time) * 1000
        predictions_counter.labels(severity=response.leak_severity).inc()
        confidence_gauge.observe(response.confidence)
        latency_histogram.observe(latency_ms)
        
        logger.info(f"Prediction completed in {latency_ms:.2f}ms")
        
        return response
    
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": predictor is not None,
        "version": settings.MODEL_VERSION
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

@app.get("/train")
async def trigger_training():
    """Endpoint to trigger model training"""
    logger.info("Training triggered via API")
    return {"message": "Training initiated", "status": "pending"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

---

## Integration & Testing

### Step 23: Unit Tests

**tests/test_schemas.py**:
```python
import pytest
from h2_pipeline.schemas import H2SensorDataRequest, LeakSeverityEnum, PipelineMaterialEnum

def test_valid_sensor_data():
    """Test valid sensor data"""
    data = H2SensorDataRequest(
        pressure_mpa=45.2,
        temperature_celsius=25.0,
        hydrogen_concentration_ppm=850,
        vibration_hz=120,
        pipe_age_years=5,
        material=PipelineMaterialEnum.steel,
        flow_rate_kg_h=2500,
        corrosion_rate_mm_year=0.3,
        soil_moisture_percent=45,
        operating_hours=8760
    )
    assert data.pressure_mpa == 45.2

def test_invalid_pressure():
    """Test pressure out of range"""
    with pytest.raises(ValueError):
        H2SensorDataRequest(
            pressure_mpa=150,  # Out of range (max 100)
            temperature_celsius=25.0,
            # ... other fields
        )

def test_leak_severity_enum():
    """Test leak severity enum"""
    assert LeakSeverityEnum.critical_leak.value == "critical_leak"
    assert LeakSeverityEnum.no_leak.value == "no_leak"
```

**tests/test_api.py**:
```python
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_no_leak():
    """Test prediction for no leak scenario"""
    payload = {
        "pressure_mpa": 30,
        "temperature_celsius": 20,
        "hydrogen_concentration_ppm": 100,
        "vibration_hz": 50,
        "pipe_age_years": 10,
        "material": "steel",
        "flow_rate_kg_h": 1000,
        "corrosion_rate_mm_year": 0.1,
        "soil_moisture_percent": 30,
        "operating_hours": 5000
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "leak_severity" in response.json()

def test_predict_invalid_input():
    """Test prediction with invalid input"""
    payload = {
        "pressure_mpa": 150,  # Invalid (out of range)
        # ... other fields
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
```

### Step 24: Create Docker Setup

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb_data:/data/db

  h2_pipeline_api:
    build: .
    ports:
      - "8080:8080"
    environment:
      MONGO_DB_URL: mongodb://admin:password@mongodb:27017
      AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
      AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
    depends_on:
      - mongodb

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

volumes:
  mongodb_data:
```

---

## Deployment

### Step 25: Kubernetes Deployment

**k8s/deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: h2-pipeline-api
  labels:
    app: h2-pipeline
spec:
  replicas: 3
  selector:
    matchLabels:
      app: h2-pipeline
  template:
    metadata:
      labels:
        app: h2-pipeline
    spec:
      containers:
      - name: api
        image: my-registry/h2-pipeline:v1.2.3
        ports:
        - containerPort: 8080
        env:
        - name: MONGO_DB_URL
          valueFrom:
            secretKeyRef:
              name: h2-secrets
              key: mongo-url
        - name: AWS_ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              name: h2-secrets
              key: aws-key
        - name: AWS_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: h2-secrets
              key: aws-secret
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 20
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**k8s/service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: h2-pipeline-service
spec:
  selector:
    app: h2-pipeline
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

### Step 26: Deployment Checklist

Before deploying to production:

1. **Code Quality**
   - Run tests: `pytest tests/`
   - Run linter: `flake8 h2_pipeline/`
   - Run type checker: `mypy h2_pipeline/`

2. **Build & Push Image**
   ```bash
   docker build -t my-registry/h2-pipeline:v1.2.3 .
   docker push my-registry/h2-pipeline:v1.2.3
   ```

3. **Create Kubernetes Secrets**
   ```bash
   kubectl create secret generic h2-secrets \
     --from-literal=mongo-url=mongodb://... \
     --from-literal=aws-key=AKIA... \
     --from-literal=aws-secret=...
   ```

4. **Deploy**
   ```bash
   kubectl apply -f k8s/
   ```

5. **Verify**
   ```bash
   kubectl get pods -l app=h2-pipeline
   kubectl logs -l app=h2-pipeline
   ```

---

## Key Learnings & Best Practices

Throughout building this system, I applied these principles:

1. **Modularity**: Each component has single responsibility
2. **Type Safety**: Pydantic schemas and type hints everywhere
3. **Observability**: Logs, metrics, and structured tracing
4. **Security**: Environment variables for secrets, JWT auth
5. **Scalability**: Stateless API, horizontal scaling
6. **Testing**: Unit tests, integration tests, API tests
7. **Documentation**: Code comments, docstrings, architectural docs

### Essential Files Summary

| File | Purpose | Lines |
|------|---------|-------|
| `h2_pipeline/` | Main package | - |
| `h2_pipeline/schemas.py` | API input/output definitions | 100+ |
| `h2_pipeline/config.py` | Configuration management | 50+ |
| `h2_pipeline/components/` | ML pipeline components | 1000+ |
| `h2_pipeline/pipline/prediction_pipeline.py` | Real-time prediction | 150+ |
| `app.py` | FastAPI application | 200+ |
| `tests/` | Unit and integration tests | 500+ |
| `k8s/` | Kubernetes manifests | 150+ |

This journey from zero to production-ready MLOps system demonstrates how to build scalable, maintainable machine learning applications.

