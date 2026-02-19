FROM python:3.9-slim

WORKDIR /app

# Update and install build dependencies
RUN apt-get update && apt-get install -y build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all necessary files with verbose output
COPY . .

# Debug: List files in container
RUN echo "=== Checking files in /app ===" && \
    ls -lah /app/ && \
    echo "=== Checking for model files ===" && \
    ls -lah /app/*.h5 2>/dev/null || echo "No .h5 files found" && \
    ls -lah /app/*.joblib 2>/dev/null || echo "No .joblib files found"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]


