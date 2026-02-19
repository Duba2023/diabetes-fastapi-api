import streamlit as st
import requests
import os
import json

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Use environment variable or default to Render deployment URL
API_URL = os.getenv("API_URL", "https://diabetes-dl-api.onrender.com")
PREDICT_ENDPOINT = f"{API_URL}/predict"
HEALTH_ENDPOINT = f"{API_URL}/"

# Sidebar - API Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info(f"🔗 API Endpoint: {API_URL}")
    
    # Check API Health
    try:
        health_response = requests.get(HEALTH_ENDPOINT, timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            st.success("✅ API is Connected")
            if health_data.get("model_loaded") and health_data.get("scaler_loaded"):
                st.success("✅ Models Loaded")
            else:
                st.warning("⚠️ Models Not Loaded")
                st.warning(f"Model: {health_data.get('model_loaded')}")
                st.warning(f"Scaler: {health_data.get('scaler_loaded')}")
        else:
            st.error("❌ API Connection Failed")
    except Exception as e:
        st.error(f"❌ Cannot Connect to API: {str(e)}")
    
    st.divider()
    st.header("📊 Patient Information")
    
    # Organize inputs in columns for better UX
    col1, col2 = st.columns(2)
    
    with col1:
        pregnancies = st.number_input("👶 Pregnancies", 0, 20, 1, help="Number of pregnancies")
        glucose = st.number_input("🩸 Glucose (mg/dL)", 0, 300, 100, help="Plasma glucose concentration")
        blood_pressure = st.number_input("💓 Blood Pressure (mmHg)", 0, 200, 70)
        skin_thickness = st.number_input("📏 Skin Thickness (mm)", 0, 100, 20)
    
    with col2:
        insulin = st.number_input("💉 Insulin (mu U/ml)", 0, 900, 80)
        bmi = st.number_input("⚖️ BMI (kg/m²)", 0.0, 70.0, 25.0)
        dpf = st.number_input("🧬 Diabetes Pedigree Function", 0.0, 3.0, 0.3, step=0.01)
        age = st.number_input("📅 Age (years)", 1, 120, 30)

# Main content
st.title("🩺 Diabetes Prediction Application")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Patient Data Summary
    This application uses a Deep Learning model to predict Diabetes risk based on medical metrics.
    """)
    
    # Display a nice summary table
    st.subheader("📋 Input Summary")
    summary_data = {
        "Metric": ["Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", 
                   "Insulin", "BMI", "Diabetes Pedigree Function", "Age"],
        "Value": [pregnancies, glucose, blood_pressure, skin_thickness, 
                  insulin, bmi, f"{dpf:.3f}", age]
    }
    st.table(summary_data)

with col2:
    st.subheader("🔗 Quick Links")
    st.markdown("""
    - [📖 API Documentation](https://diabetes-dl-api.onrender.com/docs)
    - [🔄 Alternative API Docs](https://diabetes-dl-api.onrender.com/redoc)
    """)

st.markdown("---")

# Prediction button
if st.button("🔮 Predict Diabetes Risk", key="predict_btn", use_container_width=True):
    
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
    
    with st.spinner("🔄 Analyzing patient data..."):
        try:
            response = requests.post(PREDICT_ENDPOINT, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Display results
                st.markdown("---")
                st.subheader("🎯 Prediction Results")
                
                res_col1, res_col2, res_col3 = st.columns(3)
                
                with res_col1:
                    risk_level = "HIGH RISK ⚠️" if result.get("prediction") == 1 else "LOW RISK ✅"
                    st.metric("Risk Level", risk_level)
                
                with res_col2:
                    probability = result.get("probability", 0)
                    st.metric("Confidence Score", f"{probability:.2%}")
                
                with res_col3:
                    outcome = result.get("predicted_outcome", "Unknown")
                    st.metric("Prediction", outcome)
                
                # Display detailed results
                st.markdown("---")
                st.subheader("📊 Detailed Analysis")
                
                if result.get("prediction") == 1:
                    st.error(f"""
                    ### ⚠️ High Diabetes Risk Detected
                    
                    **Probability:** {probability:.2%}
                    
                    **Recommendation:** Please consult with a healthcare professional for further evaluation 
                    and possible diagnostic tests (A1C, fasting glucose, etc.).
                    """)
                else:
                    st.success(f"""
                    ### ✅ Low Diabetes Risk
                    
                    **Probability:** {probability:.2%}
                    
                    **Recommendation:** Maintain current lifestyle and continue regular health checkups.
                    """)
                
                # Show raw API response for debugging
                with st.expander("📋 API Response (Raw JSON)"):
                    st.json(result)
                    
            elif response.status_code == 500:
                st.error("❌ Prediction Failed")
                st.error(f"**Error Details:**\n{response.text}")
                with st.expander("Show Full Error"):
                    st.code(response.text, language="json")
            else:
                st.error(f"❌ API Error: {response.status_code}")
                st.write(response.text)
                
        except requests.exceptions.Timeout:
            st.error("⏱️ Request Timeout - API took too long to respond")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to API - Please check the API URL")
        except Exception as e:
            st.error(f"❌ Unexpected Error: {str(e)}")

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>🩺 Diabetes Prediction API | Powered by Deep Learning</small>
</div>
""", unsafe_allow_html=True)
