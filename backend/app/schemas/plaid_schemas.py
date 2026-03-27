from pydantic import BaseModel
from typing import Optional
import uuid

class LinkTokenCreateRequest(BaseModel):
    user_id: str  # external_id from User table

class PublicTokenExchangeRequest(BaseModel):
    public_token: str
    user_id: str  # external_id to find our User record

class TransactionSyncRequest(BaseModel):
    item_id: uuid.UUID
