import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255))
    type_projet: Mapped[str] = mapped_column(String(50))  # neuf / rénovation
    usage: Mapped[str] = mapped_column(String(100))       # logement / ERP / tertiaire
    type_erp: Mapped[str | None] = mapped_column(String(10), nullable=True)
    zone_climatique: Mapped[str] = mapped_column(String(10))
    zone_sismique: Mapped[str] = mapped_column(String(5))
    pmr: Mapped[bool] = mapped_column(Boolean, default=False)
    specificites: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cctps: Mapped[list["CCTP"]] = relationship("CCTP", back_populates="project", cascade="all, delete")


class CCTP(Base):
    __tablename__ = "cctps"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"))
    lot_numero: Mapped[str] = mapped_column(String(10))
    lot_nom: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    provider: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project: Mapped["Project"] = relationship("Project", back_populates="cctps")
