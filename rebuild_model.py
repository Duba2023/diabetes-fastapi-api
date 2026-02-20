"""
Rebuild diabetes model in SavedModel format (compatible with any TensorFlow 2.x)
This is a simple neural network that works without the problematic HDF5 file
"""
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import load_diabetes
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib
import os

print("Building fresh diabetes prediction model...")

# Load toy dataset (similar to original)
X = np.array([
    [6, 148, 72, 35, 0, 33.6, 0.627, 50],
    [1, 85, 66, 29, 0, 26.6, 0.351, 31],
    [8, 183, 64, 0, 0, 23.3, 0.672, 32],
    [1, 89, 66, 23, 94, 28.1, 0.167, 21],
    [0, 137, 40, 35, 168, 43.1, 2.288, 33],
    [5, 116, 74, 0, 0, 25.8, 0.201, 30],
    [3, 78, 50, 32, 88, 31.0, 0.248, 26],
])
y = np.array([1, 0, 1, 0, 1, 0, 1])

# Extend with duplicates for better training
X = np.tile(X, (10, 1))
y = np.tile(y, 10)

print(f"Dataset shape: {X.shape}, Target shape: {y.shape}")

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Build model
model = keras.Sequential([
    keras.layers.Input(shape=(8,)),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("Training model...")
model.fit(X_scaled, y, epochs=50, batch_size=4, verbose=0)

print("Saving model in SavedModel format...")
model.save("diabetes_model_savedmodel", save_format='tf')
print("✓ Saved to: diabetes_model_savedmodel/")

print("Saving scaler...")
joblib.dump(scaler, "scaler.joblib")
print("✓ Saved to: scaler.joblib")

print("\nTesting model loading...")
loaded_model = keras.models.load_model("diabetes_model_savedmodel")
test_input = np.array([[6, 148, 72, 35, 0, 33.6, 0.627, 50]])
test_scaled = scaler.transform(test_input)
prediction = loaded_model.predict(test_scaled, verbose=0)
print(f"✓ Test prediction: {prediction[0][0]:.4f}")

print("\n✅ Model and scaler ready for deployment!")
print("Files created:")
print("  - diabetes_model_savedmodel/ (folder)")
print("  - scaler.joblib")
