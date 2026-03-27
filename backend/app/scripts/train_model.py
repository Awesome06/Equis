import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def generate_synthetic_data(n_samples=1000):
    """
    Generates a synthetic dataset for testing the risk score model.
    """
    np.random.seed(42)
    
    # Features
    # income_to_rent_ratio: Normal dist around 3.5
    income_to_rent_ratio = np.random.normal(3.5, 1.5, n_samples)
    
    # utility_consistency: Normal dist around 0.7
    utility_consistency = np.random.uniform(0, 1, n_samples)
    
    # discretionary_spend_ratio: Normal dist around 0.3
    discretionary_spend_ratio = np.random.normal(0.3, 0.2, n_samples)
    
    # Label logic: Higher income/rent and utility consistency, lower discretionary spend = higher score
    # We simulate a "Financial Resilience" probability
    prob = (
        (income_to_rent_ratio / 10.0) * 0.4 + 
        (utility_consistency) * 0.3 + 
        (1.0 - np.clip(discretionary_spend_ratio, 0, 1)) * 0.3
    )
    prob = np.clip(prob, 0, 1)
    
    # Class labels: 1 if high resilience (score > 60), else 0
    labels = (prob > 0.6).astype(int)
    
    df = pd.DataFrame({
        "income_to_rent_ratio": income_to_rent_ratio,
        "monthly_utility_consistency": utility_consistency,
        "discretionary_spend_ratio": discretionary_spend_ratio,
        "resilient": labels
    })
    
    return df

def train_and_save_model():
    """Trains a RandomForestClassifier and saves it as a .pkl file."""
    df = generate_synthetic_data()
    X = df.drop("resilient", axis=1)
    y = df["resilient"]
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Ensure directory exists
    model_dir = "app/resources"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    model_path = os.path.join(model_dir, "risk_model.pkl")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()
