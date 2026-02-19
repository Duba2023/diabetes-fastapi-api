from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
    title="Diabetes Prediction API",
    version="1.0"
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
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

@app.get("/")
def root():
    return {
        "message": "Diabetes Prediction API is running 🚀",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None
    }

@app.post("/predict")
def predict(data: PatientData):
    if model is None or scaler is None:
        return {
            "error": "Model or scaler not loaded",
            "model_loaded": model is not None,
            "scaler_loaded": scaler is not None
        }
    
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
