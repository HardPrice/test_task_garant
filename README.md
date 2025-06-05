# Posts API Service

Сервис для работы с постами, их фильтрации и анализа тональности текста. API построено с использованием FastAPI и асинхронного взаимодействия с PostgreSQL.

## Основные возможности

- CRUD операции с постами
- Фильтрация постов по категориям
- Поиск по ключевым словам
- Пагинация результатов
- Анализ постов:
  - Подсчет частоты слов
  - Извлечение тегов из текста
  - Анализ тональности текста

## Технический стек

- Python 3.13
- FastAPI
- SQLAlchemy (async)
- PostgreSQL + asyncpg
- pytest для тестирования
- httpx для асинхронных HTTP-запросов

## Требования

- Python 3.13+
- PostgreSQL 14+
- Виртуальное окружение Python (рекомендуется)

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/HardPrice/test_task_garant.git
cd test_task_garant
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте PostgreSQL:
- Создайте базу данных `posts_db`
- Создайте тестовую базу данных `posts_test_db`
- Настройте доступ для пользователя PostgreSQL (по умолчанию используется `postgres:nikita22335`)

5. Запустите миграции:
```bash
python init_db.py
```

6. Запустите сервер:
```bash
python run.py
```

API будет доступно по адресу: http://localhost:8000

## Тестирование

Для запуска тестов используйте:
```bash
pytest
```

## API Endpoints

### GET /health
Проверка работоспособности сервиса.

### GET /api/posts/
Получение списка постов с фильтрацией и пагинацией.

Параметры:
- category (опционально): фильтрация по категории
- keyword (опционально): поиск по ключевому слову
- page (по умолчанию=1): номер страницы
- limit (по умолчанию=10): количество записей на странице

### POST /api/posts/{post_id}/process
Запуск обработки поста для анализа текста.

## Структура проекта

```
├── app/
│   ├── api/          # API endpoints
│   ├── database/     # Конфигурация базы данных
│   ├── models/       # SQLAlchemy модели
│   └── services/     # Бизнес-логика
├── tests/            # Тесты
├── init_db.py        # Скрипт инициализации БД
└── run.py           # Точка входа приложения
```

## Лицензия

MIT

## Автор

HardPrice
