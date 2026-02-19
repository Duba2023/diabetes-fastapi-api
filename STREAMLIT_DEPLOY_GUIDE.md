# Deploy Streamlit Frontend on Render - Step by Step

## 📍 Location of Frontend Code
```
diabetes-dl-app/streamlit-frontend/
├── app.py
├── requirements.txt
├── Dockerfile
├── render.yaml
└── .streamlit/config.toml
```

---

## 🚀 Deployment Steps (5 Minutes)

### Step 1: Open Render Dashboard
Go to: **https://dashboard.render.com**

---

### Step 2: Create New Web Service
1. Click blue **"New +"** button (top right)
2. Select **"Web Service"**

---

### Step 3: Connect GitHub Repository
1. Where it says "Connect a repository", click **"Connect account"** (first time only)
2. Authorize GitHub
3. Search for: **`diabetes-fastapi-api`**
4. Select your repository
5. Click **"Connect"**

---

### Step 4: Configure the Service

Fill in these settings:

| Field | Value |
|-------|-------|
| **Name** | `diabetes-prediction-frontend` |
| **Environment** | `Docker` |
| **Branch** | `main` |
| **Root Directory** | `diabetes-dl-app/streamlit-frontend` |
| **Dockerfile Path** | `Dockerfile` |
| **Build Command** | (leave empty) |
| **Start Command** | (leave empty) |

---

### Step 5: Add Environment Variables

Click **"Advanced"** then **"Add Environment Variable"**

| Key | Value |
|-----|-------|
| `API_URL` | `https://diabetes-dl-api.onrender.com` |

---

### Step 6: Configure Free Tier (Optional)

- **Instance Type**: Free (if available)
- **Auto-Deploy**: Toggle ON

---

### Step 7: Deploy!

Click blue **"Create Web Service"** button

**Wait 2-5 minutes** for deployment to complete...

---

## ✅ After Deployment

Once it says **"Live"** in green:

Your Streamlit app will be available at:
```
https://diabetes-prediction-frontend-xxxx.onrender.com
```

(Replace xxxx with your auto-generated ID)

---

## 🧪 Test Your Frontend

1. Open the URL in browser
2. You should see:
   - 🩺 Title: "Diabetes Prediction Application"
   - Sidebar with patient data inputs
   - Green check: "✅ API is Connected" (if backend is reachable)
   - Or orange warning if backend models aren't loaded yet

---

## 📊 What You'll See

### Sidebar (Left):
- ⚙️ Configuration section
- API status check (green/red)
- Patient data input fields:
  - Pregnancies
  - Glucose
  - Blood Pressure
  - Skin Thickness
  - Insulin
  - BMI
  - Diabetes Pedigree Function
  - Age

### Main Area:
- Input summary table
- Quick links to API docs
- **"🔮 Predict Diabetes Risk"** button

---

## 🔧 If Deployment Fails

### Check These:

1. **Build Logs** (look for errors)
   - Click service
   - Click "Logs" tab
   - Scroll to top for build steps

2. **Common Issues**:
   - `requirements.txt not found` → Check file is in `diabetes-dl-app/streamlit-frontend/`
   - `Dockerfile not found` → Same check
   - `No module named streamlit` → Check requirements.txt has correct packages

---

## 📋 Checklist

Before deploying, verify:

- [x] Repository: `diabetes-fastapi-api` selected
- [x] Root Directory: `diabetes-dl-app/streamlit-frontend`
- [x] Environment Variable: `API_URL` set
- [x] Instance: Free or Paid (your choice)
- [x] All files exist in streamlit folder

---

## ⏱️ Timeline

| Step | Time |
|------|------|
| Create service | 1 min |
| Build Docker image | 2-3 min |
| Start Streamlit app | 1 min |
| **Total** | **4-5 minutes** |

---

## 🎯 Success Indicators

Once deployed, you should see:

✅ Status shows **"Live"** (green)
✅ URL is accessible
✅ Streamlit app loads with title
✅ No 404 errors
✅ Sidebar loads with input fields

---

## 📞 Need Help?

If deployment fails:
1. Check Render logs for exact error
2. Verify all files are in correct folder
3. Make sure GitHub repo is up to date

---

**Start now: https://dashboard.render.com** 🚀
