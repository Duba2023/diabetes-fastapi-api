from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import joblib
import tensorflow as tf
import numpy as np
import pandas as pd
from scipy.stats import boxcox, yeojohnson
from functools import lru_cache

# ------------------------------
# Initialize FastAPI
# ------------------------------
app = FastAPI(
    title="Pima Diabetes Prediction API",
    description="API for predicting diabetes based on health indicators",
    version="1.1.0"
)

@app.get("/")
def home():
    return {"message": "Diabetes Prediction API is running 🚀"}


# ------------------------------
# Pydantic Input Model
# ------------------------------
class DiabetesFeatures(BaseModel):
    Pregnancies: int = Field(..., ge=0, le=17)
    Glucose: float = Field(..., ge=0, le=199)
    BloodPressure: float = Field(..., ge=0, le=122)
    SkinThickness: float = Field(..., ge=0, le=99)
    Insulin: float = Field(..., ge=0, le=846)
    BMI: float = Field(..., ge=0.0, le=67.1)
    DiabetesPedigreeFunction: float = Field(..., ge=0.078, le=2.42)
    Age: int = Field(..., ge=21, le=81)


# ------------------------------
# Load Model and Scaler
# ------------------------------
@lru_cache()
def load_model():
    return tf.keras.models.load_model("diabetes_model.h5")


@lru_cache()
def load_scaler():
    return joblib.load("scaler.joblib")


# ------------------------------
# Hardcoded medians and lambdas from training
# ------------------------------
MEDIANS = {'Insulin':125,'SkinThickness':29,'BMI':32,'BloodPressure':72,'Glucose':117}
LAMBDAS = {'Insulin':0.0639,'DiabetesPedigreeFunction':-0.0731,'Age':-1.0944,'Pregnancies':0.1727,'BloodPressure':0.8980}


# ------------------------------
# Preprocessing function
# ------------------------------
def preprocess_input(input_data: DiabetesFeatures, scaler_obj):
    df = pd.DataFrame([input_data.dict()])
    processed = df.copy()

    zeros_cols = ['Insulin','SkinThickness','BMI','BloodPressure','Glucose']
    for col in zeros_cols:
        processed[f'{col}_Missing'] = (processed[col]==0).astype(int)
        processed[col] = processed[col].replace(0, np.nan).fillna(MEDIANS[col])

    # Transformations
    boxcox_cols = ['Insulin','DiabetesPedigreeFunction','Age']
    yeojohnson_cols = ['Pregnancies','BloodPressure']

    for col in boxcox_cols:
        processed[col] = boxcox(processed[col], lmbda=LAMBDAS[col])

    for col in yeojohnson_cols:
        processed[col] = yeojohnson(processed[col], lmbda=LAMBDAS[col])

    # Scaling
    scale_cols = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
    processed[scale_cols] = scaler_obj.transform(processed[scale_cols])

    # Ensure all feature columns exist
    feature_order = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI',
                     'DiabetesPedigreeFunction','Age','Insulin_Missing','SkinThickness_Missing',
                     'BMI_Missing','BloodPressure_Missing','Glucose_Missing']
    for col in zeros_cols:
        if f'{col}_Missing' not in processed.columns:
            processed[f'{col}_Missing'] = 0

    processed = processed[feature_order]
    return processed


# ------------------------------
# Prediction Endpoint
# ------------------------------
@app.post("/predict")
async def predict_diabetes(input_data: DiabetesFeatures,
                           model_obj: tf.keras.Model = Depends(load_model),
                           scaler_obj = Depends(load_scaler)):

    # Preprocess input
    processed_input = preprocess_input(input_data, scaler_obj)

    # Predict probability
    prediction_proba = float(model_obj.predict(processed_input)[0][0])
    binary_prediction = 1 if prediction_proba >= 0.5 else 0
    outcome_text = "Diabetes" if binary_prediction==1 else "No Diabetes"

    # Universal response (supports old frontend and descriptive keys)
    return {
        "prediction_probability": prediction_proba,  # descriptive key
        "predicted_outcome": outcome_text,          # descriptive key
        "probability": prediction_proba,            # old frontend key
        "prediction": binary_prediction             # old frontend key
    }
