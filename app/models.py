from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import  String, ForeignKey, func
from datetime import datetime
from typing import List
from .database import Base


class Service(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    url: Mapped[str] = mapped_column(String(200), nullable=True, unique=True, index=True)
    check_interval: Mapped[int] = mapped_column(default=5)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    check_results: Mapped[List["CheckResult"]] = relationship(back_populates="service", cascade="all, delete-orphan",lazy="selectin")

class CheckResult(Base):
    __tablename__ = 'check_results'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey('services.id'), nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    response_time: Mapped[float] = mapped_column(nullable=False)
    status_code: Mapped[int] = mapped_column(nullable=True)
    error_message: Mapped[str] = mapped_column(String(200), nullable=True)
    checked_at: Mapped[datetime] = mapped_column(server_default=func.now())


    service: Mapped["Service"] = relationship(back_populates="check_results")