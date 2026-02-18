import streamlit as st
import requests

# 🔹 Replace with your actual FastAPI Render URL
API_URL = "https://diabetes-fastapi-api.onrender.com/predict"


st.set_page_config(page_title="Diabetes Prediction System", layout="centered")
st.title("🩺 Diabetes Prediction App")
st.write("Enter patient clinical details to assess diabetes risk.")

# Sidebar inputs
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

    try:
        response = requests.post(API_URL, json=payload, timeout=30)

        st.write("API Status Code:", response.status_code)
        st.write("API Raw Response:", response.text)

        if response.status_code != 200:
            st.error(f"API returned an error (status code {response.status_code}).")
        else:
            try:
                result = response.json()

                probability = result.get("prediction_probability")
                outcome_text = result.get("predicted_outcome")

                st.subheader("Prediction Result")
                if outcome_text == "Diabetes":
                    st.error(f"⚠️ High Risk of Diabetes\nProbability: {probability:.2f}")
                elif outcome_text == "No Diabetes":
                    st.success(f"✅ Low Risk of Diabetes\nProbability: {probability:.2f}")
                else:
                    st.warning("⚠️ Unexpected outcome received from API.")

            except ValueError:
                st.error("API did not return valid JSON.")
                st.write("Raw Response:", response.text)

    except requests.exceptions.RequestException as e:
        st.error("Failed to connect to FastAPI service.")
        st.write(str(e))
