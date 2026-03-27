from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, col
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.models import User, Item, Transaction
from app.services.plaid_client import plaid_client
from app.schemas.plaid_schemas import LinkTokenCreateRequest, PublicTokenExchangeRequest, TransactionSyncRequest
import plaid
from plaid.model.link_token_create_request import LinkTokenCreateRequest as PlaidLinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from datetime import date, timedelta
from typing import List
import uuid

router = APIRouter(prefix="/api/plaid", tags=["plaid"])

@router.post("/create_link_token")
async def create_link_token(req: LinkTokenCreateRequest):
    """
    Creates a Plaid Link token for a given user.
    """
    try:
        request = PlaidLinkTokenCreateRequest(
            products=[Products("transactions")],
            client_name="The David Protocol",
            country_codes=[CountryCode("US")],
            language="en",
            user=LinkTokenCreateRequestUser(client_user_id=req.user_id)
        )
        response = plaid_client.link_token_create(request)
        return {"link_token": response['link_token']}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Plaid Link Token error: {str(e)}"
        )

@router.post("/exchange_public_token")
async def exchange_public_token(
    req: PublicTokenExchangeRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Exchanges a public token for a permanent access token and stores it.
    """
    # 1. Check if user exists
    statement = select(User).where(User.external_id == req.user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    
    if not user:
        # For hackathon purposes, auto-create the user if they don't exist
        user = User(external_id=req.user_id)
        session.add(user)
        await session.commit()
        await session.refresh(user)

    try:
        # 2. Exchange token
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=req.public_token
        )
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)
        
        # 3. Store the item
        new_item = Item(
            user_id=user.id,
            plaid_access_token=exchange_response['access_token'],
            plaid_item_id=exchange_response['item_id']
        )
        session.add(new_item)
        await session.commit()
        
        return {"status": "success", "item_id": new_item.id}
    except plaid.ApiException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Plaid Exchange error: {str(e)}"
        )

@router.post("/sync_transactions")
async def sync_transactions(
    req: TransactionSyncRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Fetches the last 90 days of transactions and syncs them to the DB.
    """
    # 1. Find the Item mapping
    statement = select(Item).where(Item.id == req.item_id)
    result = await session.execute(statement)
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    try:
        # 2. Fetch 90 days of data from Plaid
        start_date = date.today() - timedelta(days=90)
        end_date = date.today()
        
        plaid_request = TransactionsGetRequest(
            access_token=item.plaid_access_token,
            start_date=start_date,
            end_date=end_date
        )
        response = plaid_client.transactions_get(plaid_request)
        plaid_transactions = response['transactions']
        
        # 3. Insert transactions into database
        new_transactions = [
            Transaction(
                item_id=item.id,
                account_id=pt['account_id'],
                date=pt['date'],
                amount=pt['amount'],
                description=pt['name'],
                is_recurring=False # Default for now
            ) for pt in plaid_transactions
        ]
        
        session.add_all(new_transactions)
        await session.commit()
        
        return {
            "status": "success", 
            "synced_count": len(new_transactions)
        }
        
    except plaid.ApiException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Plaid Sync error: {str(e)}"
        )
