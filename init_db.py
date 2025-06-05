import asyncio
from app.database.database import async_session, engine
from app.models.models import Base, Post

async def init_db():
    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print("Таблицы успешно созданы!")

    # Создаем тестовые данные
    async with async_session() as session:
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
        print("База данных успешно инициализирована тестовыми данными!")

if __name__ == "__main__":
    asyncio.run(init_db())
