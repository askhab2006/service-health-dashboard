from fastapi import APIRouter,HTTPException, status
from typing import List

from app.checker import health_check
from app import crud,schemas
from app.database import SessionDep

router = APIRouter(prefix="/services", tags=["Services"])

@router.get("/", response_model=List[schemas.ServiceResponse])
async def get_services(db: SessionDep, skip: int = 0, limit: int = 100):
    services = await crud.get_services(db=db, skip=skip, limit=limit)
    return services
    

@router.get("/{service_id}", response_model=schemas.ServiceResponse)
async def get_service(service_id: int, db: SessionDep):
    service = await crud.get_service(db=db, service_id=service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сервис не найден")
    return service

@router.post("/", response_model=schemas.ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(service_in: schemas.ServiceCreate, db: SessionDep):
    existing_service = await crud.get_service_by_url(db, url=str(service_in.url))
    if existing_service:
        raise HTTPException(
            status_code=400, 
            detail="Сервис с таким URL уже зарегистрирован"
        )
    return await crud.create_service(db=db, service_in=service_in)


@router.put("/{service_id}", response_model=schemas.ServiceResponse)
async def update_service(service_id: int, service_in: schemas.ServiceUpdate, db: SessionDep):
    db_service = await crud.update_service(db=db, service_id=service_id, service_in=service_in)
    if not db_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сервис не найден")
    return db_service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_id: int, db: SessionDep):
    db_service = await crud.get_service(db=db, service_id=service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Сервис не найден")
    await crud.delete_service(db=db, db_service=db_service)
    return None


@router.post("/{service_id}/check-now", response_model=schemas.CheckResultResponse)
async def check_service_now(service_id: int, db: SessionDep):
    db_service = await crud.get_service(db=db, service_id=service_id)
    if not db_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сервис не найден")
    result_data = await health_check.run_check(db_service.url)
    check_create = schemas.CheckResultCreate(**result_data, service_id=service_id)
    return await crud.create_check_result(db, check_result=check_create)


@router.get("/checks/latest", response_model=List[schemas.CheckResultResponse], tags=["Checks"])
async def get_latest_checks(db: SessionDep):
    results = await crud.get_latest_check_results(db)
    return results


@router.get("/{id}/checks", response_model=List[schemas.CheckResultResponse], tags=["Checks"])
async def get_checks_for_service(id: int, db: SessionDep, skip: int = 0, limit: int = 100):
    db_service = await crud.get_service(db=db, service_id=id)
    if not db_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сервис не найден")
    results = await crud.get_check_results_for_service(db=db, service_id=id, skip=skip, limit=limit)
    return results