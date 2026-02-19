# Streamlit Frontend - Comprehensive Deployment Guide

## Project Overview

This is a containerized Streamlit application that serves as the frontend for the Diabetes Prediction Deep Learning API.

### Key Features:
- 🎨 Modern, responsive UI with real-time API health checks
- 📊 Beautiful data visualization and prediction results display
- 🔗 Integrated API connectivity with comprehensive error handling
- 📱 Mobile-friendly design
- 🔄 Loading states and improved user experience
- 🔐 CORS-enabled for secure API communication

---

## Local Development

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Git

### 1. Install Dependencies
```bash
cd diabetes-dl-app/streamlit-frontend
pip install -r requirements.txt
```

### 2. Set Environment Variables (Optional)
```powershell
# Windows PowerShell
$env:API_URL = "http://localhost:8000"

# Linux/Mac
export API_URL="http://localhost:8000"
```

### 3. Run Application Locally
```bash
streamlit run app.py
```

App will be available at: `http://localhost:8501`

---

## Deployment on Render (Recommended)

### Option 1: Deploy from Existing ZTH Project Repository

This is the simplest approach - deploy directly from your existing GitHub repo.

#### Step 1: Ensure Code is Pushed
```powershell
cd "c:\Users\DELL\OneDrive\Desktop\ZTH project"
git add .
git commit -m "Improve: Enhanced Streamlit frontend with better UX and Swagger API docs"
git push origin main
```

#### Step 2: Create Render Web Service
1. Go to https://dashboard.render.com
2. Click **"New +" → "Web Service"**
3. Select your **ZTH project** repository
4. Configure with these settings:
   - **Name**: `diabetes-prediction-frontend`
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Dockerfile Path**: `diabetes-dl-app/streamlit-frontend/Dockerfile`
   - **Build Command**: (leave empty)
   - **Start Command**: (leave empty - Dockerfile handles it)

#### Step 3: Set Environment Variables
1. Scroll to **Environment** section
2. Click **"Add Environment Variable"**
3. Add:
   - **Key**: `API_URL`
   - **Value**: `https://diabetes-dl-api.onrender.com`

#### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait for deployment to complete (2-5 minutes)
3. Once "Live", access at: `https://diabetes-prediction-frontend.onrender.com`

---

### Option 2: Deploy as Separate Repository

If you prefer to keep frontend and backend in separate repositories:

#### Step 1: Create New GitHub Repository
- Go to https://github.com/new
- Repository name: `diabetes-prediction-frontend`
- Create repository

#### Step 2: Clone and Copy Files
```powershell
# Clone the new repository
git clone https://github.com/YOUR_USERNAME/diabetes-prediction-frontend.git
cd diabetes-prediction-frontend

# Copy all Streamlit frontend files
Copy-Item "c:\Users\DELL\OneDrive\Desktop\ZTH project\diabetes-dl-app\streamlit-frontend\*" -Destination . -Recurse -Force
```

#### Step 3: Push to GitHub
```powershell
git add .
git commit -m "Initial commit: Streamlit frontend"
git push origin main
```

#### Step 4: Deploy on Render
1. Go to https://dashboard.render.com
2. Click **"New +" → "Web Service"**
3. Connect GitHub and select `diabetes-prediction-frontend` repo
4. Configure:
   - **Name**: `diabetes-prediction-frontend`
   - **Environment**: `Docker`
   - **Root Directory**: `./`
5. Add environment variable:
   - `API_URL` = `https://diabetes-dl-api.onrender.com`
6. Click **"Create Web Service"**

---

## Deployment Verification Checklist

Before deploying, verify these files exist:

- [ ] `app.py` - Main Streamlit application
- [ ] `requirements.txt` - Python dependencies (streamlit, requests, pandas, numpy)
- [ ] `Dockerfile` - Container configuration
- [ ] `.streamlit/config.toml` - Streamlit configuration
- [ ] `render.yaml` - Render deployment config (optional)

---

## Access Your Application

### After Successful Deployment

**Streamlit Frontend**:
```
https://diabetes-prediction-frontend.onrender.com
```

**API Swagger Documentation**:
```
https://diabetes-dl-api.onrender.com/docs
```

**API Alternative Documentation (ReDoc)**:
```
https://diabetes-dl-api.onrender.com/redoc
```

---

## Application Features

### Frontend Interface

The Streamlit app provides:

1. **Header**: 🩺 Diabetes Prediction Application
2. **Sidebar Configuration**:
   - API health check with real-time status
   - All patient data inputs organized in columns
   - Helpful descriptions for each field

3. **Input Fields**:
   - Pregnancies (0-20
   - Glucose (0-300 mg/dL)
   - Blood Pressure (0-200 mmHg)
   - Skin Thickness (0-100 mm)
   - Insulin (0-900 mu U/ml)
   - BMI (0.0-70.0 kg/m²)
   - Diabetes Pedigree Function (0.0-3.0)
   - Age (1-120 years)

4. **Results Display**:
   - Risk Level (HIGH/LOW)
   - Confidence Score (0-100%)
   - Prediction Outcome (Diabetes/No Diabetes)
   - Detailed analysis with recommendations
   - Raw API response (expandable)

5. **Error Handling**:
   - Connection errors
   - Timeout handling
   - API errors with detailed messages
   - Model loading status indicators

---

## API Endpoints (Swagger UI)

The backend API provides two main endpoints:

### 1. Health Check
```
GET /
```
Status: Model and scaler loaded?

### 2. Prediction
```
POST /predict
```
Input: Patient data (JSON)
Output: Prediction, probability, outcome

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_URL` | `https://diabetes-dl-api.onrender.com` | Backend API base URL |

---

## Troubleshooting

### Issue: "Cannot Connect to API"
**Solution**: 
- Verify `API_URL` is correct in Render environment
- Check that backend API is deployed and running
- Try accessing the API directly in browser

### Issue: "Models Not Loaded" Warning
**Solution**:
- This appears when backend models haven't finished loading
- Give the backend a few minutes to initialize
- Check backend logs in Render dashboard

### Issue: Slow First Load
**Solution**:
- Normal for Render free tier
- First request can take 30+ seconds
- Subsequent requests are faster
- Consider upgrading to paid tier for better performance

### Issue: Prediction Returns Error
**Solution**:
- Verify all input fields have valid values
- Check API logs in Render dashboard
- Ensure backend model is actually loaded

### Issue: "Port Already in Use" (Local Only)
**Solution**:
```bash
streamlit run app.py --server.port 8502
```

---

## Performance Optimization

1. **Streamlit Caching**: Automatically caches function results
2. **Lazy Loading**: Models load once at startup
3. **Connection Pooling**: Reuses HTTP connections
4. **Response Timeout**: Set to 30 seconds

---

## Production Recommendations

- [ ] Use strong authentication if needed
- [ ] Monitor API response times
- [ ] Set up error logging and alerts
- [ ] Test with real patient data
- [ ] Validate predictions with medical professionals
- [ ] Consider upgrading from free tier for production use

---

## File Structure

```
diabetes-dl-app/streamlit-frontend/
├── app.py                      # Main Streamlit application (improved UI)
├── requirements.txt            # Dependencies
├── Dockerfile                  # Container configuration
├── render.yaml                 # Render deployment config
├── DEPLOYMENT.md              # This guide
└── .streamlit/
    └── config.toml            # Streamlit settings
```

---

## Quick Start Summary

```powershell
# 1. Push code to GitHub
cd "c:\Users\DELL\OneDrive\Desktop\ZTH project"
git add .
git commit -m "Deploy Streamlit frontend"
git push origin main

# 2. Go to Render dashboard: https://dashboard.render.com
# 3. Create new Web Service
# 4. Select ZTH project repository
# 5. Set Dockerfile Path: diabetes-dl-app/streamlit-frontend/Dockerfile
# 6. Add API_URL environment variable
# 7. Deploy!
```

---

## Success Indicators

Once deployed, you should see:
- ✅ Streamlit app loading at https://diabetes-prediction-frontend.onrender.com
- ✅ Green health check showing "API is Connected"
- ✅ No console errors in browser
- ✅ Can enter patient data and get predictions
- ✅ API Swagger docs accessible at /docs endpoint

---

## Support Resources

- **Streamlit**: https://docs.streamlit.io
- **Render**: https://render.com/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **Docker**: https://docs.docker.com

---

**Status**: ✅ Ready for Production Deployment

