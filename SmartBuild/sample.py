# Load the model and scaler
import joblib
model = joblib.load('material_estimator_model.pkl')
scaler = joblib.load('scaler.pkl')

# Test the model with a sample wall length (e.g., 25.0 meters)
sample_length = 25.0
sample_length_scaled = scaler.transform([[sample_length]])
predicted_materials = model.predict(sample_length_scaled)

# Print the predictions
bricks, cement, sand = predicted_materials[0]
print(f"Bricks: {round(bricks)}, Cement Bags: {round(cement)}, Sand Volume: {round(sand, 2)} m³")
