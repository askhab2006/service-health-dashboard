import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# 1. Создаем тестовый движок (в памяти)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

# 2. Функция-заменитель для get_db
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

# 3. Фикстура, которая готовит базу ПЕРЕД каждым тестом
@pytest_asyncio.fixture(autouse=True)
async def init_db():
    # Создаем таблицы
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # ПОДМЕНЯЕМ зависимость в приложении
    app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    # Очищаем после теста
    app.dependency_overrides.clear()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# --- САМ ТЕСТ ---
@pytest.mark.asyncio
async def test_create_service_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "name": "Test Service",
            "url": "https://unique-test-url.com",
            "check_interval": 5
        }
        response = await ac.post("/api/v1/services/", json=payload)
    
    assert response.status_code == 201
    assert response.json()["name"] == "Test Service"
