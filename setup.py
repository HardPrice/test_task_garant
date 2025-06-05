from setuptools import setup, find_packages

setup(
    name="posts-api",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "asyncpg",
        "python-dotenv",
        "pytest",
        "pytest-asyncio",
        "httpx"
    ],
)
