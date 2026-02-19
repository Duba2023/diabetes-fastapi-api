# Deploy Streamlit Frontend on Render

## 📍 Project Structure

Your ZTH project now has:
- `main.py` - FastAPI backend server
- `streamlit_app.py` - Streamlit frontend UI
- `Dockerfile` - Backend container (FastAPI)
- `Dockerfile.streamlit` - Frontend container (Streamlit)
- `streamlit_requirements.txt` - Streamlit dependencies

---

## 🚀 Deploy Streamlit on Render (5 Minutes)

### Step 1: Open Render Dashboard
```
https://dashboard.render.com
```

### Step 2: Click "New +" → "Web Service"

### Step 3: Connect Repository
1. Select your `diabetes-fastapi-api` repository
2. Branch: `main`

### Step 4: Configure Service

| Field | Value |
|-------|-------|
| **Name** | `diabetes-dl-streamlit-frontend` |
| **Environment** | `Docker` |
| **Dockerfile Path** | `./Dockerfile.streamlit` |
| **Build Command** | (leave empty) |
| **Start Command** | (leave empty) |

### Step 5: Add Environment Variable
Click "Advanced" → "Add Environment Variable"

```
Key:   API_URL
Value: https://diabetes-dl-api.onrender.com
```

### Step 6: Deploy!
Click **"Create Web Service"** 

**Wait 2-5 minutes for deployment...**

---

## ✅ After Deployment

Once it says **"Live"** in green, your frontend will be at:
```
https://diabetes-dl-streamlit-frontend.onrender.com
```

---

## 🧪 What You'll See

### Streamlit Interface:
- 🩺 **Title**: "Diabetes Prediction AI"
- **Sidebar**:
  - API connection status
  - Patient data input fields
  - Input validation
- **Main Area**:
  - 3 Tabs: Prediction, Summary, About
  - Beautiful results display
  - Risk level indicators
  - Recommendations

---

## 📊 Features

✅ Real-time API health check
✅ Patient data input with validation
✅ Beautiful prediction results
✅ Risk level indicators (HIGH/LOW)
✅ Confidence scores
✅ Detailed recommendations
✅ Summary table
✅ About section
✅ Responsive design

---

## 📋 Files Created

```
✅ streamlit_app.py           - Streamlit frontend application
✅ streamlit_requirements.txt  - Python dependencies
✅ Dockerfile.streamlit        - Container configuration
✅ render_streamlit.yaml       - Render deployment config
```

---

## 🔗 After Deployment URLs

| Service | URL |
|---------|-----|
| 🎨 **Streamlit Frontend** | `https://diabetes-dl-streamlit-frontend.onrender.com` |
| 📚 **API Swagger Docs** | `https://diabetes-dl-api.onrender.com/docs` |
| 🔌 **API Health** | `https://diabetes-dl-api.onrender.com/` |

---

## 🧪 Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r streamlit_requirements.txt

# Run Streamlit
streamlit run streamlit_app.py
```

Open: `http://localhost:8501`

---

## 🛠️ Configuration

### Environment Variables
- `API_URL` - Backend API URL (default: http://localhost:8000)

### Streamlit Config (.streamlit/config.toml)
Already configured in Dockerfile for:
- Headless mode
- Port 8501
- XSRF protection enabled

---

## 📞 Troubleshooting

### Frontend won't connect to API
✅ Check `API_URL` environment variable is set correctly
✅ Verify backend API is deployed and running
✅ Try accessing API directly in browser

### Build fails
✅ Check files are in root directory
✅ Verify `Dockerfile.streamlit` exists
✅ Check `streamlit_requirements.txt` has all dependencies

### Slow load/timeout
✅ Normal on free tier - first load takes 30+ seconds
✅ Subsequent requests are faster
✅ Consider upgrading for production

---

## ✨ Success Indicators

✅ Status shows **"Live"** (green)
✅ URL is accessible
✅ Streamlit app loads with title
✅ Sidebar loads with input fields
✅ API status check shows (green/yellow/red)
✅ Can enter patient data

---

## 🎯 Next Steps

1. ✅ Push code to GitHub (already done)
2. Go to https://dashboard.render.com
3. Create new Web Service
4. Select your repository
5. Configure with Dockerfile.streamlit
6. Add API_URL environment variable
7. Deploy!
8. Share the URL with others

---

**Status**: ✅ Ready for Render Deployment
