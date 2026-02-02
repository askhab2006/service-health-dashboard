from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from app.api.endpoints import router as api_router
from app.checker.scheduler import scheduler_manager 
from . import schemas
from . import crud
from .database import SessionDep


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    scheduler_manager.start_scheduler()
    yield
    scheduler_manager.stop_scheduler()
    
app = FastAPI(title="Service Health Dashboard", lifespan=lifespan)


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


app.include_router(api_router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: SessionDep):
    services = await crud.get_services(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "services": services},
    )

@app.get("/api/health", tags=["System"])
async def health_check():
    return {"status": "ok"}

@app.get("/services/{service_id}", response_class=HTMLResponse)
async def service_detail(request: Request, service_id: int, db: SessionDep):
    service = await crud.get_service(db, service_id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    results = await crud.get_check_results_for_service(db, service_id=service_id, limit=20)
    results.reverse() 
    
    return templates.TemplateResponse("service_detail.html", {
        "request": request, 
        "service": service, 
        "results": results
    })

@app.get("/add-service", response_class=HTMLResponse)
async def add_service_page(request: Request):
    return templates.TemplateResponse("add_service.html", {"request": request})

@app.post("/add-service")
async def create_service_from_form(
    db: SessionDep,
    name: str = Form(...),
    url: str = Form(...),
    check_interval: int = Form(5)
):
    service_in = schemas.ServiceCreate(name=name, url=url, check_interval=check_interval)
    await crud.create_service(db=db, service_in=service_in)
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
