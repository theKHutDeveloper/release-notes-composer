from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """SQLAlchemy declarative base"""


class Release(Base):
    __tablename__ = "releases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    notes_md: Mapped[str] = mapped_column(Text)
    notes_html: Mapped[str] = mapped_column(Text)
    meta: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    changes: Mapped[list[Change]] = relationship(
        back_populates="release", cascade="all, delete-orphan"
    )


class Change(Base):
    __tablename__ = "changes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sha: Mapped[str | None] = mapped_column(String(40), index=True)
    title: Mapped[str] = mapped_column(String(300))
    body: Mapped[str | None] = mapped_column(Text)
    type: Mapped[str | None] = mapped_column(String(20))  # feat/fix/docs/...
    component: Mapped[str | None] = mapped_column(String(80))  # parsed from scope
    labels: Mapped[dict | None] = mapped_column(JSON)  # optional
    pr_number: Mapped[int | None] = mapped_column(Integer)
    author: Mapped[str | None] = mapped_column(String(120))
    merged_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # FK → releases
    release_id: Mapped[int | None] = mapped_column(ForeignKey("releases.id"))
    release: Mapped[Release | None] = relationship(back_populates="changes")
