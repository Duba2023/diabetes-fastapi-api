from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

logger.info("=" * 80)
logger.info("DIABETES PREDICTION API - STARTUP")
logger.info("=" * 80)

app = FastAPI(
    title="Diabetes Prediction API",
    description="FastAPI backend for diabetes prediction using Random Forest",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model and scaler
model = None
scaler = None

def initialize_model():
    """Train model on startup"""
    global model, scaler
    
    logger.info("Initializing Random Forest model...")
    
    try:
        # Create training data (synthetic Pima Indian Diabetes-like data)
        np.random.seed(42)
        n_samples = 768
        
        X = np.random.rand(n_samples, 8) * [20, 200, 122, 99, 846, 67.1, 2.4, 81]
        y = np.random.randint(0, 2, n_samples)
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train Random Forest
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_scaled, y)
        
        logger.info("✓✓✓ MODEL TRAINED AND READY ✓✓✓")
        logger.info(f"Model type: {type(model).__name__}")
        logger.info(f"Scaler type: {type(scaler).__name__}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize model: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

# Initialize on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Diabetes Prediction API...")
    success = initialize_model()
    logger.info(f"Model ready: {success}")
    logger.info("API is ready to accept predictions! 🚀")

# API Models
class PatientData(BaseModel):
    Pregnancies: int = Field(..., ge=0, le=20, description="Number of times pregnant")
    Glucose: float = Field(..., ge=0, le=300, description="Plasma glucose concentration (mg/dL)")
    BloodPressure: float = Field(..., ge=0, le=200, description="Diastolic blood pressure (mmHg)")
    SkinThickness: float = Field(..., ge=0, le=100, description="Triceps skin fold thickness (mm)")
    Insulin: float = Field(..., ge=0, le=900, description="2-Hour serum insulin (mu U/ml)")
    BMI: float = Field(..., ge=0, le=70, description="Body Mass Index (weight in kg/(height in m)^2)")
    DiabetesPedigreeFunction: float = Field(..., ge=0, le=3, description="Diabetes pedigree function score")
    Age: int = Field(..., ge=1, le=120, description="Age in years")

class HealthResponse(BaseModel):
    message: str
    model_loaded: bool
    scaler_loaded: bool

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="0 = No Diabetes, 1 = Diabetes")
    probability: float = Field(..., ge=0, le=1, description="Probability score from 0 to 1")
    predicted_outcome: str = Field(..., description="Human-readable prediction result")

# Endpoints
@app.get("/", response_model=HealthResponse, tags=["Health"])
def root():
    """Health check endpoint"""
    return {
        "message": "Diabetes Prediction API is running 🚀",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
def predict(data: PatientData):
    """Make a diabetes prediction"""
    if model is None or scaler is None:
        raise HTTPException(
            status_code=503,
            detail="Model not initialized. Please try again in a moment."
        )
    
    try:
        # Convert input to numpy array
        input_array = np.array([[
            data.Pregnancies,
            data.Glucose,
            data.BloodPressure,
            data.SkinThickness,
            data.Insulin,
            data.BMI,
            data.DiabetesPedigreeFunction,
            data.Age
        ]])
        
        # Scale input
        input_scaled = scaler.transform(input_array)
        
        # Make prediction
        probability = float(model.predict_proba(input_scaled)[0][1])
        prediction = 1 if probability >= 0.5 else 0
        
        return {
            "prediction": prediction,
            "probability": probability,
            "predicted_outcome": "Diabetes" if prediction == 1 else "No Diabetes"
        }
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")
