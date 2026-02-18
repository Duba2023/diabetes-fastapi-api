import streamlit as st
import requests

# 🔹 Replace with your actual FastAPI Render URL
API_URL = "https://your-fastapi-service.onrender.com/predict"

st.set_page_config(page_title="Diabetes Prediction System", layout="centered")

st.title("🩺 Diabetes Prediction App")
st.write("Enter the patient’s clinical details to predict diabetes risk.")

with st.sidebar:
    st.header("Input Patient Data")

    pregnancies = st.number_input("Pregnancies", 0, 20, 1)
    glucose = st.number_input("Glucose", 0, 200, 100)
    blood_pressure = st.number_input("Blood Pressure", 0, 122, 70)
    skin_thickness = st.number_input("Skin Thickness", 0, 99, 20)
    insulin = st.number_input("Insulin", 0, 846, 80)
    bmi = st.number_input("BMI", 0.0, 70.0, 25.0)
    diabetes_pedigree_function = st.number_input(
        "Diabetes Pedigree Function", 0.0, 2.5, 0.3, format="%.3f"
    )
    age = st.number_input("Age", 21, 100, 30)

if st.sidebar.button("Predict Diabetes"):

    payload = {
        "Pregnancies": pregnancies,
        "Glucose": glucose,
        "BloodPressure": blood_pressure,
        "SkinThickness": skin_thickness,
        "Insulin": insulin,
        "BMI": bmi,
        "DiabetesPedigreeFunction": diabetes_pedigree_function,
        "Age": age,
    }

    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()

        prediction = result["prediction"]
        probability = result["probability"]

        st.subheader("Prediction Result")

        if prediction == 1:
            st.error(
                f"⚠️ High Risk of Diabetes\n\nProbability: {probability:.2f}"
            )
        else:
            st.success(
                f"✅ Low Risk of Diabetes\n\nProbability: {probability:.2f}"
            )

    except Exception as e:
        st.error(f"API connection failed: {e}")
