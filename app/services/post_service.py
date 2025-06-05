import json
from collections import Counter
from typing import List, Tuple, Dict
from sqlalchemy import select, or_, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.models import Post, ProcessedPost

class PostService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.BATCH_SIZE = 100

    async def filter_posts(
        self,
        category: str = None,
        keyword: str = None,
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[List[Post], int]:
        # Базовый запрос с загрузкой связанных данных
        query = (
            select(Post)
            .options(selectinload(Post.processed))
            .order_by(Post.created_at.desc())
        )
        
        # Применяем фильтры
        filters = []
        if category:
            filters.append(Post.category == category)
        if keyword:
            # Поиск по нескольким словам
            for word in keyword.split():
                filters.append(Post.content.ilike(f"%{word}%"))
        
        if filters:
            query = query.filter(and_(*filters))
        
        # Получаем общее количество записей для пагинации
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query)
        
        # Применяем пагинацию
        query = query.limit(limit).offset(offset)
        
        # Выполняем запрос
        result = await self.session.execute(query)
        posts = result.scalars().all()
        
        return posts, total

    async def process_post(self, post: Post) -> ProcessedPost:
        """Обработка поста с анализом текста"""
        # Подсчет частоты слов (исключаем стоп-слова и пунктуацию)
        words = [word.lower() for word in post.content.split() 
                if len(word) > 2 and not word.startswith(('#', '@', 'http'))]
        word_frequency = Counter(words)
        
        # Извлечение тегов и упоминаний
        tags = [word for word in post.content.split() 
                if word.startswith('#')]
        mentions = [word for word in post.content.split() 
                   if word.startswith('@')]
        
        # Простой анализ тональности
        sentiment_score = await self._analyze_sentiment(post.content)
        
        # Создаем или обновляем запись об обработанном посте
        processed_data = {
            'word_frequency': json.dumps(dict(word_frequency), ensure_ascii=False),
            'extracted_tags': json.dumps({
                'hashtags': tags,
                'mentions': mentions
            }, ensure_ascii=False),
            'sentiment_score': sentiment_score
        }
        
        processed_post = await self._get_or_create_processed_post(post.id)
        for key, value in processed_data.items():
            setattr(processed_post, key, value)
        
        await self.session.commit()
        return processed_post

    async def _get_or_create_processed_post(self, post_id: int) -> ProcessedPost:
        """Получение или создание записи ProcessedPost"""
        query = select(ProcessedPost).filter(ProcessedPost.post_id == post_id)
        result = await self.session.execute(query)
        processed_post = result.scalar_one_or_none()
        
        if not processed_post:
            processed_post = ProcessedPost(post_id=post_id)
            self.session.add(processed_post)
        
        return processed_post

    async def _analyze_sentiment(self, text: str) -> int:
        """
        Простой анализ тональности текста
        Возвращает: -1 (негативный), 0 (нейтральный), 1 (позитивный)
        """
        # Простые списки позитивных и негативных слов
        positive_words = {'хорошо', 'отлично', 'замечательно', 'прекрасно', 'круто'}
        negative_words = {'плохо', 'ужасно', 'отвратительно', 'грустно', 'печально'}
        
        words = text.lower().split()
        
        pos_count = sum(1 for word in words if word in positive_words)
        neg_count = sum(1 for word in words if word in negative_words)
        
        if pos_count > neg_count:
            return 1
        elif neg_count > pos_count:
            return -1
        return 0
