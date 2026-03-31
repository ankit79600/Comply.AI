from complyai.backend.ai_engine import get_model, explain_decision
import pandas as pd
import numpy as np

def run_compliance_tests(model_id: str, regulations: list) -> list:
    model, df = get_model()
    results = []
    
    if "Fair Lending Act" in regulations:
        # Test 1: Zip Code Bias
        zip_rates = df.copy()
        zip_rates['pred'] = model.predict(df)
        approval_rates = zip_rates.groupby('zip_code')['pred'].mean()
        
        diff = approval_rates.max() - approval_rates.min()
        if diff > 0.1: # 10% tolerance
            results.append({
                "regulation_name": "Fair Lending Act",
                "status": "FAIL",
                "details": f"Disparate impact found across regions. Max approval diff is {diff*100:.1f}%.",
                "suggestion": "Remove 'zip_code' from training data as it acts as a proxy for race/income."
            })
        else:
            results.append({
                "regulation_name": "Fair Lending Act",
                "status": "PASS",
                "details": "Approval rates across regions are within acceptable bounds.",
                "suggestion": "None."
            })
    
    if "Model Risk Management" in regulations:
        # Test 2: Explainability check
        try:
            # check if we can run explain_decision
            sample = df.iloc[0].to_dict()
            explain_decision(sample)
            results.append({
                "regulation_name": "Model Risk Management",
                "status": "PASS",
                "details": "Model successfully produces SHAP baseline explanations.",
                "suggestion": "None."
            })
        except Exception as e:
            results.append({
                "regulation_name": "Model Risk Management",
                "status": "FAIL",
                "details": f"Failed to generate SHAP explanation: {str(e)}",
                "suggestion": "Ensure the model is compatible with tree explainer or kernel explainer."
            })
            
    return results
