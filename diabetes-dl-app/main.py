from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib

app = FastAPI(
    title="Diabetes Prediction API",
    version="1.0"
)

# Allow external frontend (e.g., Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Load model and scaler once
# -----------------------------
try:
    model = tf.keras.models.load_model("diabetes_model.h5")
    scaler = joblib.load("scaler.joblib")
except Exception as e:
    raise RuntimeError(f"Error loading model or scaler: {e}")

# -----------------------------
# Define Expected Feature Order
# MUST MATCH TRAINING ORDER
# -----------------------------
FEATURE_ORDER = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Insulin_Missing",
    "SkinThickness_Missing",
    "BMI_Missing",
    "BloodPressure_Missing",
    "Glucose_Missing"
]

# Clinical features (scaled) and missing indicators (not scaled)
CLINICAL_FEATURES = FEATURE_ORDER[:8]
MISSING_FEATURES = FEATURE_ORDER[8:]

# -----------------------------
# Input Schema
# -----------------------------
class PatientData(BaseModel):
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int
    Insulin_Missing: int
    SkinThickness_Missing: int
    BMI_Missing: int
    BloodPressure_Missing: int
    Glucose_Missing: int


@app.get("/")
def root():
    return {"message": "Diabetes Prediction API is running 🚀"}


@app.post("/predict")
def predict(data: PatientData):

    try:
        input_dict = data.dict()
        input_df = pd.DataFrame([input_dict])

        # Scale only clinical features
        scaled_clinical = scaler.transform(input_df[CLINICAL_FEATURES])

        # Keep missing indicators as-is
        missing_values = input_df[MISSING_FEATURES].values

        # Combine scaled clinical + missing indicators
        final_input = np.hstack([scaled_clinical, missing_values]).astype(np.float32)

        # Predict
        prediction_prob = float(model.predict(final_input, verbose=0)[0][0])
        prediction = 1 if prediction_prob >= 0.5 else 0

        return {
            "prediction": prediction,
            "probability": round(prediction_prob, 4),
            "predicted_outcome": "Diabetes" if prediction == 1 else "No Diabetes"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
