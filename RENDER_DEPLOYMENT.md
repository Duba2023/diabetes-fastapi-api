# Diabetes Deep Learning Model - Render Deployment Guide

## Deployment Steps

### 1. Prerequisites
- GitHub account with your repository pushed (ZTH project folder)
- Render account (sign up at: https://render.com)

### 2. Connect Repository to Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Select "Build and deploy from a Git repository"
4. Connect your GitHub account
5. Select the repository containing ZTH project

### 3. Configure the Service
- **Name**: `diabetes-dl-api`
- **Environment**: `Docker`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)

### 4. Deploy
The `render.yaml` configuration will automatically deploy using:
- Docker image from provided `Dockerfile`
- Python 3.9-slim base image
- Port 8000 for the FastAPI server

### 5. Environment Variables (if needed)
If you need to add environment variables in Render dashboard:
- Go to your service
- Click "Environment"
- Add any required env vars

### 6. Access Your API
Once deployed, your API will be available at:
```
https://diabetes-dl-api.onrender.com
```

### API Endpoints
- `GET /` - Health check
- `POST /predict` - Make predictions

### Example Request
```bash
curl -X POST "https://diabetes-dl-api.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Pregnancies": 1,
    "Glucose": 148,
    "BloodPressure": 72,
    "SkinThickness": 35,
    "Insulin": 0,
    "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627,
    "Age": 50
  }'
```

### Troubleshooting

**Build fails:**
- Ensure all files (main.py, diabetes_model.h5, scaler.joblib) are in repository
- Check requirements.txt has correct dependencies
- Verify Dockerfile paths match your file structure

**Model loading fails:**
- Ensure model file is not in .gitignore
- Check file paths in main.py match Dockerfile COPY commands

**Slow deploys:**
- Deep learning models are large (~1GB+)
- Initial deploy may take 10-15 minutes
- Subsequent deploys are faster due to caching

## Notes
- The API includes CORS middleware for frontend integration
- Model is loaded once at startup for performance
- Authentication: Currently open to all (add auth if needed)

## Next Steps
1. Push this folder to GitHub
2. Connect to Render using steps above
3. Monitor deployment in Render dashboard
4. Share the API URL with your Streamlit frontend
