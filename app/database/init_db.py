from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Post
import asyncio

async def create_test_data(session: AsyncSession):
    # Создаем тестовые посты
    test_posts = [
        Post(
            category="Технологии",
            content="Искусственный интеллект становится все лучше! #AI #технологии Это отличная новость для разработчиков."
        ),
        Post(
            category="Новости",
            content="Сегодня плохая погода. Дождь и ветер. #погода Настроение печальное."
        ),
        Post(
            category="Технологии",
            content="Python 3.12 выпущен! Это замечательное обновление. #python #programming Производительность существенно улучшена."
        ),
        Post(
            category="Разное",
            content="Посетил новый ресторан. Ужасное обслуживание, но еда отличная! #рестораны #обзор"
        ),
        Post(
            category="Технологии",
            content="PostgreSQL или MySQL? Оба отличные решения для разных задач. #database #programming"
        ),
    ]
    
    for post in test_posts:
        session.add(post)
    
    await session.commit()

if __name__ == "__main__":
    # Этот код можно запустить отдельно для создания тестовых данных
    from app.database.database import async_session
    import asyncio
    
    async def init_test_data():
        async with async_session() as session:
            await create_test_data(session)
    
    asyncio.run(init_test_data())
