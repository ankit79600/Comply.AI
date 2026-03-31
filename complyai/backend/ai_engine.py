import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import shap

# Generate mock data
np.random.seed(42)
ages = np.random.randint(20, 70, 1000)
incomes = np.random.randint(30000, 150000, 1000)
credit_scores = np.random.randint(300, 850, 1000)
loan_amounts = np.random.randint(5000, 100000, 1000)

# Simulate bias: zip_code influence (unfair) and credit_score
zip_codes = np.random.choice([10001, 10002, 10003], 1000)

data = {
    'age': ages,
    'income': incomes,
    'credit_score': credit_scores,
    'loan_amount': loan_amounts,
    'zip_code': zip_codes
}
df = pd.DataFrame(data)

# Approve if credit_score > 600, but penalty if zip_code is 10003 (mocking fair lending violation)
target = ((df['credit_score'] > 600) & (df['zip_code'] != 10003)).astype(int)

# Train a fast model
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(df, target)

# Initialize SHAP explainer
explainer = shap.TreeExplainer(model)

def get_model():
    return model, df

def explain_decision(input_data: dict) -> dict:
    """
    input_data: dict mapped to the dataframe columns
    Returns: Decision (Approve/Deny), confidence, top 3 factors, plain english
    """
    input_df = pd.DataFrame([input_data])
    
    # Prediction
    pred = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0]
    confidence = float(np.max(proba) * 100)
    decision = "Approved" if pred == 1 else "Denied"
    
    # SHAP logic
    shap_values = explainer.shap_values(input_df)
    
    if isinstance(shap_values, list):
        vals = shap_values[1][0]
    else:
        # shap >= 0.40 outputs an explanation object usually
        if hasattr(shap_values, 'values'):
            vals = shap_values.values[0]
            if len(vals.shape) == 2:
                vals = vals[:, 1]
        else:
            if len(shap_values.shape) == 3:
                vals = shap_values[0,:,1]
            elif len(shap_values.shape) == 2:
                vals = shap_values[0]
            else:
                vals = shap_values
                
    feature_names = input_df.columns
    impacts = np.abs(vals)
    total_impact = np.sum(impacts) + 1e-9 # avoid div by zero
    percentages = (impacts / total_impact) * 100
    
    # Get top 3
    top_indices = np.argsort(impacts)[::-1][:3]
    top_factors = []
    
    for idx in top_indices:
        feat = feature_names[idx]
        val = vals[idx]
        pct = percentages[idx]
        direction = "Positive" if val > 0 else "Negative"
        top_factors.append({ 
            "feature": feat,
            "impact_percentage": round(float(pct), 2),
            "direction": direction
        })
    
    explanation = f"Your application was {decision.lower()} with {confidence:.1f}% confidence. "
    explanation += f"The most significant factor was your {top_factors[0]['feature']}."
    
    return {
        "decision": decision,
        "confidence": round(confidence, 2),
        "top_factors": top_factors,
        "plain_english": explanation
    }
