# Use a lightweight Python image
FROM python:3.9-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (required for building some packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app + ML assets
COPY app.py .
COPY diabetes_model.h5 .
COPY scaler.joblib .

# Expose Render's default Streamlit port
EXPOSE 10000

# Command to run Streamlit in headless mode
CMD streamlit run app.py \
    --server.port=10000 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false
