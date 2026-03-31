import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

print("Generating mock banking data...")
np.random.seed(42)
n_samples = 1000

# Create dummy features
data = {
    'credit_score': np.random.randint(300, 850, size=n_samples),
    'income': np.random.randint(20000, 150000, size=n_samples),
    'loan_amount': np.random.randint(5000, 50000, size=n_samples),
    'zip_code': np.random.choice([10001, 10002, 10003, 10004], size=n_samples),
}

df = pd.DataFrame(data)

# Create a target variable (loan default)
# Base risk is calculated from credit score and debt-to-income
base_risk = (df['loan_amount'] / df['income']) * 0.4 + ((850 - df['credit_score']) / 550) * 0.4

# Introduce an artificial bias: zip code 10003 is denied much more often
# This ensures that the ComplyAI fairness test will "catch" the bias!
bias = np.where(df['zip_code'] == 10003, 0.3, 0.0)

prob = np.clip(base_risk + bias, 0, 1)
df['loan_default'] = np.random.binomial(1, prob)

# Train the model
print("Training RandomForestClassifier...")
X = df[['credit_score', 'income', 'loan_amount', 'zip_code']]
y = df['loan_default']

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

# Save the model
model_path = "mock_rf_model.pkl"
joblib.dump(model, model_path)

print(f"✅ Success! Mock model saved to: {os.path.abspath(model_path)}")
