from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import joblib
import os
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

logger.info("=" * 80)
logger.info("DIABETES PREDICTION API - STARTUP")
logger.info("=" * 80)
logger.info(f"Python Version: {sys.version}")
logger.info(f"Current Working Directory: {os.getcwd()}")
logger.info(f"Files in directory: {os.listdir('.')}")
logger.info("=" * 80)

app = FastAPI(
    title="Diabetes Prediction API",
    description="FastAPI backend for diabetes prediction using Random Forest",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
model = None
scaler = None

logger.info("Loading model and scaler...")

try:
    model = joblib.load("diabetes_model.joblib")
    logger.info("✓ Model loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load model: {e}")

try:
    scaler = joblib.load("scaler.joblib")
    logger.info("✓ Scaler loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load scaler: {e}")

logger.info("=" * 80)
logger.info(f"Model loaded: {model is not None}")
logger.info(f"Scaler loaded: {scaler is not None}")
logger.info("=" * 80)

class PatientData(BaseModel):
    Pregnancies: int = Field(..., ge=0, le=20, description="Number of times pregnant")
    Glucose: float = Field(..., ge=0, le=300, description="Plasma glucose concentration (mg/dL)")
    BloodPressure: float = Field(..., ge=0, le=200, description="Diastolic blood pressure (mmHg)")
    SkinThickness: float = Field(..., ge=0, le=100, description="Triceps skin fold thickness (mm)")
    Insulin: float = Field(..., ge=0, le=900, description="2-Hour serum insulin (mu U/ml)")
    BMI: float = Field(..., ge=0, le=70, description="Body Mass Index (weight in kg/(height in m)^2)")
    DiabetesPedigreeFunction: float = Field(..., ge=0, le=3, description="Diabetes pedigree function score")
    Age: int = Field(..., ge=1, le=120, description="Age in years")

class HealthResponse(BaseModel):
    message: str
    model_loaded: bool
    scaler_loaded: bool

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="0 = No Diabetes, 1 = Diabetes")
    probability: float = Field(..., ge=0, le=1, description="Probability score from 0 to 1")
    predicted_outcome: str = Field(..., description="Human-readable prediction result")

@app.get("/", response_model=HealthResponse, tags=["Health"])
def root():
    """Health check endpoint"""
    return {
        "message": "Diabetes Prediction API is running 🚀",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
def predict(data: PatientData):
    """Make a diabetes prediction"""
    if model is None or scaler is None:
        raise HTTPException(
            status_code=503,
            detail="Model or scaler not loaded"
        )
    
    input_df = pd.DataFrame([data.dict()])
    cols = list(input_df.columns)
    input_df[cols] = scaler.transform(input_df[cols])
    
    # Get probability for class 1 (diabetes)
    probability = float(model.predict_proba(input_df)[0][1])
    prediction = 1 if probability >= 0.5 else 0
    
    return {
        "prediction": prediction,
        "probability": probability,
        "predicted_outcome": "Diabetes" if prediction == 1 else "No Diabetes"
    }
