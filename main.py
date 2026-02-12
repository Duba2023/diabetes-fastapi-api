
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import joblib
import tensorflow as tf
import numpy as np
import pandas as pd
from scipy.stats import boxcox, yeojohnson
from functools import lru_cache

# Initialize FastAPI app
app = FastAPI(
    title="Pima Diabetes Prediction API",
    description="API for predicting diabetes based on health indicators",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Diabetes Prediction API is running 🚀"}

# Pydantic Input Model
class DiabetesFeatures(BaseModel):
    Pregnancies: int = Field(..., ge=0, le=17, description="Number of times pregnant")
    Glucose: float = Field(..., ge=0, le=199, description="Plasma glucose concentration a 2 hours in an oral glucose tolerance test")
    BloodPressure: float = Field(..., ge=0, le=122, description="Diastolic blood pressure (mmHg)")
    SkinThickness: float = Field(..., ge=0, le=99, description="Triceps skin fold thickness (mm)")
    Insulin: float = Field(..., ge=0, le=846, description="2-Hour serum insulin (mu U/ml)")
    BMI: float = Field(..., ge=0.0, le=67.1, description="Body mass index (weight in kg/(height in m)^2)")
    DiabetesPedigreeFunction: float = Field(..., ge=0.078, le=2.42, description="Diabetes pedigree function")
    Age: int = Field(..., ge=21, le=81, description="Age in years")

# Load Assets (Model and Scaler)
@lru_cache()
def load_model():
    model = tf.keras.models.load_model('diabetes_model.h5')
    return model

@lru_cache()
def load_scaler():
    scaler = joblib.load('scaler.joblib')
    return scaler

# Hardcoded parameters from training notebook for consistency
MEDIANS = {
    'Insulin': 125.0,
    'SkinThickness': 29.0,
    'BMI': 32.0,
    'BloodPressure': 72.0,
    'Glucose': 117.0
}

LAMBDAS = {
    'Insulin': 0.0639,
    'DiabetesPedigreeFunction': -0.0731,
    'Age': -1.0944,
    'Pregnancies': 0.1727,
    'BloodPressure': 0.8980
}

# Preprocessing function (mimics training notebook steps)
def preprocess_input(input_data: DiabetesFeatures, scaler_obj):
    input_df = pd.DataFrame([input_data.dict()])
    processed_df = input_df.copy()

    columns_to_process_zeros = ['Insulin', 'SkinThickness', 'BMI', 'BloodPressure', 'Glucose']
    for col in columns_to_process_zeros:
        processed_df[f'{col}_Missing'] = (processed_df[col] == 0).astype(int)
        processed_df[col] = processed_df[col].replace(0, np.nan)
        processed_df[col].fillna(MEDIANS[col], inplace=True)

    columns_for_boxcox = ['Insulin', 'DiabetesPedigreeFunction', 'Age']
    columns_for_yeojohnson = ['Pregnancies', 'BloodPressure']

    for col in columns_for_boxcox:
        processed_df[col] = boxcox(processed_df[col], lmbda=LAMBDAS[col])

    for col in columns_for_yeojohnson:
        processed_df[col] = yeojohnson(processed_df[col], lmbda=LAMBDAS[col])

    columns_to_scale = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
        'BMI', 'DiabetesPedigreeFunction', 'Age'
    ]
    processed_df[columns_to_scale] = scaler_obj.transform(processed_df[columns_to_scale])

    feature_columns_order = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI',
        'DiabetesPedigreeFunction', 'Age', 'Insulin_Missing', 'SkinThickness_Missing',
        'BMI_Missing', 'BloodPressure_Missing', 'Glucose_Missing'
    ]
    
    for col in columns_to_process_zeros:
        if f'{col}_Missing' not in processed_df.columns:
            processed_df[f'{col}_Missing'] = 0

    processed_df = processed_df[feature_columns_order]

    return processed_df

@app.post("/predict")
async def predict_diabetes(input_data: DiabetesFeatures, model_obj: tf.keras.Model = Depends(load_model), scaler_obj = Depends(load_scaler)):
    processed_input = preprocess_input(input_data, scaler_obj)
    prediction_proba = model_obj.predict(processed_input)[0][0]
    binary_prediction = 1 if prediction_proba >= 0.5 else 0
    outcome_text = "Diabetes" if binary_prediction == 1 else "No Diabetes"

    return {
        "prediction_probability": float(prediction_proba),
        "predicted_outcome": outcome_text
    }
