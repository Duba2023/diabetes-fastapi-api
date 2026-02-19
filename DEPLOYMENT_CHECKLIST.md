# Deep Learning Model - Render Deployment Checklist

## ✅ Pre-Deployment Verification

### Files Required
- [x] `main.py` - FastAPI application
- [x] `diabetes_model.h5` - Trained TensorFlow model
- [x] `scaler.joblib` - Data scaler
- [x] `requirements.txt` - Python dependencies (pinned versions)
- [x] `Dockerfile` - Container configuration
- [x] `render.yaml` - Render deployment config

### Configuration
- [x] CORS middleware enabled for frontend integration
- [x] API running on port 8000
- [x] Health check endpoint: `GET /`
- [x] Prediction endpoint: `POST /predict`

### API Specs
**Input Model (PatientData):**
```json
{
  "Pregnancies": integer,
  "Glucose": float,
  "BloodPressure": float,
  "SkinThickness": float,
  "Insulin": float,
  "BMI": float,
  "DiabetesPedigreeFunction": float,
  "Age": integer
}
```

**Output Response:**
```json
{
  "prediction": 0 or 1,
  "probability": float,
  "predicted_outcome": "Diabetes" or "No Diabetes"
}
```

## 🚀 Deployment Steps

### Step 1: Push to GitHub
```bash
cd "c:\Users\DELL\OneDrive\Desktop\ZTH project"
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Connect to Render
1. Visit https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the ZTH project branch
5. Confirm settings and deploy

### Step 3: Monitor Deployment
- Check Render dashboard for deployment status
- View logs for any errors
- Wait for "Live" status (10-15 minutes)

### Step 4: Test API
```bash
curl -X GET "https://diabetes-dl-api.onrender.com/"
```

## 📋 Important Notes

- **Model Size**: TensorFlow models can be large (100MB+)
- **First Deploy**: May take 10-15 minutes due to dependencies
- **Free Tier Limits**: Render free tier has inactivity limits
- **Cold Start**: API may take 30s on first request after inactivity
- **GPU**: Not needed for inference; standard CPU is sufficient

## 🔗 After Deployment

Once deployed, use this URL in your Streamlit frontend:
```python
API_URL = "https://diabetes-dl-api.onrender.com"
```

## 📞 Support

For issues:
1. Check Render dashboard logs
2. Verify all required files are in repository
3. Ensure model file hasn't been corrupted
4. Check requirements.txt compatibility
