from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_session
from app.services.post_service import PostService
from app.models.models import Post
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict

router = APIRouter()

class ProcessedPostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    post_id: int
    word_frequency: str
    extracted_tags: str
    sentiment_score: int
    processed_at: datetime

class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    category: str
    content: str
    created_at: datetime
    processed: Optional[ProcessedPostResponse] = None

class PaginatedResponse(BaseModel):
    items: List[PostResponse]
    total: int
    page: int
    pages: int
    has_next: bool
    has_prev: bool

@router.get("/posts/", response_model=PaginatedResponse)
async def get_posts(
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    limit: int = Query(default=10, ge=1, le=100),
    page: int = Query(default=1, ge=1),
    session: AsyncSession = Depends(get_session)
):
    """
    Получение списка постов с фильтрацией и пагинацией.
    
    Parameters:
    - category: фильтр по категории
    - keyword: поиск по ключевым словам в контенте
    - limit: количество записей на странице
    - page: номер страницы
    
    Returns:
    - items: список постов
    - total: общее количество записей
    - page: текущая страница
    - pages: общее количество страниц
    - has_next: есть ли следующая страница
    - has_prev: есть ли предыдущая страница
    """
    offset = (page - 1) * limit
    post_service = PostService(session)
    
    posts, total = await post_service.filter_posts(
        category=category,
        keyword=keyword,
        limit=limit,
        offset=offset
    )
    
    total_pages = (total + limit - 1) // limit
    
    return PaginatedResponse(
        items=posts,
        total=total,
        page=page,
        pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )

@router.post("/posts/{post_id}/process", response_model=ProcessedPostResponse)
async def process_post(
    post_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Обработка поста с анализом текста.
    
    Parameters:
    - post_id: ID поста для обработки
    
    Returns:
    - Результаты обработки поста, включая:
        - частоту слов
        - извлеченные теги
        - оценку тональности
        - время обработки
    """
    post_service = PostService(session)
    post = await session.get(Post, post_id)
    
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    processed_post = await post_service.process_post(post)
    return processed_post

@router.get("/posts/stats", response_model=Dict)
async def get_posts_stats(
    session: AsyncSession = Depends(get_session)
):
    """
    Получение статистики по всем постам.
    
    Returns:
    - Статистика по категориям
    - Общее количество постов
    - Количество обработанных постов
    - Распределение тональности
    """
    post_service = PostService(session)
    # TODO: Реализовать метод получения статистики
    # Это можно сделать с помощью агрегирующих запросов
    return {
        "total_posts": 0,
        "processed_posts": 0,
        "categories": {},
        "sentiment_distribution": {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }
    }
