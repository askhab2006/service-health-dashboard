from app.schemas import ServiceCreate, ServiceUpdate, CheckResultCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Service, CheckResult
from app import models, schemas

async def get_service(db: AsyncSession, service_id: int) -> Service | None:
    stmt = select(Service).where(Service.id == service_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_service_by_url(db: AsyncSession, url: str):
    result = await db.execute(select(models.Service).where(models.Service.url == url))
    return result.scalar_one_or_none()

async def get_services(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Service]:
    stmt = select(Service).order_by(Service.id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def create_service(db: AsyncSession, service_in: schemas.ServiceCreate):
    service_data = service_in.model_dump()
    service_data["url"] = str(service_data["url"]) 
    
    db_object = Service(**service_data)
    db.add(db_object)
    await db.commit()
    await db.refresh(db_object)
    return db_object


async def update_service(db: AsyncSession, db_service: Service, service_in: ServiceUpdate) -> Service:
    update_data = service_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_service, field, value)
    
    db.add(db_service)
    await db.commit()
    await db.refresh(db_service)
    return db_service

async def delete_service(db: AsyncSession, db_service: Service) -> None:
    await db.delete(db_service)
    await db.commit()

async def create_check_result(db: AsyncSession, check_result: CheckResultCreate) -> CheckResult: 
    db_object = CheckResult(**check_result.model_dump())
    db.add(db_object)
    await db.commit()
    await db.refresh(db_object)
    return db_object

async def get_latest_check_result(db: AsyncSession, service_id: int):
    stmt = (
        select(models.CheckResult)
        .where(models.CheckResult.service_id == service_id)
        .order_by(models.CheckResult.checked_at.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

