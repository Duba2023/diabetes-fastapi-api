from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
from scipy.stats import boxcox, yeojohnson

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

# Load model & scaler once
model = tf.keras.models.load_model("diabetes_model.h5")
scaler = joblib.load("scaler.joblib")

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
    return {"message": "Diabetes Prediction API is running 🚀"}

@app.post("/predict")
def predict(data: PatientData):

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
