from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, col
from app.database import get_session
from app.models import Transaction
from app.services.gemini_client import categorize_transactions
from typing import List
import uuid

router = APIRouter(prefix="/api/ml", tags=["ml"])

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
