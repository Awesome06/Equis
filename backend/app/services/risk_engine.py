from typing import List
from app.models import Transaction
import pandas as pd
import numpy as np

def extract_features(transactions: List[Transaction]) -> dict:
    """
    Extracts high-level financial features from a list of categorized transactions.
    """
    if not transactions:
        return {
            "income_to_rent_ratio": 0.0,
            "monthly_utility_consistency": 0.0,
            "discretionary_spend_ratio": 0.0
        }

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame([t.model_dump() for t in transactions])
    
    # Calculate income
    total_income = df[df['llm_category'] == 'Income']['amount'].sum()
    if total_income == 0:
        total_income = 1.0  # Avoid division by zero, though in real life this would be a high-risk indicator

    # 1. Income to Rent Ratio
    total_rent = df[df['llm_category'] == 'Rent']['amount'].sum()
    income_to_rent_ratio = abs(total_income / total_rent) if total_rent != 0 else 5.0 # High value if no rent found

    # 2. Monthly Utility Consistency
    # We look at the variance of utility payments
    utility_df = df[df['llm_category'] == 'Utilities'].copy()
    if not utility_df.empty:
        # Simple consistency metric: (1 / (1 + std_dev))
        # Lower variance in amount = more consistent
        std_dev = utility_df['amount'].std()
        if pd.isna(std_dev):
            utility_consistency = 1.0 # Only one utility bill is "consistent"
        else:
            utility_consistency = 1.0 / (1.0 + (std_dev / utility_df['amount'].mean()))
    else:
        utility_consistency = 0.0 # No utilities found

    # 3. Discretionary Spend Ratio
    total_discretionary = df[df['llm_category'] == 'Discretionary']['amount'].sum()
    discretionary_spend_ratio = abs(total_discretionary / total_income)

    return {
        "income_to_rent_ratio": float(income_to_rent_ratio),
        "monthly_utility_consistency": float(utility_consistency),
        "discretionary_spend_ratio": float(discretionary_spend_ratio)
    }
