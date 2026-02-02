from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ServiceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    url: Optional[HttpUrl] = Field(None, description="URL сервиса для проверки")
    check_interval: int = Field(default=5, ge=1, le=60)

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    url: Optional[HttpUrl] = None
    check_interval: Optional[int] = Field(None, ge=1, le=60)
    is_active: Optional[bool] = None

class ServiceResponse(ServiceBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CheckResultBase(BaseModel):
    status: str
    response_time: float
    status_code: Optional[int] = None
    error_message: Optional[str] = None

class CheckResultCreate(CheckResultBase):
    service_id: int

class CheckResultResponse(CheckResultBase):
    id: int
    service_id: int
    checked_at: datetime

    model_config = ConfigDict(from_attributes=True)


