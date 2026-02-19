from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
from scipy.stats import boxcox, yeojohnson
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Diabetes Prediction Deep Learning API",
    version="1.0.0",
    description="Deep Learning API for diabetes risk prediction using TensorFlow/Keras",
    contact={
        "name": "ZION TECH HUB",
        "url": "https://github.com/Duba2023/diabetes-fastapi-api",
    },
    license_info={
        "name": "MIT",
    },
)


# Allow Streamlit to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model & scaler once with error handling
model = None
scaler = None

try:
    logger.info("Loading TensorFlow model...")
    model = tf.keras.models.load_model("diabetes_model.h5")
    logger.info("✓ Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")

try:
    logger.info("Loading scaler...")
    scaler = joblib.load("scaler.joblib")
    logger.info("✓ Scaler loaded successfully")
except Exception as e:
    logger.error(f"Failed to load scaler: {e}")

class PatientData(BaseModel):
    Pregnancies: int = Field(..., ge=0, le=20, description="Number of times pregnant")
    Glucose: float = Field(..., ge=0, le=300, description="Plasma glucose concentration (mg/dL)")
    BloodPressure: float = Field(..., ge=0, le=200, description="Diastolic blood pressure (mmHg)")
    SkinThickness: float = Field(..., ge=0, le=100, description="Triceps skin fold thickness (mm)")
    Insulin: float = Field(..., ge=0, le=900, description="2-Hour serum insulin (mu U/ml)")
    BMI: float = Field(..., ge=0, le=70, description="Body Mass Index (weight in kg/(height in m)^2)")
    DiabetesPedigreeFunction: float = Field(..., ge=0, le=3, description="Diabetes pedigree function score")
    Age: int = Field(..., ge=1, le=120, description="Age in years")
    
    class Config:
        json_schema_extra = {
            "example": {
                "Pregnancies": 6,
                "Glucose": 148,
                "BloodPressure": 72,
                "SkinThickness": 35,
                "Insulin": 0,
                "BMI": 33.6,
                "DiabetesPedigreeFunction": 0.627,
                "Age": 50
            }
        }

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
    """Health check endpoint to verify API status"""
    return {
        "message": "Diabetes Prediction API is running 🚀",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
def predict(data: PatientData):
    """
    Make a diabetes prediction based on patient medical data.
    
    The model uses Deep Learning (TensorFlow/Keras) trained on patient data.
    Returns a probability score and binary prediction.
    """
    if model is None or scaler is None:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Model or scaler not loaded",
                "model_loaded": model is not None,
                "scaler_loaded": scaler is not None
            }
        )
    
    input_df = pd.DataFrame([data.dict()])

    # Simple scaling only (adjust if needed)
    cols = list(input_df.columns)
    input_df[cols] = scaler.transform(input_df[cols])

    prediction_prob = float(model.predict(input_df)[0][0])
    prediction = 1 if prediction_prob >= 0.5 else 0

    return {
        "prediction": prediction,
        "probability": prediction_prob,
        "predicted_outcome": "Diabetes" if prediction == 1 else "No Diabetes"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 50)
    logger.info("Diabetes Prediction API Starting Up")
    logger.info(f"Model Loaded: {model is not None}")
    logger.info(f"Scaler Loaded: {scaler is not None}")
    logger.info("=" * 50)
