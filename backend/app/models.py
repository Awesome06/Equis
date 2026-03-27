"""
SQLModel data models for The David Protocol.

Tables
------
- User      – represents a platform user
- Item      – a Plaid Item (bank connection) belonging to a user
- Transaction – a single bank transaction tied to an item
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timezone
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


# ── Helpers ───────────────────────────────────────────────────────────────────

def _uuid() -> uuid.UUID:
    return uuid.uuid4()


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ── User ──────────────────────────────────────────────────────────────────────

class User(SQLModel, table=True):
    """Platform user identified by an external id (e.g. auth provider sub)."""

    id: uuid.UUID = Field(default_factory=_uuid, primary_key=True)
    external_id: str = Field(unique=True, index=True, max_length=256)
    created_at: datetime = Field(default_factory=_utcnow)

    # relationships
    items: list["Item"] = Relationship(back_populates="user")


# ── Item (Plaid connection) ──────────────────────────────────────────────────

class Item(SQLModel, table=True):
    """A Plaid Item — one per bank connection per user."""

    id: uuid.UUID = Field(default_factory=_uuid, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    plaid_access_token: str = Field(max_length=512)
    plaid_item_id: str = Field(unique=True, index=True, max_length=256)

    # relationships
    user: Optional[User] = Relationship(back_populates="items")
    transactions: list["Transaction"] = Relationship(back_populates="item")


# ── Transaction ──────────────────────────────────────────────────────────────

class Transaction(SQLModel, table=True):
    """A single bank transaction record."""

    id: uuid.UUID = Field(default_factory=_uuid, primary_key=True)
    item_id: uuid.UUID = Field(foreign_key="item.id", index=True)
    account_id: str = Field(max_length=256)
    date: date
    amount: float
    description: str = Field(max_length=1024)
    llm_category: Optional[str] = Field(default=None, max_length=64)
    is_recurring: bool = Field(default=False)

    # relationships
    item: Optional[Item] = Relationship(back_populates="transactions")
