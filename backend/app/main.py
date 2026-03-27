"""
The David Protocol — FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_db_and_tables
from app.routers.plaid import router as plaid_router
from app.routers.ml import router as ml_router

# Import models so SQLModel registers their metadata before table creation.
import app.models  # noqa: F401


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown lifecycle hook."""
    await create_db_and_tables()
    yield


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="The David Protocol",
    summary="Cash-flow underwriting engine for credit-invisible users",
    version="0.1.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plaid_router)
app.include_router(ml_router)


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/")
async def health_check():
    return {"status": "ok"}
