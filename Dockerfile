FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements first (for Docker layer caching)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy main application file
COPY main.py .

# Copy model and scaler files EXPLICITLY
COPY diabetes_model.h5 .
COPY scaler.joblib .

# Verify files exist in container
RUN echo "=== Build Complete ===" && \
    echo "Current directory: $(pwd)" && \
    echo "Files in /app:" && \
    ls -lah /app/ && \
    echo "" && \
    echo "Checking for model files:" && \
    if [ -f /app/diabetes_model.h5 ]; then echo "✓ diabetes_model.h5 found"; else echo "✗ diabetes_model.h5 NOT found"; fi && \
    if [ -f /app/scaler.joblib ]; then echo "✓ scaler.joblib found"; else echo "✗ scaler.joblib NOT found"; fi

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run FastAPI application with detailed logging
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]



