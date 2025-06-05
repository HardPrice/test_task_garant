import pytest
from httpx import AsyncClient
from app.models.models import Post
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_create_and_list_posts(client: AsyncClient, test_session: AsyncSession):
    # Создаем тестовый пост
    test_post = Post(
        category="Test",
        content="Test post content #test"
    )
    test_session.add(test_post)
    await test_session.commit()
    
    # Тестируем получение списка постов
    response = await client.get("/api/posts/")
    assert response.status_code == 200
    data = response.json()
    
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["total"] == 1
    assert data["items"][0]["category"] == "Test"
    assert data["items"][0]["content"] == "Test post content #test"

@pytest.mark.asyncio
async def test_filter_posts_by_category(client: AsyncClient, test_session: AsyncSession):
    # Создаем тестовые посты
    posts = [
        Post(category="Tech", content="Tech post"),
        Post(category="News", content="News post"),
        Post(category="Tech", content="Another tech post")
    ]
    for post in posts:
        test_session.add(post)
    await test_session.commit()
    
    # Тестируем фильтрацию по категории
    response = await client.get("/api/posts/?category=Tech")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["items"]) == 2
    assert all(post["category"] == "Tech" for post in data["items"])

@pytest.mark.asyncio
async def test_search_posts_by_keyword(client: AsyncClient, test_session: AsyncSession):
    # Создаем тестовые посты
    posts = [
        Post(category="Tech", content="Python is awesome"),
        Post(category="News", content="Regular news"),
        Post(category="Tech", content="Python tutorial")
    ]
    for post in posts:
        test_session.add(post)
    await test_session.commit()
    
    # Тестируем поиск по ключевому слову
    response = await client.get("/api/posts/?keyword=Python")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["items"]) == 2
    assert all("Python" in post["content"] for post in data["items"])

@pytest.mark.asyncio
async def test_pagination(client: AsyncClient, test_session: AsyncSession):
    # Создаем 15 тестовых постов
    posts = [
        Post(category="Test", content=f"Test content {i}")
        for i in range(15)
    ]
    for post in posts:
        test_session.add(post)
    await test_session.commit()
    
    # Тестируем первую страницу (10 записей)
    response = await client.get("/api/posts/?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["items"]) == 10
    assert data["total"] == 15
    assert data["has_next"] == True
    assert data["has_prev"] == False
    
    # Тестируем вторую страницу (оставшиеся 5 записей)
    response = await client.get("/api/posts/?page=2&limit=10")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["items"]) == 5
    assert data["total"] == 15
    assert data["has_next"] == False
    assert data["has_prev"] == True

@pytest.mark.asyncio
async def test_process_post(client: AsyncClient, test_session: AsyncSession):
    # Создаем тестовый пост
    test_post = Post(
        category="Test",
        content="This is a great test post! #test #python"
    )
    test_session.add(test_post)
    await test_session.commit()

    # Запрашиваем обработку поста
    response = await client.post(f"/api/posts/{test_post.id}/process")
    assert response.status_code == 200
    data = response.json()
    
    # Проверяем, что обработка прошла успешно
    assert data["id"] == test_post.id
    assert "word_frequency" in data
    assert "extracted_tags" in data
    assert "sentiment_score" in data
