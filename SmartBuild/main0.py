import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Load your dataset
df = pd.read_csv('wall_length_dataset.csv')

# Extract features (X) and targets (Y)
X = df[['Wall_Length_Meters']]  # Input feature: Wall length
Y = df[['Bricks', 'Cement_Bags', 'Sand_Volume_m3']]  # Output targets

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Scale the input features using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train_scaled, Y_train)

# Save the trained model and scaler using joblib
joblib.dump(model, 'material_estimator_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Model and scaler saved successfully!")
