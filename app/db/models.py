from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from rag_backend.app.db.database import Base


class Document(Base):
    """Store metadata for an uploaded document."""

    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    chunking_strategy: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    total_chunks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )