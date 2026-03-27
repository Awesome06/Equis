from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models import Transaction, User
from app.services.gemini_client import categorize_transactions
from app.services.risk_engine import extract_features
import joblib
import os
from typing import List
import uuid

router = APIRouter(prefix="/api/ml", tags=["ml"])

@router.get("/score/{user_id}")
async def get_financial_resilience_score(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    """
    Calculates the financial resilience score (1-100) for a user.
    """
    # 1. Fetch user items and transactions
    statement = select(User).where(User.external_id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch all transactions for this user's items
    transaction_statement = select(Transaction).join(Transaction.item).where(Transaction.item.has(user_id=user.id))
    result = await session.execute(transaction_statement)
    transactions = result.scalars().all()

    if not transactions:
        return {"score": 0, "status": "No transactions found to score."}

    # 2. Extract features
    features = extract_features(transactions)
    
    # 3. Load model and predict
    model_path = "app/resources/risk_model.pkl"
    if not os.path.exists(model_path):
        raise HTTPException(status_code=500, detail="Risk model not found. Run training script first.")
    
    model = joblib.load(model_path)
    
    # X needs to be a 2D array for scikit-learn
    feature_values = [
        features["income_to_rent_ratio"],
        features["monthly_utility_consistency"],
        features["discretionary_spend_ratio"]
    ]
    
    # RandomForestClassifier.predict_proba returns probability for both classes [low, high]
    # We use the probability of being 'resilient' (higher score)
    probability = model.predict_proba([feature_values])[0][1]
    score = int(probability * 100)
    
    return {
        "user_id": user_id,
        "score": score,
        "features": features
    }

@router.get("/stats/{user_id}")
async def get_user_stats(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    """
    Returns aggregated spending by category for the dashboard.
    """
    statement = select(User).where(User.external_id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch all transactions with categories
    transaction_statement = select(Transaction).join(Transaction.item).where(Transaction.item.has(user_id=user.id))
    result = await session.execute(transaction_statement)
    transactions = result.scalars().all()

    # Aggregate by category
    stats = {}
    for t in transactions:
        cat = t.llm_category or "Unclassified"
        stats[cat] = stats.get(cat, 0.0) + t.amount

    # Format for Tremor DonutChart
    chart_data = [
        {"name": k, "value": abs(v)} for k, v in stats.items()
    ]

    return {
        "total_transactions": len(transactions),
        "chart_data": chart_data
    }

@router.post("/categorize")
async def batch_categorize_transactions(
    session: AsyncSession = Depends(get_session)
):
    """
    Fetches all unclassified transactions, calls Gemini to categorize them, 
    and updates the database.
    """
    # 1. Fetch unclassified transactions
    statement = select(Transaction).where(Transaction.llm_category == None)
    result = await session.execute(statement)
    transactions = result.scalars().all()

    if not transactions:
        return {"status": "success", "updated_count": 0, "message": "No unclassified transactions found."}

    # 2. Extract descriptions
    descriptions = [t.description for t in transactions]
    
    # 3. Call Gemini service
    # Note: For very large lists, we should batch these to Gemini's context limits.
    # For now, we'll process them in one go (or could add batching logic here).
    categorized_data = await categorize_transactions(descriptions)

    # 4. Map results back to transactions and update
    # We use a mapping to ensure we update the right record even if Gemini reorders them (though it shouldn't)
    category_map = {res['description']: res['category'] for res in categorized_data if 'description' in res and 'category' in res}

    updated_count = 0
    for t in transactions:
        if t.description in category_map:
            t.llm_category = category_map[t.description]
            updated_count += 1
            session.add(t)

    await session.commit()
    
    return {
        "status": "success",
        "updated_count": updated_count,
        "results": categorized_data[:10]  # Return a sample of results
    }
