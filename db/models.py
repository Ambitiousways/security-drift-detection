from __future__ import annotations

from datetime import datetime, UTC
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, JSON

class Base(DeclarativeBase):
    pass

class DriftRun(Base):
    __tablename__ = "drift_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    host: Mapped[str] = mapped_column(String(256), nullable=False)
    captured_at: Mapped[str] = mapped_column(String(64), nullable=False)

    risk_level: Mapped[str] = mapped_column(String(16), nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)

    snapshot_path: Mapped[str] = mapped_column(String(512), nullable=False)
    result: Mapped[dict] = mapped_column(JSON, nullable=False)
