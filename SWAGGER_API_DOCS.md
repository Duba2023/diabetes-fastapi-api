# Swagger UI API Documentation

## Overview

Your FastAPI backend includes automatic API documentation with Swagger UI and ReDoc. No additional setup needed!

---

## Accessing Swagger UI

### Swagger Interactive Documentation
```
https://diabetes-dl-api.onrender.com/docs
```

This provides:
- ✅ Interactive API endpoint testing
- ✅ Request/response examples
- ✅ Full field documentation
- ✅ Try it out button to test endpoints
- ✅ Beautiful UI

---

## Accessing ReDoc

### Alternative API Documentation
```
https://diabetes-dl-api.onrender.com/redoc
```

This provides:
- ✅ Clean, readable documentation
- ✅ Better for printing/reference
- ✅ Search functionality
- ✅ Complete schema documentation

---

## Available Endpoints

### 1. Health Check Endpoint

**GET** `/`

**Description**: Check if API is running and models are loaded

**Response**: 
```json
{
  "message": "Diabetes Prediction API is running 🚀",
  "model_loaded": true,
  "scaler_loaded": true
}
```

**Status Codes**:
- `200 OK` - API is healthy

---

### 2. Prediction Endpoint

**POST** `/predict`

**Description**: Make a diabetes risk prediction based on patient data

**Request Body**:
```json
{
  "Pregnancies": 6,
  "Glucose": 148,
  "BloodPressure": 72,
  "SkinThickness": 35,
  "Insulin": 0,
  "BMI": 33.6,
  "DiabetesPedigreeFunction": 0.627,
  "Age": 50
}
```

**Parameters**:

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| Pregnancies | integer | 0-20 | Number of times pregnant |
| Glucose | number | 0-300 | Plasma glucose concentration (mg/dL) |
| BloodPressure | number | 0-200 | Diastolic blood pressure (mmHg) |
| SkinThickness | number | 0-100 | Triceps skin fold thickness (mm) |
| Insulin | number | 0-900 | 2-Hour serum insulin (mu U/ml) |
| BMI | number | 0-70 | Body Mass Index (kg/m²) |
| DiabetesPedigreeFunction | number | 0-3 | Diabetes pedigree function score |
| Age | integer | 1-120 | Age in years |

**Response**:
```json
{
  "prediction": 1,
  "probability": 0.85,
  "predicted_outcome": "Diabetes"
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| prediction | integer | 0 = No Diabetes, 1 = Diabetes |
| probability | number | Probability score (0-1) |
| predicted_outcome | string | "Diabetes" or "No Diabetes" |

**Status Codes**:
- `200 OK` - Prediction successful
- `503 Service Unavailable` - Models not loaded

---

## How to Use Swagger UI

### Step 1: Open Swagger UI
Visit: `https://diabetes-dl-api.onrender.com/docs`

### Step 2: Find Endpoint
Click on the endpoint you want to test:
- GET `/` - Health check
- POST `/predict` - Make prediction

### Step 3: Click "Try it out"
Button appears on the right side of each endpoint

### Step 4: Enter Parameters
For POST `/predict`:
- Click the request field
- Enter patient data as JSON
- Click "Execute"

### Step 5: View Response
You'll see:
- Request sent
- Response status
- Response body (JSON)
- Response headers

---

## Example API Calls

### Using cURL

```bash
# Health check
curl -X GET "https://diabetes-dl-api.onrender.com/" \
  -H "Accept: application/json"

# Make prediction
curl -X POST "https://diabetes-dl-api.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Pregnancies": 6,
    "Glucose": 148,
    "BloodPressure": 72,
    "SkinThickness": 35,
    "Insulin": 0,
    "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627,
    "Age": 50
  }'
```

### Using Python Requests

```python
import requests

# Health check
response = requests.get("https://diabetes-dl-api.onrender.com/")
print(response.json())

# Make prediction
data = {
    "Pregnancies": 6,
    "Glucose": 148,
    "BloodPressure": 72,
    "SkinThickness": 35,
    "Insulin": 0,
    "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627,
    "Age": 50
}
response = requests.post("https://diabetes-dl-api.onrender.com/predict", json=data)
print(response.json())
```

### Using JavaScript/Fetch

```javascript
// Health check
fetch('https://diabetes-dl-api.onrender.com/')
  .then(response => response.json())
  .then(data => console.log(data));

// Make prediction
const patientData = {
  "Pregnancies": 6,
  "Glucose": 148,
  "BloodPressure": 72,
  "SkinThickness": 35,
  "Insulin": 0,
  "BMI": 33.6,
  "DiabetesPedigreeFunction": 0.627,
  "Age": 50
};

fetch('https://diabetes-dl-api.onrender.com/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(patientData)
})
.then(response => response.json())
.then(data => console.log(data));
```

### Using Streamlit (Frontend)

```python
import requests
import streamlit as st

API_URL = "https://diabetes-dl-api.onrender.com"

# Make prediction
response = requests.post(f"{API_URL}/predict", json={
    "Pregnancies": 6,
    "Glucose": 148,
    "BloodPressure": 72,
    "SkinThickness": 35,
    "Insulin": 0,
    "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627,
    "Age": 50
})

result = response.json()
st.write(result)
```

---

## Response Examples

### Successful Prediction (Low Risk)
```json
{
  "prediction": 0,
  "probability": 0.23,
  "predicted_outcome": "No Diabetes"
}
```

### Successful Prediction (High Risk)
```json
{
  "prediction": 1,
  "probability": 0.87,
  "predicted_outcome": "Diabetes"
}
```

### API Health Check
```json
{
  "message": "Diabetes Prediction API is running 🚀",
  "model_loaded": true,
  "scaler_loaded": true
}
```

### Error Response (Models Not Loaded)
```json
{
  "detail": {
    "error": "Model or scaler not loaded",
    "model_loaded": false,
    "scaler_loaded": false
  }
}
```

---

## API Features

### 1. Automatic Input Validation
- Type checking (numbers, integers)
- Range validation (0-20 for pregnancies, etc.)
- Clear error messages for invalid input

### 2. CORS Support
- Allow requests from any frontend
- Configured for Streamlit frontend

### 3. Health Checks
- Monitor if models are properly loaded
- Status endpoint for readiness checks

### 4. Error Handling
- Clear error messages
- HTTP status codes
- Detailed response bodies

### 5. Response Schemas
- Consistent response format
- Type-safe responses
- Examples included

---

## Rate Limiting

Currently no rate limiting is enforced. Production deployments should add:
- Per-IP rate limiting
- Authentication tokens
- Request throttling

---

## CORS Configuration

API allows requests from:
- All origins (`*`)
- All methods
- All headers

For production, restrict to:
```python
allow_origins=["https://diabetes-prediction-frontend.onrender.com"]
```

---

## Security Recommendations

1. **Add Authentication**
   - Use API keys
   - JWT tokens
   - OAuth2

2. **Rate Limiting**
   - Prevent abuse
   - Use middleware

3. **Input Validation**
   - Already implemented via Pydantic
   - Additional checks can be added

4. **HTTPS**
   - Already enforced on Render
   - All data encrypted

---

## Monitoring & Logging

### Check Logs
1. Go to Render dashboard
2. Click your service
3. View "Logs" tab
4. Look for request details

### Health Monitoring
Call health check endpoint periodically:
```bash
curl https://diabetes-dl-api.onrender.com/
```

---

## Troubleshooting

### Models Not Loaded
- Check backend is fully deployed
- Wait a few minutes for startup
- Check Render logs for errors

### Validation Errors
- Verify all fields are provided
- Check value ranges match documentation
- Ensure data types are correct (int vs float)

### CORS Errors
- Check API allows your origin
- Browser console will show error
- Verify API headers

---

## Next Steps

1. ✅ Open Swagger UI: `https://diabetes-dl-api.onrender.com/docs`
2. ✅ Test health endpoint
3. ✅ Test prediction endpoint with example data
4. ✅ View ReDoc docs: `https://diabetes-dl-api.onrender.com/redoc`
5. ✅ Integrate with frontend (Streamlit)

---

**API Status**: ✅ Ready for Production Use
