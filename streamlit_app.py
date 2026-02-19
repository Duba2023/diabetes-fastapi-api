import streamlit as st
import requests
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #FF6B6B;
    }
    .metric-card {
        background-color: #fff;
        border-radius: 10px;
        padding: 20px;
        border: 2px solid #FF6B6B;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
API_PREDICT = f"{API_BASE_URL}/predict"
API_HEALTH = f"{API_BASE_URL}/"

# Main title
st.markdown('<h1 class="main-title">🩺 Diabetes Prediction AI</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar - API Status & Input
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info(f"🔗 API: {API_BASE_URL}")
    
    # Check API health
    try:
        health_response = requests.get(API_HEALTH, timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            if health_data.get("model_loaded") and health_data.get("scaler_loaded"):
                st.success("✅ API Connected & Ready")
            else:
                st.warning("⚠️ API Connected (Models Loading...)")
                st.warning(f"  Model: {health_data.get('model_loaded')}")
                st.warning(f"  Scaler: {health_data.get('scaler_loaded')}")
        else:
            st.error("❌ API Connection Error")
    except Exception as e:
        st.error(f"❌ Cannot Reach API")
        st.caption(f"Error: {str(e)}")
    
    st.divider()
    st.header("👤 Patient Data")
    
    # Create two columns for better organization
    col1, col2 = st.columns(2)
    
    with col1:
        pregnancies = st.number_input(
            "👶 Pregnancies",
            min_value=0,
            max_value=20,
            value=1,
            help="Number of times pregnant"
        )
        glucose = st.number_input(
            "🩸 Glucose (mg/dL)",
            min_value=0,
            max_value=300,
            value=100,
            help="Plasma glucose concentration"
        )
        blood_pressure = st.number_input(
            "💓 Blood Pressure (mmHg)",
            min_value=0,
            max_value=200,
            value=70,
            help="Diastolic blood pressure"
        )
        skin_thickness = st.number_input(
            "📏 Skin Thickness (mm)",
            min_value=0,
            max_value=100,
            value=20,
            help="Triceps skin fold thickness"
        )
    
    with col2:
        insulin = st.number_input(
            "💉 Insulin (mu U/ml)",
            min_value=0,
            max_value=900,
            value=80,
            help="2-Hour serum insulin"
        )
        bmi = st.number_input(
            "⚖️ BMI (kg/m²)",
            min_value=0.0,
            max_value=70.0,
            value=25.0,
            step=0.1,
            help="Body Mass Index"
        )
        dpf = st.number_input(
            "🧬 Diabetes Pedigree",
            min_value=0.0,
            max_value=3.0,
            value=0.3,
            step=0.01,
            help="Diabetes pedigree function"
        )
        age = st.number_input(
            "📅 Age (years)",
            min_value=1,
            max_value=120,
            value=30,
            help="Age in years"
        )

# Main content area
tab1, tab2, tab3 = st.tabs(["🔮 Prediction", "📊 Summary", "ℹ️ About"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Make a Prediction")
        
        if st.button("🔮 Predict Diabetes Risk", use_container_width=True, key="predict"):
            # Prepare data
            payload = {
                "Pregnancies": int(pregnancies),
                "Glucose": float(glucose),
                "BloodPressure": float(blood_pressure),
                "SkinThickness": float(skin_thickness),
                "Insulin": float(insulin),
                "BMI": float(bmi),
                "DiabetesPedigreeFunction": float(dpf),
                "Age": int(age)
            }
            
            with st.spinner("🔄 Analyzing patient data..."):
                try:
                    response = requests.post(API_PREDICT, json=payload, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display results
                        st.success("✅ Prediction Complete!")
                        st.markdown("---")
                        
                        # Results in metrics
                        res_col1, res_col2, res_col3 = st.columns(3)
                        
                        with res_col1:
                            prediction = result.get("prediction", 0)
                            risk_text = "🔴 HIGH RISK" if prediction == 1 else "🟢 LOW RISK"
                            st.metric("Risk Level", risk_text)
                        
                        with res_col2:
                            probability = result.get("probability", 0)
                            st.metric("Confidence", f"{probability:.1%}")
                        
                        with res_col3:
                            outcome = result.get("predicted_outcome", "Unknown")
                            st.metric("Outcome", outcome)
                        
                        st.markdown("---")
                        
                        # Detailed analysis
                        if prediction == 1:
                            st.error(f"""
                            ### ⚠️ High Diabetes Risk Detected
                            
                            **Probability: {probability:.1%}**
                            
                            This model predicts a **high risk of diabetes** based on the provided medical metrics.
                            
                            **Recommendations:**
                            - Consult with a healthcare professional
                            - Request additional diagnostic tests (A1C, fasting glucose)
                            - Consider lifestyle modifications
                            - Monitor blood glucose regularly
                            """)
                        else:
                            st.success(f"""
                            ### ✅ Low Diabetes Risk
                            
                            **Probability: {probability:.1%}**
                            
                            This model predicts a **low risk of diabetes** based on the provided medical metrics.
                            
                            **Recommendations:**
                            - Maintain current healthy lifestyle
                            - Continue regular health checkups
                            - Monitor diet and exercise habits
                            - Stay informed about diabetes prevention
                            """)
                        
                        # Expandable details
                        with st.expander("📋 Raw API Response"):
                            st.json(result)
                    
                    else:
                        st.error(f"❌ Prediction Failed (Status: {response.status_code})")
                        st.write(response.text)
                
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request Timeout - API took too long")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Cannot connect to API - Please check the API URL")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.info("""
        ### 📌 Quick Guide
        
        1. **Enter patient data** in the sidebar
        2. **Click predict button**
        3. **View results** with confidence score
        4. **Review recommendations**
        
        ---
        
        **Model**: Deep Learning (TensorFlow)
        **Input Features**: 8
        **Output**: Binary Classification
        """)

with tab2:
    st.subheader("Patient Data Summary")
    
    # Create a summary table
    summary_data = {
        "Metric": [
            "Pregnancies",
            "Glucose",
            "Blood Pressure",
            "Skin Thickness",
            "Insulin",
            "BMI",
            "Diabetes Pedigree Function",
            "Age"
        ],
        "Value": [
            f"{pregnancies}",
            f"{glucose} mg/dL",
            f"{blood_pressure} mmHg",
            f"{skin_thickness} mm",
            f"{insulin} mu U/ml",
            f"{bmi:.1f} kg/m²",
            f"{dpf:.3f}",
            f"{age} years"
        ],
        "Status": [
            "✅" if 0 <= pregnancies <= 20 else "⚠️",
            "✅" if 0 <= glucose <= 300 else "⚠️",
            "✅" if 0 <= blood_pressure <= 200 else "⚠️",
            "✅" if 0 <= skin_thickness <= 100 else "⚠️",
            "✅" if 0 <= insulin <= 900 else "⚠️",
            "✅" if 0 <= bmi <= 70 else "⚠️",
            "✅" if 0 <= dpf <= 3 else "⚠️",
            "✅" if 1 <= age <= 120 else "⚠️"
        ]
    }
    
    st.table(summary_data)
    
    st.markdown("---")
    st.subheader("📊 Data Ranges")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pregnancies Range", "0 - 20")
    with col2:
        st.metric("Glucose Range", "0 - 300")
    with col3:
        st.metric("BP Range", "0 - 200")
    with col4:
        st.metric("Age Range", "1 - 120")

with tab3:
    st.subheader("About This Application")
    
    st.markdown("""
    ### 🩺 Diabetes Prediction AI System
    
    This application uses a **Deep Learning Neural Network** trained on clinical diabetes data 
    to predict the risk of diabetes based on patient medical metrics.
    
    ---
    
    ### 📊 Model Architecture
    - **Type**: TensorFlow/Keras Neural Network
    - **Training Data**: Clinical patient records
    - **Input Features**: 8 medical measurements
    - **Output**: Binary classification (Diabetes / No Diabetes)
    
    ---
    
    ### 📋 Input Features
    
    1. **Pregnancies** - Number of times pregnant
    2. **Glucose** - Plasma glucose concentration (mg/dL)
    3. **Blood Pressure** - Diastolic blood pressure (mmHg)
    4. **Skin Thickness** - Triceps skin fold thickness (mm)
    5. **Insulin** - 2-Hour serum insulin (mu U/ml)
    6. **BMI** - Body Mass Index (weight in kg/(height in m)²)
    7. **Diabetes Pedigree Function** - Genetic predisposition score
    8. **Age** - Age in years
    
    ---
    
    ### ⚠️ Important Disclaimer
    
    **This application is for educational and research purposes only.**
    
    - Results should NOT be used for medical diagnosis
    - Always consult with qualified healthcare professionals
    - This model is a predictive tool, not a diagnostic tool
    - Individual results may vary based on many factors
    
    ---
    
    ### 🔗 API Documentation
    
    - **Swagger UI**: [API Docs](/docs)
    - **Backend**: Deployed on Render
    - **Frontend**: Streamlit
    
    ---
    
    ### 👨‍💻 Technology Stack
    
    - **Frontend**: Streamlit
    - **Backend**: FastAPI
    - **ML Model**: TensorFlow/Keras
    - **Data Processing**: Scikit-learn, Pandas
    - **Deployment**: Docker, Render
    
    ---
    
    **Last Updated**: {datetime.now().strftime("%B %d, %Y")}
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px;'>
    <small>🩺 Diabetes Prediction AI | Powered by Deep Learning | Built with Streamlit</small>
</div>
""", unsafe_allow_html=True)
