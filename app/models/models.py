from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import Optional

class Base(DeclarativeBase):
    pass

def convert_datetime_to_naive(attr, value, oldvalue, initiator):
    if value is not None and value.tzinfo is not None:
        return value.astimezone(timezone.utc).replace(tzinfo=None)
    return value

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    
    # Связь один-к-одному с ProcessedPost
    processed: Mapped[Optional["ProcessedPost"]] = relationship(
        back_populates="post",
        uselist=False,
    )

class ProcessedPost(Base):
    __tablename__ = "processed_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("posts.id"),
        unique=True,
        index=True
    )
    word_frequency: Mapped[str] = mapped_column(Text)  # JSON строка с частотой слов
    extracted_tags: Mapped[str] = mapped_column(Text)  # JSON строка с извлеченными тегами
    sentiment_score: Mapped[int] = mapped_column(Integer)  # Оценка тональности текста (-1, 0, 1)
    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    
    # Обратная связь с Post
    post: Mapped[Post] = relationship(Post, back_populates="processed")

# Добавляем обработчики событий для автоматической конвертации дат
event.listen(Post.created_at, 'set', convert_datetime_to_naive, retval=True)
event.listen(ProcessedPost.processed_at, 'set', convert_datetime_to_naive, retval=True)
