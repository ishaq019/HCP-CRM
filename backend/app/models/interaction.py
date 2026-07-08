from sqlalchemy import Boolean, DateTime, Integer, JSON, Sequence, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(Integer, Sequence("crm_interactions_id_seq"), primary_key=True, index=True)
    hcp_name: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    hcp_specialty: Mapped[str | None] = mapped_column(String(160), nullable=True)
    organization: Mapped[str | None] = mapped_column(String(220), nullable=True, index=True)
    interaction_type: Mapped[str] = mapped_column(String(40), nullable=False)
    interaction_datetime: Mapped[DateTime] = mapped_column(DateTime(timezone=False), nullable=False)
    discussion_summary: Mapped[str] = mapped_column(Text, nullable=False)
    products_discussed: Mapped[str | None] = mapped_column(Text, nullable=True)
    samples_requested: Mapped[str | None] = mapped_column(Text, nullable=True)
    follow_up_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    follow_up_date: Mapped[DateTime | None] = mapped_column(DateTime(timezone=False), nullable=True)
    representative_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    sentiment: Mapped[str] = mapped_column(String(24), default="Neutral", nullable=False)
    priority: Mapped[str] = mapped_column(String(24), default="Medium", nullable=False)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_insights: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    next_best_action: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False), server_default=func.now(), onupdate=func.now()
    )
