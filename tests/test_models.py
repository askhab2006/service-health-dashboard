import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Base, Service, CheckResult


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as session:
        yield session
    
    await engine.dispose()

@pytest.mark.asyncio
async def test_create_service_model(db_session: AsyncSession):

    new_service = Service(
        name="Model Test Name", 
        url="https://model-unique-url.com", 
        check_interval=10
    )
    db_session.add(new_service)
    await db_session.commit()
    await db_session.refresh(new_service)
    
    assert new_service.id is not None
    assert new_service.name == "Model Test Name"



@pytest.mark.asyncio
async def test_service_check_result_relationship(db_session: AsyncSession):
    """Проверка связи между Сервисом и Результатами (Relationship)"""
    service = Service(name="Monitor", url="https://mon.com")
    db_session.add(service)
    await db_session.flush() 
    

    result = CheckResult(
        service_id=service.id,
        status="UP",
        response_time=150.5,
        status_code=200
    )
    db_session.add(result)
    await db_session.commit()
    
    await db_session.refresh(service)
    assert len(service.check_results) == 1
    assert service.check_results[0].status == "UP"
