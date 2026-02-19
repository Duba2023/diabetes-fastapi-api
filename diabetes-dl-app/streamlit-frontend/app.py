import streamlit as st
import requests

API_URL = "https://diabetes-fastapi-api.onrender.com/predict"

st.title("🩺 Diabetes Prediction App")

with st.sidebar:
    pregnancies = st.number_input("Pregnancies", 0, 20, 1)
    glucose = st.number_input("Glucose", 0, 300, 100)
    blood_pressure = st.number_input("Blood Pressure", 0, 200, 70)
    skin_thickness = st.number_input("Skin Thickness", 0, 100, 20)
    insulin = st.number_input("Insulin", 0, 900, 80)
    bmi = st.number_input("BMI", 0.0, 70.0, 25.0)
    dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.3)
    age = st.number_input("Age", 1, 120, 30)

if st.sidebar.button("Predict Diabetes"):

    payload = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": dpf,
        "Age": age
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        if result["prediction"] == 1:
            st.error(f"⚠️ High Risk of Diabetes\nProbability: {result['probability']:.2f}")
        else:
            st.success(f"✅ Low Risk of Diabetes\nProbability: {result['probability']:.2f}")
    else:
        st.error(f"API Error: {response.status_code}")
        st.write(response.text)
