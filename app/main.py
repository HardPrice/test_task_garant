from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.posts import router as posts_router
from app.models.models import Base
from app.database.database import engine
from contextlib import asynccontextmanager
from typing import Dict

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup
    await engine.dispose()

app = FastAPI(
    title="Posts API",
    description="API для работы с постами, их фильтрации и анализа",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Проверка работоспособности API
    """
    return {"status": "healthy"}

# Включаем роутер для работы с постами
app.include_router(
    posts_router,
    prefix="/api",
    tags=["posts"]
)
