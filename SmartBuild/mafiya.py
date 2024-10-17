import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = pd.read_csv('wall_length_dataset.csv')

# Extract features (X) and targets (Y)
X = df[['Wall_Length_Meters']]  # Input: Wall length (you can extend with more features)
Y = df[['Bricks', 'Cement_Bags', 'Sand_Volume_m3']]  # Targets: Materials to predict

# Split into training and test sets (80% train, 20% test)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Scale the input features for better model performance
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)




from sklearn.linear_model import LinearRegression

# Initialize the model
model = LinearRegression()

# Train the model on the training data
model.fit(X_train_scaled, Y_train)

# Check the model’s coefficients (weights)
print(f'Model Coefficients: {model.coef_}')
print(f'Model Intercept: {model.intercept_}')




from sklearn.metrics import mean_squared_error, r2_score

# Predict materials on the test set
Y_pred = model.predict(X_test_scaled)

# Evaluate the model using R-squared and Mean Squared Error (MSE)
print(f'R-squared Score: {r2_score(Y_test, Y_pred):.2f}')
print(f'Mean Squared Error: {mean_squared_error(Y_test, Y_pred):.2f}')
