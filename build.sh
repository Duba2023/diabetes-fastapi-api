#!/bin/bash

# Build script for Render
echo "Starting Render build process..."

# List files in current directory
echo "Files in current directory:"
ls -la

# Check if model files exist
if [ -f "diabetes_model.h5" ]; then
    echo "✓ Model file found"
else
    echo "✗ WARNING: diabetes_model.h5 not found"
fi

if [ -f "scaler.joblib" ]; then
    echo "✓ Scaler file found"
else
    echo "✗ WARNING: scaler.joblib not found"
fi

echo "Build process complete"
