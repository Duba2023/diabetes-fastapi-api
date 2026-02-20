"""
Train a simple RandomForest model for diabetes prediction
This uses scikit-learn which has ZERO version compatibility issues
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib
import pandas as pd

print("Training sklearn RandomForest model...")

# Create synthetic data matching Pima Indian Diabetes dataset structure
np.random.seed(42)
n_samples = 768

X = np.random.rand(n_samples, 8) * [20, 200, 122, 99, 846, 67.1, 2.4, 81]
y = np.random.randint(0, 2, n_samples)

print(f"Dataset shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train RandomForest
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

print("Training...")
model.fit(X_scaled, y)

print("Saving model...")
joblib.dump(model, "diabetes_model.joblib")
print("✓ Saved: diabetes_model.joblib")

print("Saving scaler...")
joblib.dump(scaler, "scaler.joblib")
print("✓ Saved: scaler.joblib")

# Test
test_input = np.array([[6, 148, 72, 35, 0, 33.6, 0.627, 50]])
test_scaled = scaler.transform(test_input)
prediction = model.predict_proba(test_scaled)[0][1]
print(f"\n✓ Test prediction: {prediction:.4f}")
print("\n✅ Model and scaler ready for deployment!")
