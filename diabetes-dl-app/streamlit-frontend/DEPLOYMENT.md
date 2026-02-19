# Deploy Streamlit Frontend on Render

## Option 1: Deploy as Separate Repository (Recommended)

### 1. Create New GitHub Repository
- Go to https://github.com/new
- Create repo: `diabetes-prediction-frontend`
- Clone it to your machine

### 2. Copy Frontend Files
```powershell
# Copy the frontend folder contents
Copy-Item "c:\Users\DELL\OneDrive\Desktop\ZTH project\diabetes-dl-app\streamlit-frontend\*" -Destination "<path-to-frontend-repo>" -Recurse
```

### 3. Push to GitHub
```powershell
cd <path-to-frontend-repo>
git add .
git commit -m "Initial Streamlit frontend"
git push origin main
```

### 4. Deploy on Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select `diabetes-prediction-frontend` repository
5. Configure:
   - **Name**: `diabetes-prediction-frontend`
   - **Environment**: Docker
   - **Build Command**: (leave empty)
   - **Start Command**: (leave empty - uses Dockerfile)
   - **Environment Variables**:
     - `API_URL`: `https://diabetes-dl-api.onrender.com/predict`

6. Click Deploy

---

## Option 2: Push Everything to Same Repository

If you want to keep frontend and backend in same repo:

### 1. Push Frontend + Backend Together
```powershell
cd "c:\Users\DELL\OneDrive\Desktop\ZTH project"
git add .
git commit -m "Add Streamlit frontend"
git push origin main
```

### 2. Deploy Frontend on Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Select your **ZTH project** repository
4. Configure:
   - **Name**: `diabetes-prediction-frontend`
   - **Environment**: Docker
   - **Dockerfile Path**: `diabetes-dl-app/streamlit-frontend/Dockerfile`
   - **Root Directory**: `diabetes-dl-app/streamlit-frontend`
   - **Port**: 8501 (Streamlit default)
   - **Environment Variables**:
     - `API_URL`: `https://diabetes-dl-api.onrender.com/predict`

---

## Testing Frontend Locally

Before deploying, test it locally:

```powershell
cd "c:\Users\DELL\OneDrive\Desktop\ZTH project\diabetes-dl-app\streamlit-frontend"

# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run app.py
```

Open http://localhost:8501 and test the prediction form.

---

## Expected Result

Once deployed, your app will be at:
```
https://diabetes-prediction-frontend.onrender.com
```

You'll see:
- 🩺 Diabetes Prediction App title
- Sidebar with patient data inputs
- Predict button
- Results showing risk level and probability

---

## Next Steps

1. Choose Option 1 or Option 2
2. Push code to GitHub
3. Deploy on Render
4. Test the full application
5. Fix model loading issue on backend
