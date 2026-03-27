"""
Database engine, async session factory, and startup helper.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import settings

# ── Engine ────────────────────────────────────────────────────────────────────

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
)

# ── Session factory ───────────────────────────────────────────────────────────

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── Dependency ────────────────────────────────────────────────────────────────

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async DB session."""
    async with async_session() as session:  # type: ignore[operator]
        yield session


# ── Startup helper ────────────────────────────────────────────────────────────

async def create_db_and_tables() -> None:
    """Create all SQLModel tables (idempotent)."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
