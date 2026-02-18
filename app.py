import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
from scipy.stats import boxcox, yeojohnson

# ------------------------------
# Load model and scaler
# ------------------------------
@st.cache_resource
def load_model_and_scaler():
    model = tf.keras.models.load_model('diabetes_model.h5')
    scaler = joblib.load('scaler.joblib')
    return model, scaler

model, scaler = load_model_and_scaler()

# Hardcoded preprocessing parameters (from training)
MEDIANS = {'Insulin':125, 'SkinThickness':29, 'BMI':32, 'BloodPressure':72, 'Glucose':117}
LAMBDAS = {'Insulin':0.0639, 'DiabetesPedigreeFunction':-0.0731, 'Age':-1.0944, 'Pregnancies':0.1727, 'BloodPressure':0.8980}

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Diabetes Prediction App")
st.title("🩺 Diabetes Prediction App")

with st.sidebar:
    st.header("Patient Information")
    pregnancies = st.number_input("Pregnancies", 0, 20, 1)
    glucose = st.number_input("Glucose", 0, 300, 100)
    blood_pressure = st.number_input("Blood Pressure", 0, 200, 70)
    skin_thickness = st.number_input("Skin Thickness", 0, 100, 20)
    insulin = st.number_input("Insulin", 0, 900, 80)
    bmi = st.number_input("BMI", 0.0, 70.0, 25.0)
    dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.3)
    age = st.number_input("Age", 1, 120, 30)

# ------------------------------
# Prediction logic
# ------------------------------
if st.sidebar.button("Predict Diabetes"):
    input_df = pd.DataFrame([{
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': blood_pressure,
        'SkinThickness': skin_thickness,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': dpf,
        'Age': age
    }])

    # Missing indicators
    columns_to_process_zeros = ['Insulin','SkinThickness','BMI','BloodPressure','Glucose']
    for col in columns_to_process_zeros:
        input_df[f'{col}_Missing'] = (input_df[col]==0).astype(int)
        input_df[col] = input_df[col].replace(0, MEDIANS[col])

    # Transformations
    for col in ['Insulin','DiabetesPedigreeFunction','Age']:
        input_df[col] = boxcox(input_df[col], lmbda=LAMBDAS[col])
    for col in ['Pregnancies','BloodPressure']:
        input_df[col] = yeojohnson(input_df[col], lmbda=LAMBDAS[col])

    # Scale numerical columns
    cols_to_scale = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
    input_df[cols_to_scale] = scaler.transform(input_df[cols_to_scale])

    # Arrange columns
    feature_order = cols_to_scale + [f'{c}_Missing' for c in columns_to_process_zeros]
    input_df = input_df[feature_order]

    # Prediction
    pred_proba = model.predict(input_df)[0][0]
    pred_class = 1 if pred_proba >= 0.5 else 0

    # Display result
    if pred_class==1:
        st.error(f"⚠️ High Risk of Diabetes\nProbability: {pred_proba:.2f}")
    else:
        st.success(f"✅ Low Risk of Diabetes\nProbability: {pred_proba:.2f}")
